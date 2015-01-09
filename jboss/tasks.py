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

from cloudify import ctx
from cloudify.decorators import operation
from jbosscli import JBossClient
from utils import Utils


def install_driver(jcli,
                   jdbc_driver,
                   datasource,
                   **kwargs):
    """
    Handle jdbc driver installation.
    :param jcli:
    :param jdbc_driver:
    :param datasource:
    :param kwargs:
    :return:
    """
    ctx.logger.info('Starting driver installation')
    jcli.install_jdbc_driver_as_core_module(jdbc_driver['name'],
                                            jdbc_driver['path-from'],
                                            jdbc_driver['org-com'])
    jcli.add_jdbc_driver_command(jdbc_driver['name'],
                                 jdbc_driver['org-com'],
                                 datasource['xa-class-name'],
                                 datasource['driver-class-name'])
    jcli.create_datasource_command(datasource['name'],
                                   datasource['jndi'],
                                   jdbc_driver['name'],
                                   datasource['url'])
    jcli.create_enable_datasource_command(datasource['name'])


@operation
def deploy(jboss,
           jdbc_driver=None,
           datasource=None,
           **kwargs):
    ctx.logger.info('Starting deploy')
    utils = Utils()
    resource_name = jboss['resource-name']
    ctx.logger.info('Deployment filename {0}'.format(resource_name))
    jcli = JBossClient(utils.tempdir, jboss)
    resource_dir = jboss['resource-dir']
    if (jdbc_driver is not None) and (datasource is not None):
        install_driver(jcli, jdbc_driver, datasource)
    jcli.create_deploy_command(resource_dir, resource_name)
    jcli.run_script()


@operation
def undeploy(jboss,
             **kwargs):
    ctx.logger.info('Starting undeploy')
    utils = Utils()
    resource_name = jboss['resource-name']
    ctx.logger.info('Filename to undeploy ' + resource_name)
    jcli = JBossClient(utils.tempdir, jboss)
    jcli.create_undeploy_command(resource_name)
    jcli.run_script()


@operation
def redeploy(jboss,
             **kwargs):
    undeploy(jboss)
    deploy(jboss)
