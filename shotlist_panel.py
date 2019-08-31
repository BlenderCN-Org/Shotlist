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

from functools import reduce

import bpy
from bpy.utils import time_from_frame

from . shotlist_api import (
	get_shots,
	is_active_shot,
	get_shot_after,
)
from . shotlist_ops import (
	ShotsAdd, ShotsRemoveShot, ShotsRemoveAll,
	ShotsNext, ShotsPrevious, ShotsGoTo,
	MarkersToggleLock,
)


# Main Panel
class ShotlistPanel(bpy.types.Panel):
	bl_idname = "SHOTSLIST_PT_ShotlistPanel"
	bl_label =  "Shotlist"
	bl_category = "Shotlist"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	
	@classmethod
	def poll(cls, context):
		# Only display this panel in object mode
		return context.mode == "OBJECT"

	def draw(self, context):
		scene = context.scene

		layout = self.layout

		box = layout.box()
		col = box.column()

		# Add New Shot Label
		col.label(text="New Shot")

		flow = col.grid_flow(columns=3, even_columns=False, even_rows=False, align=False)
		
		obj = context.object
		selected_object = obj.name if obj and obj.type == "CAMERA" else "No Camera Selected"
		selected_icon = "VIEW_CAMERA" if obj and obj.type == "CAMERA" else "RESTRICT_SELECT_ON"
		
		# Current Frame Label
		flow.column().label(text=str(scene.frame_current), icon="TIME")
		# New Shot Name Field
		new_shot_name = context.scene.shotlist_props.new_shot_name
		new_shot_name_icon = "EVENT_S" if not list(filter(lambda shot: shot.name == new_shot_name, get_shots())) else "ERROR"
		flow.column().prop(scene.shotlist_props, "new_shot_name", text="", icon=new_shot_name_icon)
		# Selected object Label
		flow.column().label(text=selected_object, icon=selected_icon)

		# ShotsAdd Button
		col.operator(ShotsAdd.bl_idname, text="Add Shot", icon="ADD")

		layout.separator()
		
		# Box that encapsulates the whole "shots" section
		box = layout.box()

		# Shots Header
		row = box.row(align=True)
		# Shots Count Label
		shots_count = len(get_shots())
		row.label(text=f"Shots:  {shots_count}", icon="SEQUENCE")
		# Lock Markers Toggle Button
		lock_icon = "LOCKED" if scene.tool_settings.lock_markers else "UNLOCKED"
		row.row().prop(context.scene.tool_settings, "lock_markers", icon=lock_icon, icon_only=True, emboss=False)
		
		box.row().prop(context.scene.shotlist_props, "show_camera_name")
		box.row().prop(context.scene.shotlist_props, "hide_inactive_cameras")

		# Next/Previous Shot Buttons
		row = box.row(align=True)
		row.operator(ShotsNext.bl_idname, text="Next Shot", icon="SORT_ASC")
		row.operator(ShotsPrevious.bl_idname, text="Previous Shot", icon="SORT_DESC")
		
		if not get_shots():
			return
		
		grid_header = ("START", "SHOT", "CAMERA", "DURATION", "")
		flow = box.row().grid_flow(columns=len(grid_header), even_columns=False, even_rows=False, align=True)
		for title in grid_header:
			flow.label(text=title)

		sorted_shots = sorted(get_shots(), key=lambda shot: shot.frame)
		
		sub_box = box.box()
		for shot in sorted_shots:
			flow = sub_box.grid_flow(columns=len(grid_header), even_columns=True, even_rows=True, align=True)
			
			flow.operator(ShotsGoTo.bl_idname, text=f"{shot.frame}", emboss=True, depress=is_active_shot(shot)).frame = shot.frame
			flow.prop(shot, "name", text="")

			flow.prop(shot, "camera", text="", icon="DOT")

			next_shot = get_shot_after(shot.frame)
			shot_frames = next_shot.frame - shot.frame if next_shot else scene.frame_end - shot.frame
			show_seconds = True
			shot_duration_str = f"{int(time_from_frame(shot_frames).seconds)}s" if show_seconds else str(shot_frames)
			flow.label(text=shot_duration_str)

			flow.operator(ShotsRemoveShot.bl_idname, text="", emboss=False, depress=False, icon="CANCEL").at_frame = shot.frame
		
		# Ideal would be to disable only the editable or destructive props, or at least leave the frame button clickable
		sub_box.enabled = True if not scene.tool_settings.lock_markers else False
		
		layout.separator()

		# ShotsRemoveAll Button
		row = layout.row()
		row.operator(ShotsRemoveAll.bl_idname, text="Remove All Shots", icon="CANCEL")

		row.enabled = False if scene.tool_settings.lock_markers else True