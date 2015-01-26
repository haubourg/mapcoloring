# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapColoring
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
 This script initializes the plugin, making it known to QGIS.
"""
def name():
    return "Map coloring"
def description():
    return "Coloring a map such that two contiguous polygons do not have the same color. The algorithm does not always provide a solution with a minimum number of colors."
def version():
    return "Version 0.2"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.8"
def classFactory(iface):
    # load MapColoring class from file MapColoring
    from mapcoloring import MapColoring
    return MapColoring(iface)
