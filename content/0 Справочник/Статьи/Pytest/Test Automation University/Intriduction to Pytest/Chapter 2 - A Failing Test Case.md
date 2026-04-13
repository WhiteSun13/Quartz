---
title: "Chapter 2 - A Failing Test Case"
source: "https://testautomationu.applitools.com/pytest-tutorial/chapter2.html"
author:
published:
created: 2026-03-22
description: "Become a test automation superstar! 🌟"
tags:
  - "clippings"
---
In the previous chapter, we created a Python project with pytest, wrote our first test, and ran it. If everything was set up correctly, then the test should have passed without any issues.

Now, that’s the happy path. In this chapter, let’s do something devious. Let’s deliberately cause a test to fail so we can learn how pytest handles failures.

Go back to the `test_math.py` module. Add a new Python test function named `test_one_plus_two` and implement it as follows:

  
```python
def test_one_plus_two():
  a = 1
  b = 2
  c = 0
  assert a + b == c
```
  

Clearly, one plus two does not equal zero. This test case should fail when we run it. You might be wondering why we are writing this test case to use variables instead of simply writing `assert 1 + 2 == 0`. You will see why in just a moment.

Run the new test. pytest will discover and run both test cases, and then both will run very quickly.

  
```
python -m pytest
```
  

Notice how the output prints a "." for the previous test that passes and an "F" for the new test that fails. pytest also dumps a code snippet for each failing test at the point of failure.

Take a closer look at the line identified as the failure, `assert a + b == c`.

Immediately beneath it, pytest prints another line that shows the values of each variable used in the assertion. This feature is called *[assertion introspection](https://docs.pytest.org/en/latest/how-to/assert.html#assert-details)*. It is very helpful when trying to figure out why tests fail because you don't need to re-run the test with debugging to see the variables' values.

Under the failing line, pytest will also print the type of exception that caused the test to fail, which in this case is `AssertionError`. When a test fails due to a failed assertion, the exception will be an `AssertionError`. However, tests will fail for \_any \_unhandled exception type. For example, if a test tries to access the ninth index in a list of only five elements, then the exception will be an index error instead of an assertion error. Pay attention to the exception types to help determine if test failures are due to legitimate defects or automation bugs.

At the bottom of the report, pytest lists the paths and names of each failing test with their failures. It then concludes by printing the test result totals. pytest's basic test report is both concise and helpful.

Failing tests are bad, so let's go back and fix that.

  
```python
def test_one_plus_two():
  a = 1
  b = 2
  c = 3
  assert a + b == c
```
  

Change `c = 0` to `c = 3`, then re-run the tests. pytest should now report two passing tests. Nice.

If you'd like to learn more about how pytest handles assertions, check out the page, [How to write and report assertions in tests](https://docs.pytest.org/en/stable/assert.html), on pytest.org.

pytest handles failures gracefully, just as we would expect for any resilient test framework. Its assertion introspection is a very helpful feature for determining *why* something failed, not merely *what* failed. It works for any kind of test case, not just the simple arithmetic tests we covered in this chapter.

In the next chapter, we’ll learn how to test for expected exceptions.

  
  

## Resources

- [GitHub repository branch for Chapter 2](https://github.com/AutomationPanda/tau-intro-to-pytest/tree/chapter/02-failing-test)
- [How to write and report assertions in tests](https://docs.pytest.org/en/stable/assert.html)
- [Assertion introspection](https://docs.pytest.org/en/latest/how-to/assert.html#assert-details)

  
  

## Quiz: +100 credits

Please Note: You must enroll to take the quiz and earn credits and badges!

## 1\. One Python test module can contain more than one test case function.

## 2\. What symbol does pytest use in its reports to denote a passing test?

## 3\. What symbol does pytest use in its reports to denote a failing test?

## 4\. What types of exceptions will make a pytest test case fail?

## 5\. By default, pytest will print test code snippets, failure reasons, and test result tallies for failed test cases.