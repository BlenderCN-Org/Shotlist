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


# ----------------------------------------------------------------------------
# Getters

def get_shots():
	"""
	Get all shots available.
	Returns a List.
	"""
	scene = bpy.context.scene
	return list(filter(lambda marker: marker.camera, scene.timeline_markers))


def higher_frame_shot(a, b):
	frame_current = bpy.context.scene.frame_current

	if a.frame > b.frame:
		if a.frame > frame_current:
			return a
		elif b.frame > frame_current:
			return b
		return a
	
	else:
		if a.frame > frame_current:
			return a
		elif b.frame > frame_current:
			return b
		return a
	
	return a


def lower_frame_shot(a, b):
	frame_current = bpy.context.scene.frame_current

	if a.frame < b.frame:
		if a.frame < frame_current:
			return a
		elif b.frame < frame_current:
			return b
		return a
	
	else:
		if a.frame < frame_current:
			return a
		elif b.frame < frame_current:
			return b
		return a
		
	return a


# ----------------------------------------------------------------------------
# Add/Remove

def add_shot():
	"""
	Add new shot to the scene.
	Returns shot(marker) if successful;
	Returns None if there is another shot at current frame.
	"""
	context = bpy.context
	scene = context.scene

	shots = get_shots()

	if scene.frame_current in (shot.frame for shot in shots):
		return
	
	shots_count = len(get_shots())
	shot = scene.timeline_markers.new(name=f"Shot_{shots_count + 1}", frame=scene.frame_current)
	shot.camera = context.object
	# shot.framing = 'MS'
	
	# For ignore/replace functionality (to be implemented)
	# matching_frame = list(filter(lambda shot: shot.frame == bpy.context.scene.frame_current, shots))

	# if any(matching_frame):
	# 	for shot in matching_frame:
	# 		remove(shot)

	return shot


# def remove(shot):
# 	bpy.context.scene.timeline_markers.remove(shot.marker)
# 	shots.remove(shot)

def remove_all():
	for marker in bpy.context.scene.timeline_markers:
		if marker.camera:
			bpy.context.scene.timeline_markers.remove(marker)


# ----------------------------------------------------------------------------
# Checkers

def is_active_shot(shot):
	scene = bpy.context.scene

	markers = scene.timeline_markers
	sorted_shots = sorted(list(filter(lambda marker: marker.camera, markers)), key=lambda shot: shot.frame)
	shots_frames = [shot.frame for shot in sorted_shots]

	# Check if playhead is at any shot's frame
	if scene.frame_current in shots_frames:
		# Check if playhead is at this particular shot
		return shot.frame == scene.frame_current
	
	# Check if the shot to the left of the playhead is the active shot
	previous_shot = reduce(lower_frame_shot, sorted(sorted_shots, key=lambda shot: shot.frame, reverse=True))
	if shot == previous_shot and previous_shot.frame < scene.frame_current:
		return True
	
	# Check if the shot to the right of the playhead is the active shot
	next_shot = reduce(higher_frame_shot, sorted(sorted_shots, key=lambda shot: shot.frame))
	if shot == next_shot and previous_shot.frame > scene.frame_current:
		return True
	
	return False