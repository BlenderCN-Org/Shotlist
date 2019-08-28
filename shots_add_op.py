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

from . import shotlist_api


# Shot Add Operator
class ShotsAdd(bpy.types.Operator):
	bl_idname = "shotlist.add_shot"
	bl_label = "Add New Shot"
	bl_description = "Add new shot for the active Camera, at current frame"
	bl_options = {"UNDO"}

	# shot_name: bpy.props.StringProperty(
		# default=str(len(bpy.context.scene.timeline_markers)),
	# )

	@classmethod
	def poll(cls, context):
		return context.object.type == "CAMERA"
	
	def execute(self, context):
		added_shot = shotlist_api.add_shot()
		
		if added_shot:
			self.report({"INFO"}, f"Shot '{added_shot.name}' Added")
		
		else:
			# Temporary. Should be replaced with dialog asking whether to replace or to cancel
			self.report({"WARNING"}, f"Shot Not Added. Remove Existing Shot First")
		
		return {"FINISHED"}