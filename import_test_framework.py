import shared_functions
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

# Framework version identifier
VERSION = 1.0

# This function tests whether a specific module is imported in the student's program
# The 'import_name' can be changed per test scenario.
def test_passed(test_feedback):
    import_name = "math"  # Module we want to check for

    try:
        # Capture all printed output from the student's program
        sink = StringIO()
        with redirect_stdout(sink):
            # Patch input to provide dummy responses or controlled test inputs
            # Here, we use a generic dummy input function
            with patch("builtins.input", side_effect=shared_functions.dummy_input):
                # Freshly import the student's main module
                stu_main = shared_functions.fresh_import('main', test_feedback)

    # Handle cases where the student's file is missing
    except FileNotFoundError as e:
        test_feedback.write(f"{e.strerror}: {e.filename}")
        return False
    
    # -------------------------
    # Check if the student's module imported the expected library
    # -------------------------
    if shared_functions.check_import(stu_main, import_name):
        test_feedback.write(f"RESULTS: The {import_name} module was imported.")
        return True
    else:
        test_feedback.write(f"RESULTS: The {import_name} module was not imported.")
        return False
