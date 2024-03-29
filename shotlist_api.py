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


def get_shot_at(frame):
	for shot in get_shots():
		if shot.frame == frame:
			return shot
	
	return None


def get_shot_after(reference_frame, wrap_around=False):
	next_shot = get_adjecent_shot(reference_frame, "right", wrap_around)

	return next_shot


def get_shot_before(reference_frame, wrap_around=False):
	previous_shot = get_adjecent_shot(reference_frame, "left", wrap_around)

	return previous_shot


def get_adjecent_shot(reference_frame, side="right", wrap_around=False):
	index = 0 if side == "right" else -1
	slicing_function = (lambda shot: shot.frame > reference_frame) if side == "right" \
		else (lambda shot: shot.frame < reference_frame)
	
	shots = get_shots()
	shots_left_or_right_reference = list(filter(slicing_function, shots))
	
	if not shots_left_or_right_reference:
		if wrap_around:
			return sorted(shots, key=lambda shot: shot.frame)[index]
		
		return None
	
	shots_left_or_right_reference_sorted = sorted(shots_left_or_right_reference, key=lambda shot: shot.frame)
	
	# Return first(0) shot from shots after playhead, or last(-1) shot of shots before the playhead
	return shots_left_or_right_reference_sorted[index]


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
	
	new_shot_name_prop = context.scene.shotlist_props.new_shot_name

	if list(filter(lambda shot: shot.name == new_shot_name_prop, get_shots())):
		return
	
	new_shot_name = new_shot_name_prop or f"Shot_{len(get_shots()) + 1}"

	shot_at_playhead = get_shot_at(scene.frame_current)
	if shot_at_playhead:
		scene.timeline_markers.remove(shot_at_playhead)

	shot = scene.timeline_markers.new(name=new_shot_name, frame=scene.frame_current)
	shot.camera = context.object

	scene.shotlist_props.new_shot_name = ""

	return shot


def remove_shot(shot):
	bpy.context.scene.timeline_markers.remove(shot)


def remove_all():
	for marker in bpy.context.scene.timeline_markers:
		if marker.camera:
			bpy.context.scene.timeline_markers.remove(marker)


# ----------------------------------------------------------------------------
# Checkers

def is_active_shot(shot):
	scene = bpy.context.scene
	frame_current = scene.frame_current

	sorted_shots = sorted(get_shots(), key=lambda shot: shot.frame)
	shots_frames = [shot.frame for shot in sorted_shots]

	# Check if playhead is at any shot's frame
	if scene.frame_current in shots_frames:
		# Check if playhead is at this particular shot
		return shot.frame == scene.frame_current
	
	# Check if the shot to the left of the playhead is the active shot
	previous_shot = get_shot_before(frame_current, wrap_around=True)
	if shot == previous_shot and previous_shot.frame < frame_current:
		return True
	
	# Check if the shot to the right of the playhead is the active shot
	next_shot = get_shot_after(frame_current, wrap_around=True)
	
	if shot == next_shot and previous_shot.frame > frame_current:
		return True
	
	return False