# Python Unit Test Framework for Zybooks

This framework provides reusable tools and templates to create automated unit tests for Python programs, particularly for use in Zybooks exercises. It is designed to check user input, variable values, function outputs, file reads/writes, and module imports without modifying student code.

---

## Features

- **Mocked Inputs**: Simulate user input using `unittest.mock.patch`.
- **Capture Output**: Capture printed output using `StringIO` and `redirect_stdout`.
- **File Interception**: Track and verify file reads/writes using `make_mocked_open`.
- **Function Checks**: Verify that functions exist, have the correct signature, and return expected values.
- **Variable Checks**: Verify that variables exist and have the correct type and value.
- **Module Import Checks**: Confirm that required modules (e.g., `math`) are imported.
- **Customizable Test Templates**: Easily adapt tests for different exercises by changing the "answer/input" section.

---

## Shared functions

- **fake_open(expected_file_name, file_name, redirect_file, expected_mode, mode='r')** Redirects specific file opens to a different file for testing.
- **fresh_import(module_name: str = 'main', feedback_file = None) -> ModuleType:** Re-imports the student's module so tests run on a clean copy
- **dummy_input(prompt=None)** Replacement for input() when testing
- **check_function(name, program, \*args)** Validates function existence, parameter count, and callability
- **compare_lists(stu_list, expected_list, float_tol=1e-9, field_names=None)** Compares two structured lists (list of lists) with numeric tolerances
- **check_print(sink, expected_fstring, case_sensitive=False)** Searches captured print output using regex
- **check_variable(name, program, var_type)** Verifies variable existence and type
