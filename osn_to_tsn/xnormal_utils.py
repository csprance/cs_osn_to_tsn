# python
'''
This script allows you to use xNormal within Modo
It uses xml bake settings files and runs them through xnormal.exe
All of these settings can be set from within Modo

'''
__author__ = 'Chris Sprance'
__version__ = 0.01

import xml.etree.ElementTree as ET
import subprocess
import tempfile
import os
import sys
import lx
import lxu.object


class Baker(object):

    """This Class Contains all the methods necessary to modify xml files based on settings and tweak and save the xml file"""

    def __init__(self):
        super(Baker, self).__init__()

        # this is the path to the settings file
        self.settings_file = lx.eval('user.value settings_file ?')

        self.xpath = lx.eval('user.value baker_xpath ?')

        # bake_settings.xml file for xNormal to run
        self.settings = self.parseXML()

        # hi poly settings
        self.hi_poly_settings = self.settings.find(
            'HighPolyModel').find('Mesh').attrib

        # low poly settings
        self.lo_poly_settings = self.settings.find(
            'LowPolyModel').find('Mesh').attrib
        # generate map settings
        self.generate_maps_settings = self.settings.find('GenerateMaps').attrib

        # path to xNormal
        self.xpath = lx.eval('user.value baker_xpath ?')

        # dictionary that contains all the user values
        self.user_values = self.get_user_values()

        # this is the base directory of the kit
        self.BASE_PATH = (lx.eval(
            'query platformservice path.path ? scripts') + "\\baker").replace("\\", "/")

    def get_user_values(self):
        user_values = dict()
        # This list contains all our user values.
        uv = [
            'low_poly_mesh',  # low poly mesh
            'baker_xpath',  # path where xnormal resides at
            'hi_poly_mesh',  # hi poly mesh
            'cage_mesh',  # cage mesh
            'settings_file',  # where the settings file is stored at
            # should we overwrite the file or warn about it
            'baker_overwrite_warn',
            'baker_bucket_size',  # render bucket size
            'baker_aa',  # how much aa to us 1x 2x 4x
            'baker_map_size_x',  # what size to output the width
            # what size to output the height
            'baker_map_size_y',
            # where to output the maps to
            'baker_map_output',
            # how much edge padding to use
            'baker_edge_padding',
            'baker_height_map',  # bool bake height map
            # method used to normalize height map
            'baker_height_normalization',
            'baker_base_texture_map',  # bool bake base texture
            'baker_ao_map',  # bool bake AO
            'baker_ao_rays',  # int num rays
            'baker_ao_distribution',  # list choice
            'baker_ao_bias',  # int
            'baker_ao_spread_angle',  # int
            'baker_ao_limit_ray_distance',  # bool
            'baker_ao_attenuation_x',  # int
            'baker_ao_attenuation_y',  # int
            'baker_ao_attenuation_z',  # int
            'baker_ao_jitter',  # bool
            'baker_ao_ignore_backface_hits',  # bool
            'baker_ao_allow_full_occlusion',  # bool
            'baker_cavity_map',  # bool should we bake a cavity map
            'baker_cavity_rays',  # how many rays to use
            'baker_cavity_radius',  # int
            'baker_cavity_contrast',  # int
            'baker_cavity_steps',  # int
            # bool should we bake a normal map?
            'baker_norm_map',
            # bool should the normal map be a tangent space
            # world map
            'baker_tangent_space',
            # the swizzle of the normal this is a string
            # xyz +-
            'baker_norm_swiz_x',
            # the swizzle of the normal this is a string
            # xyz +-
            'baker_norm_swiz_y',
            # the swizzle of the normal this is a string
            # xyz +-
            'baker_norm_swiz_z',
            # bool bake curvature map
            'baker_curvature_map',
            'baker_curvature_rays',  # how many rays to use
            # Bool use jitter or curavutre?
            'baker_curvature_jitter',
            'baker_curvature_bias',  # int
            'baker_curvature_spread_angle',  # int
            # string uniform cosine cosinesq
            'baker_curvature_algorithm',
            # string uniform cosine cosinesq
            'baker_curvature_distribution',
            'baker_curvature_search_distance',  # int
            # monocrom twotone threecolor string
            'baker_curvature_tone_mapping',
            # should we use smoothing boolean
            'baker_curvature_smoothing',
        ]

        # go through every user value and get them
        for x in uv:
            user_values[x] = lx.eval('user.value %s ?' % x)
        return user_values

    def parseXML(self):
        """Parse the xml and return the xml tree back to us"""
        bake_settings = open(self.settings_file)
        tree = ET.parse(bake_settings).getroot()
        return tree

    def writeXML(self):
        '''This method writes settings from the settings dictionary to an xml file and returns the file object'''
        # open the settings file
        f = open(self.settings_file + '_bake', 'w+')
        # write the file using utf-8 encoding
        f.write(ET.tostring(self.settings, encoding='UTF-8'))
        f.close()
        # return the file object
        return f

    def set_user_values(self):
        # low poly mesh file
        self.lo_poly_settings['File'] = self.user_values['low_poly_mesh']

        # cage mesh file
        self.lo_poly_settings['CageFile'] = self.user_values['cage_mesh']

        # where is the hi poly file at
        self.hi_poly_settings['File'] = self.user_values['hi_poly_mesh']

        # How much edge padding to use
        self.generate_maps_settings['EdgePadding'] = str(
            self.user_values['baker_edge_padding'])

        # Where to output the file
        self.generate_maps_settings[
            'File'] = self.user_values['baker_map_output']

        # Generate Normal map boolean
        self.generate_maps_settings['GenNormals'] = 'true' if self.user_values[
                                                                  'baker_norm_map'] == 1 else 'false'

        # Generate AO map boolean
        self.generate_maps_settings['GenAO'] = 'true' if self.user_values[
                                                             'baker_ao_map'] == 1 else 'false'

        # Cavity Map Generation Boolean
        self.generate_maps_settings['GenCavity'] = 'true' if self.user_values[
                                                                 'baker_cavity_map'] == 1 else 'false'

        # Should the normal map be tangent space or world space?
        self.generate_maps_settings['TangentSpace'] = 'true' if self.user_values[
                                                                    'baker_tangent_space'] == 1 else 'false'

        # contains all the sizes of the map to bake
        baker_sizes = {'0': '256', '1': '512', '2': '1024',
                       '3': '2048', '4': '4096', '5': '8192'}
        # set the height and width by looking up a dictionary value based
        # on a key from a user value
        self.generate_maps_settings['Width'] = baker_sizes[
            self.user_values['baker_map_size_x']]
        self.generate_maps_settings['Height'] = baker_sizes[
            self.user_values['baker_map_size_y']]

    def startBake(self):
        '''This kicks off the xNormal worker thread'''
        self.set_user_values()
        config_file = self.writeXML()
        # Try To Kick off the xNormal worker fail silently
        try:
            subprocess.Popen(
                str(self.xpath + ' ' + self.settings_file + '_bake'))
            return config_file
        except:
            lx.out("Bake Failed Please Check Settings and try again")

'''
Start the main thread off

'''


def main():
    # create our baker instance
    x = Baker()
    config = x.startBake()
    lx.out(x.BASE_PATH)
    lx.out(__version__)


if __name__ == '__main__':
    main()