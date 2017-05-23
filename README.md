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
6. Many-faced itself: create (or navigate) to directory where you want to have many-faced and clone it from github or download and unzip it.


__The common cases__:

You have deployed web-application and want to run Selenium tests against it and 
1. You have git repository with Selenium tests
2. You want to write Selenium tests for your application and run these tests against application
3. You have git repository with Selenium tests and you want to add some other tests and run all these tests against application 

First, you need to create jobs in job_templates.yaml. Let's discover the examples for all cases.

1. Run tests from git repository against your web application.
   
   1. Open job_templates.yaml
   2. Find ‘project’ section, ‘many-faced’ project, ‘jobs’ section.
   3. Create there job from 'tests_from_repo-{platform}-{browser}-{title}’ template.
   
You can specify the addresses of your app and grid in ‘defaults’ section (see above) for ‘app’ and ‘grid’ parameters respectively. It is useful when you want to create more that one job for the same application and the same grid. So you can define other defaults values in ‘defaults’ section depending on your needs. 
So you can specify the addresses in the body of the job in ‘project’ section, ‘many-faced’ project, ‘jobs’ section:
```
- 'tests_from_repo-{platform}-{browser}-{title}':
   platform: LINUX (you can specify any OSs and browser you have in Selenium grid)
   browser: chrome
   test_repo: <repo_address, for example, https://github.com/jjonson/app_tests>
   title: <just to make easy the identification of job, for example, 'the_first_case'>
``` 

2. Write new tests and run it against your web application.
   
   1. Create .py file with ’test_’ prefix in one directory with ‘base_setup_teardown' file.
   
   1. In this new file make import from base_setup_teardown import BaseTestCase.
   
   1. Create your test class, for example class MyTestCase and inherit it from class BaseTestCase.
   
   1. Write your test method and don\t care about setUp() and tearDown(), just use self.driver. 
   
   1. In the end of file put 
   
``` 
        if __name__ == '__main__':
            unittest.main()
``` 
Example of file with new tests (let’s name it test_some_faeture.py):
``` 
from base_setup_teardown import BaseTestCase
import unittest


class MyTestCase(BaseTestCase):
    def test_inspect_introduction(self):
        self.driver.find_element_by_link_text('Introduction').click()
        a = self.driver.find_element_by_id('welcome')
        self.assertTrue(a.is_displayed())

    def test_inspect_installationt(self):
        self.driver.find_element_by_link_text('Introduction').click()
        a = self.driver.find_element_by_id('introduction')
        self.assertTrue(a.is_displayed())

if __name__ == '__main__':
    unittest.main()
``` 
⋅⋅6. Open job_templates.yaml
⋅⋅7. Find ‘project’ section, ‘many-faced’ project, ‘jobs’ section.
⋅⋅8. Create there job from 'new_tests-{platform}-{browser}' template:
```
- 'new_tests-{platform}-{browser}-{title}':
   platform: LINUX
   browser: firefox
   test_dir: /path_to_directory_with_your_new_tests
   title: <for example, 'the_second_case'>
```

3. Write new tests, get tests from git repository and run them all against your web application.

⋅⋅⋅Clone tests from git repository.

⋅⋅⋅Put file ‘base_setup_teardown' in the same directory and create there file(s) with new tests.

⋅⋅⋅Open job_templates.yaml

⋅⋅⋅Find ‘project’ section, ‘many-faced’ project, ‘jobs’ section.

⋅⋅⋅Create there job from 'new_tests-{platform}-{browser}' template: 
```
- 'new_tests-{platform}-{browser}-{title}':
   platform: LINUX
   browser: firefox
   test_dir: /path_to_directory_with_your_new_tests
   title: <for example, 'the_third_case'>
```   

Second, the common part for the all cases is that you need to create these job(s) in Jenkins.

Here you need to create (or use the existing one) jenkins_jobs.ini file.
jenkins_jobs.ini should have at least following format:
``` 
[jenkins]
user=<jenkins user with permissions to create jobs>
password=<password for this user, you can find in in http://jenkins_address/me/configure in Show API Token...>
url=http://jenkins_address
``` 
When you have the jenkins_jobs.ini file, go to the terminal (if you have Linux) and execute the following command:
``` 
    jenkins-jobs --conf /<path_to_jenkins_jobs.ini_file> update  /<path_to_job_templates.yaml>
``` 

If job_templates.yaml is correct, you will see something like
``` 
INFO:root:Updating jobs in ['/<path_to_job_templates.yaml>'] ([])
INFO:jenkins_jobs.builder:Number of jobs generated:  <number of jobs you created>
INFO:jenkins_jobs.builder:Creating jenkins job <name of created job, for example, new_test-LINUX-chrome-the_first_case>
INFO:jenkins_jobs.builder:Creating jenkins job <name of created job, for example, test-LINUX-firefox-the_third_case>
``` 

Go to your Jenkins and check that jobs were created.
Click the ‘Build now’ button(s) for every job that created in the previous step.

That’s it!
