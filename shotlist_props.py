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


framing_sizes = {
	('text', 'ECU', 'description', 0),
	('text', 'CU', 'description', 1),
	('text', 'MS', 'description', 2),
	('text', 'WS', 'description', 3),
	('text', 'EWS', 'description', 4),
}


def get_framing(self, number):
	return number


def set_framing(self, value):
	print("Setting value", value)


framing_prop = bpy.props.EnumProperty(
	name="Framing",
	items=framing_sizes,
	description="Framing sizes",
	get=get_framing,
	set=set_framing,
	default="WS",
)


class ShotProps(bpy.types.PropertyGroup):
	pass
	# shot_current: bpy.props.IntProperty()

	# new_shot_name: bpy.props.StringProperty(
	# 	default="",
	# 	description="New shot name",
	# )

	# search_bar: bpy.props.StringProperty(
	# 	default="",
	# 	description="Search shots by name"
	# )