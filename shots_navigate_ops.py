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
	higher_frame_shot, lower_frame_shot,
	is_active_shot,
)


class ShotsNext(bpy.types.Operator):
	"Go to next shot [Operator]"
	bl_idname = "shotlist.shots_next"
	bl_label = "Go To Next Shot"
	bl_description = "Go to next shot in your shotlist"
	bl_options = {"UNDO"}
	
	@classmethod
	def poll(cls, context):
		return len(get_shots()) > 0
	
	def execute(self, context):
		shots = get_shots()
		next_shot = reduce(higher_frame_shot, sorted(shots, key=lambda shot: shot.frame))
		
		context.scene.frame_current = next_shot.frame
		
		return {"FINISHED"}


class ShotsPrevious(bpy.types.Operator):
	"""Go to previous shot [Operator]"""
	bl_idname = "shotlist.shots_previous"
	bl_label = "Go To Previous Shot"
	bl_description = "Go to previous shot in your shotlist"
	bl_options = {"UNDO"}
	
	@classmethod
	def poll(cls, context):
		return len(get_shots()) > 0
	
	def execute(self, context):
		shots = get_shots()
		
		previous_shot = reduce(lower_frame_shot, sorted(shots, key=lambda shot: shot.frame, reverse=True))
		
		context.scene.frame_current = previous_shot.frame
		
		return {"FINISHED"}


class ShotsGoTo(bpy.types.Operator):
	"""Go to specific shot [Operator]"""
	bl_idname = "shotlist.shots_goto"
	bl_label = "Go To Shot"
	bl_description = "Go to shot"
	bl_options = {"UNDO"}

	frame: bpy.props.IntProperty()
	
	@classmethod
	def poll(cls, context):
		return len(get_shots()) > 0
	
	def execute(self, context):
		context.scene.frame_current = self.frame
		
		return {"FINISHED"}