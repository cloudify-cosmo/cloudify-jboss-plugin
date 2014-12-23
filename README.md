cloudify-jboss-plugin
=====================

Cloudify plugin for managing the JBoss application server



What it does
------------

The plugin:

1.  deploys provided resource on JBoss server,
2.  deletes resource after deployment from JBoss server,
3.  undeploys provided resource from JBoss server.

Additionally:

4.  installs provided JDBC driver,
5.  sets up datasource on JBoss server,
6.  enables datasource on JBoss server.

Basic how-to
-----------

1.  Import the plugin in blueprint.

2.  Add a node that uses .

3.  In *inputs* for task deploy or undeploy:
    *   create `jboss` section,
    *   add ip address to the jboss server as `ip` parameter,
    *   add path to directory where resource to be deployed exists as `home_path` parameter,
    *   add path to directory where resource to be deployed exists as `resource_dir` parameter,
    *   add name of deployed resource as `resource_name` parameter,

    for example:

        start: 
          implementation: jboss.jboss.tasks.deploy
          inputs:
            jboss:
              ip: 127.0.0.1:8888
              home_path: /home/vagrant/EAP-6.2.0/jboss-eap-6.2
              resource_dir: /tmp
              resource_name: jboss-helloworld.war

### Minimum working example ###

The following is a basic working example:

tosca_definitions_version: cloudify_dsl_1_0
imports:
  - http://www.getcloudify.org/spec/cloudify/3.1rc1/types.yaml
  - http://127.0.0.1:8001/plugin.yaml

node_templates:
  myhost:
    type: cloudify.nodes.Compute
    properties:
      ip: 127.0.0.1
      cloudify_agent:
        user: cloudify_user
        key: /home/cloudify_user/.ssh/id_rsa

  jboss_server:
    type: cloudify.nodes.Root
    interfaces:
      cloudify.interfaces.lifecycle:
        start: 
          implementation: jboss.jboss.tasks.deploy
          inputs:
            jboss:
              ip: 127.0.0.1:8888
              home_path: /home/vagrant/EAP-6.2.0/jboss-eap-6.2
              resource_dir: /tmp
              resource_name: jboss-helloworld.war
        stop:   
          implementation: jboss.jboss.tasks.undeploy
          inputs:
            jboss: 
              ip: 127.0.0.1:8888
              home_path: /home/vagrant/EAP-6.2.0/jboss-eap-6.2
              resource_dir: /tmp
              resource_name: jboss-helloworld.war
    relationships:
      - type: cloudify.relationships.contained_in
        target: myhost

#### Assumptions for the above example ####

*   Both `plugin.yaml` and `plugin.zip` are served on `localhost:8001`.
*   JBoss server is up and running.
*   JBoss management is available on `localhost:8888`.
*   User `cloudify_user` exists and can be accessed with
    `my secret password`.

