### Show the object for exactly one frame
def HideObjectKeyframe(obj,frame_number):
    # Hide the object from the start of the scene until the desired frame number
    # Keyframes from 0 to T-1 to ensure it remains hidden the entire time.
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_render",frame=0)
    obj.keyframe_insert(data_path="hide_render",frame=frame_number-1)
    # Display the object for frame T and save keyframe.
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide_render",frame=frame_number)
    # Hide object again at frame T+1 and save keyframe.
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_render",frame=frame_number+1)
