# python3
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Blender Add-on to Set and Manage Camera Shots.
"""

bl_info = {
	"name": "Shotlist (Alpha)",
	"author": "Hyuri Pimentel",
	"description": "Set and Manage Camera Shots",
	"blender": (2, 81, 0),
	"version": (1, 0, 0),
	"location": "View3D > Properties > Shotlist",
	"support": "COMMUNITY",
	"warning": "",
	"category": "3D View"
}

import bpy


from . shotlist_ops import OPERATORS
from . shotlist_props import ShotlistProps
from . shotlist_panel import ShotlistPanel
from . shotlist_handlers import (
	DEPSGRAPTH_UPDATE_PRE,
	FRAME_CHANGE_PRE,
)


def register():
	# Operators
	for op in OPERATORS:
		bpy.utils.register_class(op)

	# Panel
	bpy.utils.register_class(ShotlistPanel)

	# Props
	bpy.utils.register_class(ShotlistProps)
	bpy.types.Scene.shotlist_props = bpy.props.PointerProperty(type=ShotlistProps)

	# Handlers
	for fn in DEPSGRAPTH_UPDATE_PRE:
		bpy.app.handlers.depsgraph_update_pre.append(fn)
	
	for fn in FRAME_CHANGE_PRE:
		bpy.app.handlers.frame_change_pre.append(fn)


def unregister():
	# Operators
	for op in OPERATORS:
		bpy.utils.unregister_class(op)

	# Panel
	bpy.utils.unregister_class(ShotlistPanel)

	# Props
	bpy.utils.unregister_class(ShotlistProps)
	if bpy.context.scene.get("shotlist_props"):
		del bpy.context.scene["shotlist_props"]
	try:
		del bpy.types.Scene.shotlist_props
	except:
		pass
	
	# Handlers
	for fn in DEPSGRAPTH_UPDATE_PRE:
		bpy.app.handlers.depsgraph_update_pre.remove(fn)
	
	for fn in FRAME_CHANGE_PRE:
		bpy.app.handlers.frame_change_pre.remove(fn)


if __name__ == "__main__":
	register()