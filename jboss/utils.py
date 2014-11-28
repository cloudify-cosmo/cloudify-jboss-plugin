###############################################################################
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
###############################################################################

import tempfile
import os
import shutil
import subprocess
from cloudify import ctx


class Utils:
    """ Utility class of useful tools  """
    def __init__(self):
        self.tempdir = tempfile.mkdtemp()
        ctx.logger.info('Tempdir created: [{0}]'.format(self.tempdir))

    def __del__(self):
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)
            ctx.logger.info('Tempdir removed: [{0}]'.format(self.tempdir))

    @staticmethod
    def save_command_to_file(command, file_path):
        """
        :param command: command to be put into file
        :param file_name: full path to command file
        :return:
        """
        with open(file_path, 'w+') as file:
            file.write(command)

    @staticmethod
    def append_command_flags(flags_string, file_path):
        """
        :param command: command to be put into file
        :param file_name: full path to command file
        :return:
        """
        with open(file_path, 'a+') as file:
            file.write(' ' + flags_string)

    @staticmethod
    def append_command_to_file(command, file_path):
        """
        :param command: command to be put into file
        :param file_name: full path to command file
        :return:
        """
        with open(file_path, 'a+') as file:
            file.write('\n' + command)

    @staticmethod
    def system(*args, **kwargs):
        """
        :param args: list of commandline arguments
        :param kwargs:
        :return:
        """
        kwargs.setdefault('stdout', subprocess.PIPE)
        process = subprocess.Popen(args, **kwargs)
        out, err = process.communicate()
        return out
