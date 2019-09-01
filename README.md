![Shotlist_v0 0 3_Screenshot](https://user-images.githubusercontent.com/18584014/64071810-b3f6e000-cc58-11e9-9f31-b485a496957c.png)

# Shotlist | Shot Manager for Blender 2.8
### Quickly Create, Change, Remove, and Navigate Through Your Shots.
#### Leaves your regular markers untouched.
Originally developed for my own use—when the process of switching between cameras was a little more convoluted, in Blender—but updated and upgraded(read: made more useful) for 2.8.

# TODO:
- Add "framing", and other fields
- Add settings popover menu
- Add confirmation dialog to Remove All operator, unless undo is reliable on that end
- Add dialog asking whether to replace the existing shot or not, when adding a shot at a frame that already has a shot
- Merge shots navigate operators into one
- Improve is_active_shot's design
- Shot Configuration UI, with presets, and quick buttons(like the Pixar one) (goes hand in hand with the one above)
- Be able to disable/enable, in the settings, the visibility of some fields


### FUTURE:
- Investigate creating new camera data for each shot, switching at each shot's start frame, so that you can have different camera settings for each shot. Maybe sync the name of the camera data with the name of the shot... or, have a custom prop that keeps track of this link. Remember to  always have fake user active/save the data even with no users
- Add option, in the settings, to have the "DURATION" field follow timeline "show_seconds"
- Be able to have multiple, named, shotlists
- Add slider, to quickly zip through the shots?
- Auto use_pin main panel?
