# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapColoringDialog
                                 A QGIS plugin
 Coloring a map with minimal number of color
                             -------------------
        begin                : 2012-09-24
        copyright            : (C) 2012 by Alain Delplanque
        email                : alaindelplanque@laposte.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from ui_mapcoloring import Ui_MapColoring

class MapColoringDialog(QDialog, Ui_MapColoring):
    algorithme = ["Welsh - Powell", "DSATUR"]

    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        QObject.connect(self.saveAsButton, SIGNAL("clicked()"), self.outFile)
        layers = self.getLayerNames()
        self.inputLayerCombo.addItems(layers)
        self.algorithmeCombo.addItems(self.algorithme)
        self.algorithmeCombo.setCurrentIndex(0)


    def getLayerNames(self):
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        layerList = []
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer:
                if layer.geometryType() == QGis.Polygon:
                    layerList.append( unicode( layer.name() ) )
        return layerList


    # Return QgsVectorLayer from a layer name ( as string )
    def getVectorLayerByName(self, layerName):
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == layerName:
                if layer.isValid():
                    return layer
                else:
                    return None


    def outFile(self):
        self.outputLayerEdit.clear()
        (self.shapefileName, self.encoding) = self.saveDialog(self)
        if self.shapefileName is None or self.encoding is None:
            return
        self.outputLayerEdit.setText(QString(self.shapefileName))

    def saveDialog(self, parent ):
        settings = QSettings()
        dirName = settings.value( "/UI/lastShapefileDir" ).toString()
        filtering = QString( "Shapefiles (*.shp)" )
        encode = settings.value( "/UI/encoding" ).toString()
        fileDialog = QgsEncodingFileDialog( parent, "Save output shapefile", dirName, filtering, encode )
        fileDialog.setDefaultSuffix( QString( "shp" ) )
        fileDialog.setFileMode( QFileDialog.AnyFile )
        fileDialog.setAcceptMode( QFileDialog.AcceptSave )
        fileDialog.setConfirmOverwrite( True )
        if not fileDialog.exec_() == QDialog.Accepted:
            return None, None
        files = fileDialog.selectedFiles()
        settings.setValue("/UI/lastShapefileDir", QVariant( QFileInfo( unicode( files.first() ) ).absolutePath() ) )
        return ( unicode( files.first() ), unicode( fileDialog.encoding() ) )

    #overide
    def accept(self):
        if self.inputLayerCombo.currentText() == "":
            QMessageBox.information(self, "Error", self.tr("Please specify input vector layer"))
            return
        if self.outputLayerEdit.text() == "":
            QMessageBox.information(self, "Error", self.tr("Please specify output shapefile"))
            return
        if self.encoding == "":
            self.encoding = "utf-8"
        self.do(self.inputLayerCombo.currentText(),self.outputLayerEdit.text())
        QDialog.accept(self)


    def computeMatrixAll(self, m, layer, selected):
        # Calcul la matrice de connection en testant toutes les combinaisons
        feature = QgsFeature()
        poly = []
        for s in selected:
            layer.featureAtId(s, feature)
            poly.append(QgsGeometry(feature.geometry()))
        for i in range(len(selected)-1):
            for j in range(i+1, len(selected)):
                if poly[i].touches(poly[j]):
                    inter = poly[i].intersection(poly[j])
                    if not inter is None:
                        if inter.type() in [1, 2]:
                            m[selected[i]].add(selected[j])
                            m[selected[j]].add(selected[i])


    def computeMatrixRec(self, m, layer, bbox, selected, progressFrom, progressTo):
        if len(selected) <= 20:
            self.computeMatrixAll(m, layer, selected)
        else:
            # Calcul récursif après partage en deux
            # Calcul BBox
            bbox0 = QgsRectangle(bbox[selected[0]])
            for i in range(1, len(selected)):
                bbox0.combineExtentWith(bbox[selected[i]])
            # Partage en deux de la bbox
            if bbox0.width() > bbox0.height():
                # Partage vertical
                bbox1 = QgsRectangle(bbox0)
                bbox1.setXMaximum((bbox0.xMinimum()+bbox0.xMaximum())/2)
                bbox2 = QgsRectangle(bbox0)
                bbox2.setXMinimum(bbox1.xMaximum())
            else:
                # Partage horitontal
                bbox1 = QgsRectangle(bbox0)
                bbox1.setYMaximum((bbox0.yMinimum()+bbox0.yMaximum())/2)
                bbox2 = QgsRectangle(bbox0)
                bbox2.setYMinimum(bbox1.yMaximum())
            # Construction des deux sous groupes
            selected1 = [s for s in selected if bbox[s].intersects(bbox1)]
            selected2 = [s for s in selected if bbox[s].intersects(bbox2)]
            # Appel récursif sur les deux sous groupes
            if len(selected) == len(selected1) or len(selected) == len(selected2):
                # Echec du partage en deux, recherche sur l'ensemble des combinaisons possibles
                self.computeMatrixAll(m, layer, selected)
            else:
                self.computeMatrixRec(m, layer, bbox, selected1, progressFrom, (progressFrom+progressTo)/2)
                self.computeMatrixRec(m, layer, bbox, selected2, (progressFrom+progressTo)/2, progressTo)
        self.progressBar.setValue(progressTo)


    def computeMatrix(self, layer):
        # Extraction des BBox
        nbFeat = layer.featureCount()
        bbox = []
        feature = QgsFeature()
        for i in range(nbFeat):
            layer.featureAtId(i, feature)
            bbox.append(feature.geometry().boundingBox())

        # Initialisation des sommets adjacents
        m = [set() for i in range(nbFeat)]
        # Calcul récursif
        self.computeMatrixRec(m, layer, bbox, range(nbFeat), 0.0, 100.0)
        return m


    def colorationWelshPowell(self, m):
        vertex = range(len(m))
        vertex.sort(key=lambda i: len(m[i]), reverse=True)

        # Initialisation du tableau de couleur, indexé par le no de sommet
        vertexColor = [-1 for i in range(len(vertex))]

        # Affectation des couleurs par algorithme de Welsh-Powell
        currentColor = 0
        done = 0

        # Boucle sur la couleur
        while len(vertex) > 0:
            # Boucle sur les sommets
            i = 0
            while i < len(vertex):
                # Test si current color est possible
                if currentColor in [vertexColor[j] for j in m[vertex[i]]]:
                    i += 1
                else:
                    vertexColor[vertex[i]] = currentColor
                    del vertex[i]
                    done += 1
                    self.progressBar.setValue(done*100/len(m))
            currentColor += 1
        return vertexColor


    def colorationDSATUR(self, m):
        # Classement des sommets en fonction de leur nombre DSAT
        DSAT = []
        vertexDSAT = [len(adj) for adj in m]
        DSAT = [[] for i in range(max(vertexDSAT)+1)]
        for i in range(len(m)):
            # Ajout à la liste DSAT
            DSAT[vertexDSAT[i]].append(i)

        # Algorithme principal:
        vertexColor = [-1 for i in range(len(m))]
        done = 0
        # Boucle de coloration
        while len(DSAT) > 0:
            # Sommet suivant à colorer : nDSAT max, et si égalité degré max
            currentVertex = DSAT[len(DSAT)-1][0]
            # couleur à utiliser : la plus petite possible
            colorUsed = [vertexColor[i] for i in m[currentVertex] if vertexColor[i] != -1]
            colorUsed.sort()
            currentColor = 0
            for i in colorUsed:
                if i > currentColor:
                    break
                currentColor = i+1
            # coloration du sommet
            vertexColor[currentVertex] = currentColor
            # Suppression du sommet currentVertex des liste DSAT
            del DSAT[len(DSAT)-1][0]

            # Mise à jour des nombres DSAT, Itération sur les sommets adjacents au sommet qui vient d'être coloré
            for i in m[currentVertex]:
                if vertexColor[i] != -1: # Le sommet est déjà coloré, rien à faire
                    continue
                # Calcul du nouveau DSAT
                newDSAT = len([1 for s in m[i] if vertexColor[s] != -1])
                # Suppression de i dans DSAT[oldDSAT]
                oldDSAT = vertexDSAT[i]
                DSAT[oldDSAT].remove(i)
                # Ajoute de i dans DSAT[newDSAT], trie par degré décroissant
                while newDSAT >= len(DSAT):
                    DSAT.append([])
                k = 0
                while k < len(DSAT[newDSAT]):
                    if len(m[DSAT[newDSAT][k]]) < len(m[i]):
                        break
                    k += 1
                DSAT[newDSAT].insert(k, i)
                # Mise à jour du nombre DSAT dans vertex
                vertexDSAT[i] = newDSAT
            # Nétoyage de DSAT
            while len(DSAT) > 0:
                if len(DSAT[len(DSAT)-1]) > 0:
                    break
                DSAT.pop()
            done += 1
            self.progressBar.setValue(done*100/len(m))

        return vertexColor


    def do(self, inputLayer, outputLayer):
        vlayer = self.getVectorLayerByName(inputLayer)
        nbFeat = vlayer.featureCount()

        # Matrice des connections
        self.stateLabel.setText("calculating connexion graph :")
        m = self.computeMatrix(vlayer)

        # Classement des sommets par nombre de connections, et liste des sommets adjacents
        self.stateLabel.setText("Map coloring :")
        self.progressBar.setValue(0)
        algoId = self.algorithmeCombo.currentIndex()
        if algoId == 0:
            vertexColor = self.colorationWelshPowell(m)
        elif algoId == 1:
            vertexColor = self.colorationDSATUR(m)

        # Enregistrement dans le fichier final
        self.stateLabel.setText("Save output file :")
        self.progressBar.setValue(0)
        # Liste des champs de données
        fields = {}
        fields[0] = QgsField(self.colorField.text(), QVariant.Int)
        if self.keepFieldsCheckBox.isChecked():
            for sindex, sfield in vlayer.dataProvider().fields().iteritems():
                fields[len(fields)] = sfield

        # Création du fichier
        outShapefile = QgsVectorFileWriter(outputLayer, self.encoding, fields,
            vlayer.dataProvider().geometryType(), vlayer.dataProvider().crs())

        # Insertion des polygones
        feature = QgsFeature()
        done = 0
        for i in range(nbFeat):
            vlayer.featureAtId(i, feature)
            attr_src = feature.attributeMap()
            attr_dst = {0: QVariant(vertexColor[i])}
            if self.keepFieldsCheckBox.isChecked():
                for i in range(1, len(fields)):
                    attr_dst[i] = attr_src[i-1]
            feature.setAttributeMap(attr_dst)
            outShapefile.addFeature(feature)
            done += 1
            self.progressBar.setValue(done*100/nbFeat)

        del outShapefile

        # Ouverture du fichier
        self.iface.addVectorLayer(outputLayer, os.path.basename(str(outputLayer)), "ogr")



























