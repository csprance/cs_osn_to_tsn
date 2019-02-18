import modo
import lx


def convert_osn_to_tsn_using_xnormal(filepath):
    print(filepath)
    return "NewFilePath.tga"


def get_selected_clip_filepath():
    scene = modo.Scene()
    [clip] = scene.selectedByType(lx.symbol.sITYPE_VIDEOSTILL)
    filepath = clip.channel("filename").get()
    return filepath


def execute(msg, flags):
    clip_filepath = get_selected_clip_filepath()
    tsn_filepath = convert_osn_to_tsn_using_xnormal(clip_filepath)
