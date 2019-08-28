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
	get_next_shot, get_previous_shot,
	is_active_shot,
)
from . shotlist_ops import (
	ShotsAdd, ShotsRemoveAll,
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
		# Get active Scene
		scene = context.scene
		# Get active object
		obj = context.object

		layout = self.layout

		current_selection_column = layout.box().column()

		# Add New Shot Label
		current_selection_column.label(text="New Shot")

		current_selection_grid = current_selection_column.grid_flow(columns=0, even_columns=False, even_rows=False, align=True)

		# current_selection_grid.box().operator(ShotsGoTo.bl_idname, text=f"{str(shot.frame)}").frame = shot.frame
		### FIX ###
		# If we have an active object
		if obj:
			if obj.type == "CAMERA":
				# Active active label
				current_selection_grid.box().label(text=obj.name, icon="OUTLINER_OB_CAMERA")

			else:
				# Active obj label
				current_selection_grid.box().label(text=obj.name, icon="OBJECT_DATA")

		# If no active object
		else:
			# Info
			current_selection_grid.box().label(text="No Camera Selected", icon="RESTRICT_SELECT_ON")
		
		# Current Frame Label
		current_selection_grid.box().label(text=str(scene.frame_current), icon="TIME")
		# shots_add_row.props(props, "new_shot_name", icon="TIME", icon_only=False, emboss=False)
		# ShotsAdd Button
		current_selection_column.operator(ShotsAdd.bl_idname, text="Add Shot", icon="ADD")

		layout.separator()
		
		# shots_row
		shots_row = layout.box()
		# Shots Header
		shots_header = shots_row.row(align=True)
		# Shots Label
		shots_count = len(get_shots())
		shots_header.label(text=f"Shots:  {shots_count}", icon="SEQUENCE")
		# Lock Markers
		lock_icon = "LOCKED" if scene.tool_settings.lock_markers else "UNLOCKED"
		shots_header.row().prop(context.scene.tool_settings, "lock_markers", icon=lock_icon, icon_only=True, emboss=True)
		
		# Alternative Left/Right Icons: "BACK"/"FOWARD"
		navigation_buttons_row = shots_row.row(align=True)
		navigation_buttons_row.operator(ShotsPrevious.bl_idname, text="Previous Shot", icon="SORT_DESC")
		navigation_buttons_row.operator(ShotsNext.bl_idname, text="Next Shot", icon="SORT_ASC")

		# Props
		# props = scene.shot_props
		# SearchBar
		# shots_row.row().prop(props, "search_bar", text="Search", icon="VIEWZOOM")
		
		if not get_shots():
			return

		header_row = shots_row.row().column(align=True)

		header_grid = header_row.grid_flow(columns=4, even_columns=True, even_rows=False, align=True)

		# for title in ("START", "SHOT", "FRAMING", "CAMERA"):
		for title in ("START", "SHOT", "CAMERA"):
			header_grid.row().label(text=str(title))
		
		body_row = shots_row.row().column(align=True)

		sorted_shots = sorted(get_shots(), key=lambda shot: shot.frame)
		
		for shot in sorted_shots:
			body_grid = body_row.grid_flow(columns=4, even_columns=False, even_rows=False, align=True)
			
			body_grid.box().operator(ShotsGoTo.bl_idname, text=f"{shot.frame}", emboss=True, depress=is_active_shot(shot)).frame = shot.frame
			body_grid.box().prop(shot, "name", text="")
			# body_grid.box().prop(shot, "framing", text="")
			body_grid.box().label(text=shot.camera.name)
		
		# Ideal would be to disable only the editable or destructive props, or at least leave the frame button clickable
		body_row.enabled = False if scene.tool_settings.lock_markers else True
		
		layout.separator()

		# ShotsRemoveAll Button
		remove_all_row = layout.row()
		remove_all_row.operator(ShotsRemoveAll.bl_idname, text="Remove All Shots", icon="CANCEL")

		remove_all_row.enabled = False if scene.tool_settings.lock_markers else True