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
from bpy.props import StringProperty, BoolProperty


class ShotlistProps(bpy.types.PropertyGroup):
	new_shot_name: StringProperty(
		name="New Shot Name",
		description="The name of your new shot (e.g. 58A)",
	)

	show_camera_name: BoolProperty(
		name="Show Camera Name",
		description="Show active camera's name",
		default=True,
	)

	hide_inactive_cameras: BoolProperty(
		name="Hide Inactive Cameras",
		description="Hide all but the active camera",
	)