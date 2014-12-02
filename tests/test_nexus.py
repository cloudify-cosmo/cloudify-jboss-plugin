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

import os
import httplib
import unittest
from cloudify.mocks import MockCloudifyContext
from cloudify.state import current_ctx
from nexus import nexuscon
from jboss import utils


class TestNexus(unittest.TestCase):
    """
        This is Nexus integration test. Nexus instance should be at
        11.0.0.8:8080/nexus url and should have jboss-helloworld.war
        in (repository id) test_repository_id, (artifact name)
        jboss-helloworld, (version) 1.0, (group id) testGroupId,
        (type) war. Nexus should have also anonymous user disabled
        and test user with credentials test:test created.
    """
    def setUp(self):
        ctx = MockCloudifyContext()
        ctx.node.properties['nexus'] = "http://repo.maven.apache.org/maven2/"
        current_ctx.set(ctx)

    def test_download_file_no_credentials(self):
        parameters = {"r": "central",
                      "a": "HTTPClient",
                      "v": "0.3-3",
                      "g": "HTTPClient",
                      "p": "jar"}
        file_name = 'HTTPClient.jar'
        util = utils.Utils()
        nexus = nexuscon.NexusConnector()
        code = nexus.download_file(parameters,
                                   file_name,
                                   util.tempdir)
        self.assertTrue(code == httplib.OK)
        self.assertTrue(os.path.exists(util.tempdir + '/' + file_name))

    # def test_download_with_credentials(self):
    #     parameters = {"r": "test_repository_id",
    #                   "a": "jboss-helloworld",
    #                   "v": "1.0",
    #                   "g": "testGroupId",
    #                   "p": "war"}
    #     file_name = 'jboss-helloworld.war'
    #     util = utils.Utils()
    #     nexus = nexuscon.NexusConnector()
    #     code = nexus.download_war_file(parameters,
    #                                    file_name,
    #                                    util.tempdir,
    #                                    'test',
    #                                    'test')
    #     self.assertEqual(code, httplib.OK)
    #     self.assertTrue(os.path.exists(util.tempdir + '/' + file_name))

if __name__ == '__main__':
    unittest.main()
