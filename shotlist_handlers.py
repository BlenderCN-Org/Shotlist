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

import bpy

from . shotlist_api import get_shots


@bpy.app.handlers.persistent
def show_camera_name(self):
	if bpy.context.scene.shotlist_props.show_camera_name:
		for shot in get_shots():
			shot.camera.show_name = True
			shot.camera.data.show_name = True
	
	else:
		for shot in get_shots():
			shot.camera.show_name = False
			shot.camera.data.show_name = False


@bpy.app.handlers.persistent
def hide_inactive_cameras(self):
	if bpy.context.scene.shotlist_props.hide_inactive_cameras:
		for shot in get_shots():
			if shot.camera != bpy.context.scene.camera:
				shot.camera.hide_viewport = True
			
			else:
				shot.camera.hide_viewport = False
				if bpy.context.object.type == "CAMERA":
					shot.camera.select_set(True)
					bpy.context.view_layer.objects.active = shot.camera
	
	else:
		for shot in get_shots():
			shot.camera.hide_viewport = False


DEPSGRAPTH_UPDATE_PRE = (
	show_camera_name,
	hide_inactive_cameras,
)

FRAME_CHANGE_PRE = (
	hide_inactive_cameras,
)