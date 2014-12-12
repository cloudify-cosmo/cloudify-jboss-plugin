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


@operation
def install_driver(jboss, jdbc_driver, datasource, **kwargs):
    ctx.logger.info('Starting driver installation')
    utils = Utils()
    jcli = JBossClient(utils.tempdir, jboss)
    driver_name = jdbc_driver.get('name')
    driver_path_from = jdbc_driver.get('path_from')
    jcli.install_jdbc_driver_as_core_module(driver_name, driver_path_from)
    jcli.create_datasource_command(datasource['name'],
                                   datasource['jndi'],
                                   driver_name,
                                   datasource['url'])
    jcli.create_enable_datasource_command(datasource['name'])


@operation
def deploy(jboss, **kwargs):
    ctx.logger.info('Starting deploy')
    utils = Utils()
    resource_name = jboss['resource_name']
    ctx.logger.info('Deployment filename {0}'.format(resource_name))
    jcli = JBossClient(utils.tempdir, jboss)
    resource_dir = jboss['resource_dir']
    jcli.create_deploy_command(resource_dir, resource_name)
    jcli.run_script()
    utils.delete_file(resource_dir + '/' + resource_name)


@operation
def undeploy(jboss, **kwargs):
    ctx.logger.info('Starting undeploy')
    utils = Utils()
    resource_name = jboss['resource_name']
    ctx.logger.info('Filename to undeploy ' + resource_name)
    jcli = JBossClient(utils.tempdir, jboss)
    jcli.create_undeploy_command(resource_name)
    jcli.run_script()


@operation
def redeploy(jboss, **kwargs):
    undeploy(jboss)
    deploy(jboss)
