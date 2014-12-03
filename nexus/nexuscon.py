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

import urllib
import httplib
from cloudify import ctx
from nexus.restful import RestRequest


class NexusConnector():
    """ Nexus Rest connector  """
    LOCAL_REST_PATH = u'/service/local'
    MAVEN_CONTENT_PATH = u'/artifact/maven/content'
    REDIRECT_PATH = u'redirect'

    def __init__(self):
        self.nexus_base_path = ctx.node.properties['nexus']

    def download_file(self,
                      parameters,
                      output_file,
                      tempdir,
                      user=None,
                      password=None):
        """
        Download war file from Nexus that is
        :param parameters: dictionary of artifact parameters:
        repoId, artifactId, version, groupId, type
        :param output_file: filename to save
        :return: None if everything ok, http error code otherwise
        """
        url = urllib.urlencode(parameters)
        url = self.nexus_base_path + \
            self.LOCAL_REST_PATH + \
            self.MAVEN_CONTENT_PATH + \
            '?' + url
        ctx.logger.info('Requested url: [{0}]'.format(url))
        request = RestRequest.prepare_request(url, 'GET', user, password)
        out, code = RestRequest.process_request(request)
        if code == httplib.OK:
            with open(tempdir + '/' + output_file, 'w') as f:
                f.write(out)
        else:
            ctx.logger.error("Error while downloading artifact : {0}"
                             .format(code))
        return code
