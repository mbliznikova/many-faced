Many-faced is a framework for running Selenium tests on different platforms against the web-applications using Jenkins. 

So there is the ability to write and run the new Python Selenium autotests without carrying about setUp and tearDown, you can just inherit the new tests class from BaseTestCase class and use the driver object. 



### How to use many-faced?

The many-faced framework consists of:
* __File job_templates.yaml__ to create Jenkins jobs with specified parameters. It consists of the following sections:
    * ‘defaults’ section: the default values that can be common for all jobs, for example, address of application, grid, etc. You can change these values in jobs in ‘project’ section.
    * ‘builder’ sections: the macros for the jobs. 
    * 'project' section: the jobs for creating in Jenkins. It created from job templates defined in ‘job-template' sections. The jobs in Jenkins are created with specified values in corresponding macros defined in the corresponding job template. 
    * ‘job-template’ sections: there are templates for jobs. 
* __File base_setup_teardown.py__ (Python file with BaseTestCase class with setUp and tearDown methods) to inherit from it to write new tests.
* __File configure_jenkins.yaml__ to update the framework (if something in git repository of framework will change).

__Prerequisites__:

Before you start you should have 
1. Jenkins ([how get it and set it up](https://jenkins.io/download/))
2. Jenkins job builder ([how get it and set it up](https://docs.openstack.org/infra/jenkins-job-builder/))
3. Running Selenium Grid with all desired capabilities - OSs and browsers ([how get it and set it up](https://seleniumhq.github.io/docs/grid.html)). So remember that tests should execute on the nodes in headless mode (read [1](http://elementalselenium.com/tips/38-headless), [2](http://stackoverflow.com/questions/6183276/how-do-i-run-selenium-in-xvfb )).  
4. Deployed web-application
5. Selenium tests for application


__There are 3 common cases__:

You have deployed web-application and want to run Selenium tests against it and 
1. You have git repository with Selenium tests
2. You want to write Selenium tests for your application and run these tests against application
3. You have git repository with Selenium tests and you want to add some other tests and run all these tests against application 
