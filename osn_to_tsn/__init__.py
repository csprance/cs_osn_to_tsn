import os
import tempfile
import subprocess

import modo
import lx
import lxu


def get_xnormal_path():
    # if the value is not set create it and ask the user what it is then set that value
    if lx.eval('user.value xnormal_path ?') == '':
        # ask the user where it's located at here
        # set up our fileOpen Dialog
        lx.eval("dialog.setup fileOpen")
        lx.eval('dialog.title "Select xNormal Path"')
        # open the dialog
        lx.eval("dialog.open")
        # dialog.result ? holds the name of the file dialog
        xnormal_path = lx.eval("dialog.result ?")
        # set the path to the user value
        lx.eval('user.value xnormal_path "%s"' % xnormal_path)
    # if the value does exist return that
    return lx.eval("user.value xnormal_path ?")


def get_selected_meshes():
    scene = modo.Scene()
    meshes = scene.selectedByType(lx.symbol.sITYPE_MESH)
    return meshes


def get_selected_clip_filepath():
    scene = modo.Scene()
    [clip] = scene.selectedByType(lx.symbol.sITYPE_VIDEOSTILL)
    filepath = clip.channel("filename").get()
    return filepath


def start_bake(
    input_mesh_path,
    input_normal_map,
    output_normal_map,
    smooth_normals=False,
    osn_to_tsn=True,
    edge_padding=32,
):

    command = "%s -os2ts %s %s %s %s %s %s" % (
        get_xnormal_path(),
        input_mesh_path,
        smooth_normals,
        input_normal_map,
        output_normal_map,
        osn_to_tsn,
        edge_padding,
    )
    return subprocess.Popen(command).wait()


def export_selected_meshes_to_tempfile():
    """
    Exports any selected meshes as one mesh
    scene.saveAs filepath filetype save_selected
    :return: str the path to the created temp file
    """
    lo_poly_mesh_path = os.path.join(tempfile.gettempdir(), "low_poly_mesh.fbx")
    eval_command = 'scene.saveAs "%s" fbx true' % lo_poly_mesh_path
    print(eval_command)
    lx.eval(eval_command)
    return lo_poly_mesh_path


def import_new_clip(img_path):
    sel_svc = lxu.select.SceneSelection()
    current_scene = sel_svc.current()
    scn_svc = lx.service.Scene()
    # get a channel object
    chan = current_scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)
    # channel writ object
    channel_out = lx.object.ChannelWrite(chan)
    # add a videoStill item to the scene
    v_clip = current_scene.ItemAdd(scn_svc.ItemTypeLookup(lx.symbol.sITYPE_VIDEOSTILL))
    # get the index of the videoStill item's filename channel
    idx = v_clip.ChannelLookup(lx.symbol.sICHAN_VIDEOSTILL_FILENAME)
    # set the filename
    channel_out.String(v_clip, idx, img_path)


def execute(msg, flags):
    osn_filepath = get_selected_clip_filepath()
    input_mesh_filepath = export_selected_meshes_to_tempfile()
    output_filename = (
        os.path.splitext(os.path.basename(osn_filepath))[0]
        + "_TSN"
        + os.path.splitext(osn_filepath)[1]
    )
    output_filepath = os.path.join(os.path.dirname(osn_filepath), output_filename)
    results = start_bake(input_mesh_filepath, osn_filepath, output_filepath)
    if results == 0:
        # TODO: Check if the clips filepath already exists and updated instead of importing
        import_new_clip(output_filepath)
