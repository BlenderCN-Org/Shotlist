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


class Shot:
	name = None
	camera = None
	start = None
	end = None
	scene = None
	marker = None

	def __init__(self, name, camera, start, end, scene, marker):
		self.name = name
		self.camera = camera
		self.start = start
		self.end = end
		self.scene = scene
		self.marker = marker


class ShotList:
	shots = set()

	def __init__(self):
		pass
	
	def scan_markers(self):
		# self.refresh()

		markers = bpy.context.scene.timeline_markers
		
		for marker in markers:
			if marker.camera:
				if not set(filter(lambda shot: shot.marker == marker, self.shots)):
					shot = Shot(name=marker.name if marker.name else f"Shot_{len(self.shots) + 1}", camera=marker.camera, start=marker.frame, scene=bpy.context.scene, marker=marker, end=None)
					
					self.shots.add(shot)

	def add(self):
		matching_frame = list(filter(lambda shot: shot.start == bpy.context.scene.frame_current, self.shots))

		if any(matching_frame):
			for shot in matching_frame:
				self.remove(shot)

		marker = bpy.context.scene.timeline_markers.new(name=f"Shot_{len(self.shots) + 1}")
		marker.camera = bpy.context.object
		marker.frame = bpy.context.scene.frame_current

		shot = Shot(name=f"Shot_{len(self.shots) + 1}", camera=bpy.context.object, start=bpy.context.scene.frame_current, scene=bpy.context.scene, marker=marker, end=None)

		self.shots.add(shot)

	def remove(self, shot):
		bpy.context.scene.timeline_markers.remove(shot.marker)
		self.shots.remove(shot)

	def remove_all(self):
		for shot in self.shots:
			bpy.context.scene.timeline_markers.remove(shot.marker)
		
		self.shots = set()

	def __len__(self):
		return len(self.shots)
	
	def __iter__(self):
		return iter(self.shots)


SHOTLIST = ShotList()