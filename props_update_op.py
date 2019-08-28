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


class PropsUpdate(bpy.types.Operator):
	"""Update props' values."""

	bl_idname = "shotlist.props_update"
	bl_label = "Update props"
	# bl_options = {"UNDO"}
	
	def execute(self, context):
		bpy.context.scene.shot_props.update_prop(context)

		return {"FINISHED"}