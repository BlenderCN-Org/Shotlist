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

from . shotlist_api import (
	get_shots,
	is_active_shot,
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

		flow = col.grid_flow(columns=0, even_columns=False, even_rows=False, align=True)
		
		obj = context.object
		selected_info = obj.name if obj and obj.type == "CAMERA" else "No Camera Selected"
		selected_icon = "OUTLINER_OB_CAMERA" if obj and obj.type == "CAMERA" else "RESTRICT_SELECT_ON"
		
		# Selected object Label
		flow.box().label(text=selected_info, icon=selected_icon)
		# Current Frame Label
		flow.box().label(text=str(scene.frame_current), icon="TIME")

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
		
		# Next/Previous Shot Buttons
		row = box.row(align=True)
		row.operator(ShotsPrevious.bl_idname, text="Previous Shot", icon="SORT_DESC")
		row.operator(ShotsNext.bl_idname, text="Next Shot", icon="SORT_ASC")
		
		if not get_shots():
			return

		flow = box.row().grid_flow(columns=4, even_columns=False, even_rows=False, align=True)

		for title in ("START", "SHOT", "CAMERA", ""):
			flow.label(text=str(title))

		sorted_shots = sorted(get_shots(), key=lambda shot: shot.frame)
		
		sub_box = box.box()
		for shot in sorted_shots:
			flow = sub_box.grid_flow(columns=4, even_columns=True, even_rows=True, align=True)
			
			flow.operator(ShotsGoTo.bl_idname, text=f"{shot.frame}", emboss=True, depress=is_active_shot(shot)).frame = shot.frame
			flow.prop(shot, "name", text="")
			flow.label(text=shot.camera.name)
			flow.operator(ShotsRemoveShot.bl_idname, text="", emboss=False, depress=False, icon="CANCEL").at_frame = shot.frame
		
		# Ideal would be to disable only the editable or destructive props, or at least leave the frame button clickable
		sub_box.enabled = False if scene.tool_settings.lock_markers else True
		
		layout.separator()

		# ShotsRemoveAll Button
		row = layout.row()
		row.operator(ShotsRemoveAll.bl_idname, text="Remove All Shots", icon="CANCEL")

		row.enabled = False if scene.tool_settings.lock_markers else True