---
title: "Chapter 1 - The First Test Case"
source: "https://testautomationu.applitools.com/pytest-tutorial/chapter1.html"
author:
published:
created: 2026-03-22
description: "Become a test automation superstar! 🌟"
tags:
  - "clippings"
---
Welcome to Chapter 1 for intro to pytest.

This first chapter will be mostly setup stuff. We will:

1. Install the latest version of Python
2. Install pytest
3. Create a new Python project for testing
4. Write our first test case

Get your laptops ready, because we’re about to start coding!

The first thing we need to do is make sure Python is installed on our local machine. It might already be there, even if you’ve never used Python before. To check, execute the following command in a terminal:

  
```
python --version
```
  

You should see the proper version printed. If the Python command doesn't work or doesn't print the expected version number, then try using `python3` instead:

  
```
python3 --version
```
  

If that still doesn’t work, then you need to install Python.

You can download the latest version of Python from [python.org](https://www.python.org/). After installing Python, retry the version commands I just showed to make sure Python is available from the command line. If that doesn’t work, then you may need to add Python to your system path.

With Python installed, let's talk about pytest.

pytest is what I call a “core test framework.” It is a Python package that lets programmers write test cases as functions. It also executes those tests and then reports results. In that sense, pytest is similar to other test frameworks like Java's JUnit, C#’s NUnit, and JavaScript's Mocha. However, it has very cool distinctives that we'll cover later in this course. There’s nothing quite like it.

Here, I'm showing pytest's website at pytest.org. Anytime you get stuck with pytest, try reading the docs. I've always found them to be helpful.

Now, let's install pytest. pytest is *not* part of the Python Standard Library. It is an open source project that is distributed as a third-party package. You will need to install it explicitly.

Here’s the command for installing pytest:

  
```
pip install pytest
```
  

pip is the standard package installer for Python. If you need to use the `python3` command to run Python, then you might also need to use the `pip3` command in lieu of `pip`.

Now, as you can see here, pip installed the pytest package, in addition to a few other dependencies. Everything from this output looks good to go.

NOTE

Using pip will install packages globally for the whole machine. However, it's typically a best practice to manage dependencies per project using virtual environments. There are several tools and methods for managing virtual environments. I won't use them in my examples in this course just to keep things simple, but I recommend trying to use them on your own. The example project's README includes some pointers about virtual environments.

With Python and pytest installed, let's create our first test project. Create a project directory by running the following command:

  
```
mkdir tau-intro-to-pytest
```
  

Then, change into that directory by running `cd` and the directory name:

  
```
cd tau-intro-to-pytest/
```
  

Inside the project directory, create a new directory named `tests`.

  
```
mkdir tests
```
  

The `tests` directory will contain all the test cases we will write. pytest does not *require* a directory named "tests" per se, but most Python projects use it as a conventional way to separate product code from test code.

I'd also like to mention one more thing about project structure. For this course, we will create a new project for our test cases. However, when you write new test cases on your own, you might want to add them to an existing project rather than creating an entirely new project. For example, unit tests should almost always be added to the same project as the product code they cover. As another example, end-to-end tests might be best located in their own separate project if the application they cover is split into several repositories. Please consider what is best for your team's needs.

Now that we have our project, let's create our first test case module.

For this course, I will use Visual Studio Code as my editor. I like using VS Code for Python because Microsoft publishes a very good Python extension, and I find that VS Code has a good balance between features, speed, and simplicity. JetBrains PyCharm is another excellent Python editor that I can recommend.

Create a file named `test_math.py` under the tests directory. Python source code files use the ".py" extension. We call Python files "modules" because they contain code that can be executed directly or imported by other files.

Inside this module, create a new function named `test_one_plus_one`:

  
```python
def test_one_plus_one():
  assert 1 + 1 == 2
```
  

This function is a complete pytest test case. pytest is unique amongst test frameworks because its test cases are written as functions. Other frameworks like Python's unittest, Java's JUnit, and C#'s NUnit structure test cases as classes. Functions are simpler and more concise. In Python, there’s a popular saying: “Simple is better than complex.”

Naming conventions are important to pytest. Notice that both our test module and our test function contain the prefix "test\_". When pytest runs, it will discover tests from its current directory down. By default, any function names with the prefix "test\_" in any modules with the prefix "test\_" will be identified and executed as test cases. You can override these settings using pytest config files, but I recommend sticking with convention. Note that you may also put non-test functions inside test modules.

Finally, notice the one-line body. Our test case simply verifies the basic math operation of addition. To perform assertions, pytest uses Python's native `assert` statement. There's no special assertion API or library. The assert statement simply evaluates a boolean condition and raises an exception of type `AssertionError` if the condition is false.

Let's run this test. Clearly, one plus one does indeed equal two, so our test should pass. For this course, I will run test cases from the command line. The command line is the most universal way to run tests. pytest also has a rich set of command line options, many of which we will learn in future chapters. You can also run tests directly from editors and IDEs, but they require extra configuration.

To run tests from the command line, enter the following command from the project's root directory. This invocation will find and execute all test cases within the project.

  
```
python -m pytest
```
  

NOTE

You can also run tests using the shorter `pytest` command. However, I recommend always using `python -m pytest`. The lengthier command automatically adds the current directory to `sys.path` so that all modules in the project can be discovered.

  

When you enter the command to execute the tests, you will see pytest print a banner, list test modules as they run, print a "." for each passing test case, and then conclude with the test results summary. In our case, you should see that our one test passed. Nice! It should run very quickly, too.

Now, you should be ready to roll! You should have Python installed with your initial test project.

If for some reason the test case fails when you try to run it, double-check your code and your setup. You can always refer to the example repository to make sure your code is correct. Make sure everything is working before proceeding to the next chapter.

  
  

## Resources

- [GitHub repository branch for Chapter 1](https://github.com/AutomationPanda/tau-intro-to-pytest/tree/chapter/01-first-test)
- [Python.org](https://www.python.org/)
- [pytest documentation](https://pytest.org/)
- [Python virtual environments](https://realpython.com/python-virtual-environments-a-primer/)
- [Python in Visual Studio Code](https://code.visualstudio.com/docs/languages/python)
- [JetBrains PyCharm](https://www.jetbrains.com/pycharm/)

  
  

## Quiz: +100 credits

Please Note: You must enroll to take the quiz and earn credits and badges!

## 1\. What command prints the current Python version?

## 2\. Conventionally, tests in a Python project belong under a directory named "tests".

## 3\. What command does pytest used for making assertions?

## 4\. What is the best command for running pytest tests?

## 5\. pytest treats all functions in modules under the "tests" directory as test cases.