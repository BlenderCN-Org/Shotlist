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
	"version": (0, 0, 2),
	"location": "View3D > Properties > Shotlist",
	"support": "COMMUNITY",
	"warning": "",
	"category": "3D View"
}

import bpy


from . shotlist_ops import OPERATORS
from . shotlist_panel import ShotlistPanel
# from . shotlist_props import (
# 	ShotProps,
# 	framing_sizes,
# 	get_framing, set_framing,
# )
# from . shotlist_menu import ShotlistMenu


# def draw_menu(self, context):
# 	self.layout.menu(ShotlistMenu.bl_idname)


def register():
	# Operators
	for op in OPERATORS:
		bpy.utils.register_class(op)

	# Panel
	bpy.utils.register_class(ShotlistPanel)

	# # Props
	# bpy.utils.register_class(ShotProps)
	# bpy.types.Scene.shot_props = bpy.props.PointerProperty(type=ShotProps)

	# Framing prop
	# bpy.types.TimelineMarker.framing = framing_prop

	# Menu
	# bpy.utils.register_class(ShotlistMenu)
	# bpy.types.VIEW3D_MT_object.append(draw_menu)


def unregister():
	# Operators
	for op in OPERATORS:
		bpy.utils.unregister_class(op)

	# Panel
	bpy.utils.unregister_class(ShotlistPanel)

	# # Props
	# bpy.utils.unregister_class(ShotProps)

	# if bpy.context.scene.get("shot_props"):
	# 	del bpy.context.scene["shot_props"]

	# for shot in bpy.context.scene.timeline_markers:
	# 	try:
	# 		del shot.framing
	# 	except AttributeError:
	# 		pass

	# try:
	# 	del bpy.types.Scene.shot_props
	# 	# del bpy.types.TimelineMarker.framing
	# except:
	# 	pass
	
	# Menu
	# bpy.utils.unregister_class(ShotlistMenu)
	# bpy.types.VIEW3D_MT_object.remove(draw_menu)


if __name__ == "__main__":
	register()