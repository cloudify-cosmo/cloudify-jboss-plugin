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
        ctx = MockCloudifyContext(
            node_id='id',
            node_name='name',
            properties={'nexus': "https://repository.jboss.org/nexus"})
        current_ctx.set(ctx)

    def test_download_file_no_credentials(self):
        parameters = {"r": "google",
                      "a": "visualization-datasource",
                      "v": "1.0.1",
                      "g": "com.google.visualization",
                      "p": "pom"}
        file_name = 'HTTPClient.jar'
        util = utils.Utils()
        nexus = nexuscon.NexusConnector()
        code = nexus.download_file(parameters,
                                   file_name,
                                   util.tempdir)
        self.assertTrue(code == httplib.OK)
        self.assertTrue(os.path.exists(util.tempdir + '/' + file_name))

if __name__ == '__main__':
    unittest.main()
