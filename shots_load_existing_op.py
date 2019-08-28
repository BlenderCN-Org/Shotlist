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

from . shotlist import SHOTLIST


# Shot Add Operator
class ShotsLoadExisting(bpy.types.Operator):
	bl_idname = "shotlist.shots_scan"
	bl_label = "Scan Existing Shots"
	bl_description = "Add existing shots to Shotlist"
	# bl_options = {"UNDO"}

	@classmethod
	def poll(cls, context):
		cls.refresh()
		
		return len(context.scene.timeline_markers) > 0
	
	def execute(self, context):
		SHOTLIST.scan_markers()
		
		self.report({"INFO"}, f"Finished Scanning Timeline")
		return {"FINISHED"}
	
	@classmethod
	def refresh(cls):
		# pass
		# Remove marker-orphan shots
		# TODO

		# Refresh Shots' Start Frames
		# for shot in SHOTLIST:
		# 	shot_marker = bpy.context.scene.timeline_markers[shot.name]
		# 	shot.start = shot_marker.frame
		
		# # Scan Existing Shots
		if len(bpy.context.scene.timeline_markers) > 0:
			SHOTLIST.scan_markers()