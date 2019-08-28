# TODO:
- Add "shot name" field to "new shot area"
- Add "framing" and other fields
- Add confirmation dialog to Remove All operator
- Add dialog asking whether to replace the existing shot or not, when adding a shot at a frame that already has a shot
- Merge shots navigate operators into one
- Improve is_active_shot's design
- Change ShotlistPanel's layout naming to official recommendations


### FUTURE:
- Investigate creating new camera data for each shot, switching at each shot's start frame, so that you can have different camera settings for each shot. Maybe sync the name of the camera data with the name of the shot... or, have a custom prop that keeps track of this link. Remember to  always have fake user active/save the data even with no users
- Shot Configuration UI, with presets, and quick buttons(like the Pixar one) (goes hand in hand with the one above)
- Be able to have multiple, named, shotlists
- Add slider, to quickly zip through the shots?
- Auto use_pin main panel?