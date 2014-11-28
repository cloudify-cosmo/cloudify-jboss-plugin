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

import httplib
from cloudify import ctx
from cloudify.decorators import operation
from jbosscli import JBossClient
from nexus import nexuscon
from utils import Utils


@operation
def deploy(*args, **kwargs):
    ctx.logger.info('Starting deploy')
    utils = Utils()
    file_name = get_filename()
    parameters = get_artifact_parameters()
    ctx.logger.info('Deployment filename {0}'.format(file_name))
    nexus = nexuscon.NexusConnector()
    if nexus.download_file(parameters, file_name, utils.tempdir) != httplib.OK:
        ctx.logger.info("There is no file to be deployed. Exiting.")
        return
    ctx.logger.info('File ' + file_name)
    jcli = JBossClient(utils.tempdir)
    jcli.create_deploy_command(file_name)
    jcli.run_script()


@operation
def undeploy(*args, **kwargs):
    ctx.logger.info('Starting undeploy')
    utils = Utils()
    file_name = get_filename()
    ctx.logger.info('Filename to undeploy ' + file_name)
    jcli = JBossClient(utils.tempdir)
    jcli.create_undeploy_command(file_name)
    jcli.run_script()


@operation
def redeploy(*args, **kwargs):
    undeploy()
    deploy()


def get_artifact_parameters():
    parameters = dict()
    parameters['a'] = ctx.node.properties['artifact']['artifactId']
    parameters['r'] = ctx.node.properties['artifact']['repositoryId']
    parameters['p'] = ctx.node.properties['artifact']['extension']
    parameters['g'] = ctx.node.properties['artifact']['groupId']
    parameters['v'] = ctx.node.properties['artifact']['version']
    return parameters


def get_filename():
    return ctx.node.properties['artifact']['artifactId'] + \
        '.' + ctx.node.properties['artifact']['extension']
