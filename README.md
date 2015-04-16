cloudify-jboss-plugin
=====================

Cloudify plugin for managing the JBoss application server

This plugin was developed for Cloudify version 3.1 and is a part of the regression testing we’re doing therefore should be used with care. 

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

2.  Add a node that uses tasks from plugin.

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
      - http://www.getcloudify.org/spec/cloudify/3.1/types.yaml
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


Optionally you can jboss['admin'] and jboss['password'] parameters if authentication is needed by jboss.

Installing driver how-to
-----------

To install JDBC driver and add datasource on JBoss you need to add following fields to 'start' inputs:

                datasource:
                  name: postgreDS
                  jndi: java:jboss/datasources/postgreDS
                  xa-class-name: org.postgresql.xa.PGXADataSource
                  driver-class-name: org.postgresql.Driver
                  url: jdbc:postgresql://localhost:5432/dbname
                jdbc_driver:
                  name: postgresql
                  path-from: /tmp/postgresql.jar
                  org-com: org


Explanation of parameters:
----

#### datasource - group of parameters (dictionary) containing parameters defining datasource ####

*  name: name of desired datasource
*  jndi: jndi name upon which this datasource will be registered
*  xa-class-name: class name for XA datasources
*  driver-class-name: class name for driver
*  url: url to access database


#### jdbc_driver- group of parameters (dictionary) containing parameters defining jndi-driver ####

*   name: name which will be used by datasource to determine which driver to use
*   path-from: absolute location of driver jar
*   org-com: determines which path should be saved and registered

#### Assumptions for the above example ####

*   Both `plugin.yaml` and `plugin.zip` are served on `localhost:8001`.
*   JBoss server is up and running.
*   JBoss management is available on `localhost:8888`.
*   User `cloudify_user` exists and can be accessed with
    `my secret password`.
*   Postgresql is installed on localhost and available at 5432 port, has dbname database set and is up and running.
*   File postgresql.jar is located at /tmp/postgresql.jar.
