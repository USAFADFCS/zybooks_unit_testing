import shared_functions, random, math
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

# Framework version identifier
VERSION = 1.0

# Framework-style test function to check printed output from student code
def test_passed(test_feedback):
    # -------------------------
    # Section to generate test inputs and expected output
    # -------------------------
    types = ["Visitor", "Employee", "Manager"]
    account_type = types[0]
    active_list = ["Cleared", "Not Cleared"]
    active = active_list[0]
    test_inputs = [account_type, active]
    print(f"Test Inputs: {test_inputs}")
    alt_fstrings = ["Temporary Access", "No Access", "Standard Access", "Access Suspended", "Full Access", "Security Review Required"]
    fstring = alt_fstrings[0]
    # -------------------------
    # End of section to generate test inputs and expected output
    # -------------------------

    test_passed = True  # Default test result

    # -------------------------
    # Run the student program and capture printed output
    # -------------------------
    try:
        sink = StringIO()
        with redirect_stdout(sink):
            # Patch input calls in the student program to return dummy values
            # or controlled test inputs if needed
            with patch("builtins.input", side_effect=test_inputs):
                stu_main = shared_functions.fresh_import('main', test_feedback)

    except FileNotFoundError as e:
        # Student file missing
        test_feedback.write(f"{e.strerror}: {e.filename}")
        return False

    # -------------------------
    # Compare captured output to expected output
    # -------------------------
    other_string = False
    for string in alt_fstrings:
        if string == fstring:
            specific_string = shared_functions.check_print(sink.getvalue(), fstring, True)
        else:
            if other_string:
                continue
            else:
                other_string = shared_functions.check_print(sink.getvalue(), string, True)
    
    if specific_string and (not other_string):
        test_passed = True
        feedback_msg = f"The printed value of '{fstring}' was correct"
    elif specific_string and other_string:
        test_passed = False
        feedback_msg = f"Only one result should be printed multipule were present"
    else:
        test_passed = False
        feedback_msg = f"The printed value of '{fstring}' was not in your output"
        feedback_msg += f"\nHINT:\n\tCheck conditional logic.\n\tCheck Spelling and Capitalization"
    # Write feedback to the test_feedback object
    test_feedback.write(f"RESULTS: {feedback_msg}\n")
    return test_passed