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


# Remove All Shots Operator
class ShotsRemoveShot(bpy.types.Operator):
	bl_idname = "shotlist.remove_shot"
	bl_label = "Remove Specific Shot"
	bl_description = "Remove Specific Shot"
	bl_options = {"UNDO"}

	at_frame: bpy.props.IntProperty()
	
	def execute(self, context):
		shot = shotlist_api.get_shot_at(self.at_frame)
		shot_name = shot.name

		shotlist_api.remove_shot(shot)
		
		self.report({"INFO"}, f"Shot '{shot_name}' Removed")
		return {"FINISHED"}