# coding=utf-8


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

import unittest
import os
from jboss import utils


class TestUtils(unittest.TestCase):

    def test_utils_temp_folder(self):
        util = utils.Utils()
        tempdir = util.tempdir
        self.assertTrue(os.path.exists(tempdir))
        del util
        self.assertFalse(os.path.exists(tempdir))

    def test_utils_to_script(self):
        util = utils.Utils()
        filename = util.tempdir + '/' + 'test'
        command = 'Test'
        util.save_command_to_file(command, filename)
        f = open(filename, 'r')
        self.assertEqual(f.read(), command)

    def test_utils_append_flags_to_script(self):
        util = utils.Utils()
        filename = util.tempdir + '/' + 'test'
        command = 'Test'
        util.save_command_to_file(command, filename)
        flags = '--Flags'
        util.append_command_flags(flags, filename)
        f = open(filename, 'r')
        self.assertEqual(f.read(), command + flags)

    def test_utils_append_command_to_script(self):
        util = utils.Utils()
        filename = util.tempdir + '/' + 'test'
        command = 'Test'
        util.save_command_to_file(command, filename)
        command2 = 'Test2'
        util.append_command_to_file(command2, filename)
        f = open(filename, 'r')
        self.assertEqual(f.read(), command + '\n' + command2)

    def test_utils_subproces(self):
        command = 'Test'
        out = utils.Utils.system('echo', command)
        self.assertEqual(out, command + '\n')

if __name__ == '__main__':
    unittest.main()
