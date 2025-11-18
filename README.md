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
