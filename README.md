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
