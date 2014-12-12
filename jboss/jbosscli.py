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

import re
import shutil
from cloudify import ctx
from utils import Utils


class JBossClient(object):
    """JBoss Client of standalone mode using jboss-cli.sh """

    def __init__(self, tempdir, parameters):
        self.tempdir = tempdir
        self.address = parameters['ip']
        self.user = parameters.get('user')
        self.password = parameters.get('password')
        self.home_path = parameters['home_path']
        self.cli_path = self.home_path + '/bin/jboss-cli.sh'
        self.command_script = self.tempdir + '/script.cli'
        self.modules = self.home_path + '/modules'
        command = 'connect \nbatch'
        Utils.save_command_to_file(command, self.command_script)

    def create_undeploy_command(self, war_name):
        """
        Create undeploy command that is saved to file 'script.cli'
        in temporary folder to get invoked by jboss-cli.sh '--file' parameter
        :param war_name: name of war to be undeployed
        :return:
        """
        undeploy_command = 'undeploy' + ' ' + war_name
        ctx.logger.info('Undeploy command [{0}]'.format(undeploy_command))
        Utils.append_command_to_file(undeploy_command, self.command_script)

    def create_deploy_command(self, resource_dir, resource_name):
        """
        Create deploy command that is saved to file 'script.cli'
        in temporary folder to get invoked by jboss-cli.sh '--file' parameter
        :param resource_path full path to resource
        :return:
        """
        deploy_command = 'deploy' + ' ' + resource_dir + '/' + resource_name
        ctx.logger.info('Deploy command [{0}]'.format(deploy_command))
        Utils.append_command_to_file(deploy_command, self.command_script)

    def install_jdbc_driver_as_core_module(self, driver_name, path_from):
        self.modules = '{0}/modules/org/{1}/main'.format(self.home_path,
                                                         driver_name)
        Utils.create_subdirs_recursively(self.modules)
        shutil.copy(path_from, self.modules + '/{0}.jar'.format(driver_name))
        self.add_module_file(driver_name)

    def add_module_file(self, driver_name):
        text = '<module xmlns=\"urn:jboss:module:1.1\" name=\"org.{0}\">'\
               '<resources>'\
               '<resource-root path="{0}.jar"/>'\
               '</resources>'\
               '<dependencies>'\
               '<module name=\"javax.api\"/>'\
               '<module name=\"javax.transaction.api\"/>'\
               '</dependencies>'\
               '</module>' \
            .format(driver_name)
        file_path = self.modules + '/module.xml'
        Utils.save_command_to_file(text, file_path)

    def add_jdbc_driver_command(self, xa_datasource_class_name):
        name = 'postgresql'
        text = '/subsystem=datasources/jdbc-driver={0}:' \
               'add(driver-module-name=org.{0},' \
               'driver-xa-datasource-class-name={1})'\
            .format(name, xa_datasource_class_name)
        Utils.append_command_to_file(text, self.command_script)

    def create_datasource_command(self,
                                  datasource_name,
                                  jndi_name,
                                  driver_name,
                                  connection_url):
        """
        Create datasource command that is added to file 'script.cli'
        in temporary folder to get invoked by jboss-cli.sh '--file' parameter
        :return:
        """
        datasource_command = 'data-source add --name=' + datasource_name + \
                             ' --jndi-name=' + jndi_name +\
                             ' --driver_name=' + driver_name + \
                             ' --connection_url=' + connection_url
        ctx.logger.info('Data source command: [{0}]'
                        .format(datasource_command))
        Utils.append_command_to_file(datasource_command, self.command_script)

    def create_xadatasource_command(self,
                                    datasource_name,
                                    jndi_name,
                                    driver_name,
                                    connection_url):
        """
        Create datasource command that is saved to file 'datasource.cli'
        in temporary folder to get invoked by jboss-cli.sh '--file' parameter
        :return:
        """
        datasource_command = 'data-source add --name=' + datasource_name + \
                             ' --jndi-name=' + jndi_name + \
                             ' --driver_name=' + driver_name + \
                             ' --connection_url=' + connection_url
        ctx.logger.info('Data source XA command: [{0}]'
                        .format(datasource_command))
        Utils.append_command_to_file(datasource_command, self.command_script)

    def create_enable_datasource_command(self, datasource_name):
        enable_command = 'data-source enable --name=' + datasource_name
        ctx.logger.info('Enable command: [{0}]'.format(enable_command))
        Utils.append_command_to_file(enable_command, self.command_script)

    def run_script(self):
        Utils.append_command_to_file('run-batch', self.command_script)
        if (self.user is None) or (self.password is None):
            out = Utils.system(self.cli_path,
                               '--file=' + self.command_script,
                               '--controller=' + self.address)
        else:
            out = Utils.system(self.cli_path,
                               '--file=' + self.command_script,
                               '--controller=' + self.address,
                               '--user=' + self.address,
                               '--password=' + self.password)
        if self.is_there_any_problem(out):
            ctx.logger.error(out)
        else:
            ctx.logger.info(out)

    @staticmethod
    def is_there_any_problem(out):
        result = re.compile(r'\b({0})\b'.format('failed'), flags=re.IGNORECASE)\
            .search(out)
        if result is None:
            return False
        return True


class JBossClientDomain(JBossClient):
    """JBoss client of domain mode using jboss-cli.sh   """
    def create_deploy_command(self, war_name, server_groups=None):
        """
        Create deploy command that is saved to file 'script.cli'
        in temporary folder to get invoked by jboss-cli.sh '--file' parameter
        :param war_name: name of war to be deployed
        :param server_groups: list of server group names the deploy command
        should apply to, if None "--all-server-groups" will be applied
        :return:
        """
        super(JBossClientDomain, self).create_deploy_command(war_name)
        if server_groups is None:
            server_group_command = '--all-server-groups'
        else:
            server_group_command = '--server-groups=' + ','.join(server_groups)

        Utils.append_command_flags(server_group_command, self.command_script)

    def create_undeploy_command(self, war_name, server_groups=None):
        """
        Create undeploy command that is saved to file 'script.cli'
        in temporary folder to get invoked by jboss-cli.sh '--file' parameter
        :param war_name: name of war to be undeployed
        :param server_groups: list of server group names the deploy command
        should apply to, if None "--all-server-groups" will be applied
        :return:
        """
        super(JBossClientDomain, self).create_undeploy_command(war_name)
        if server_groups is None:
            server_group_command = '--all-relevant-server-groups'
        else:
            server_group_command = '--server-groups=' + ','.join(server_groups)
        Utils.append_command_flags(server_group_command, self.command_script)
