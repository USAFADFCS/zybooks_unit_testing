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
    names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley"]
    name = random.choice(names)
    current_lap = random.randint(1,100)
    average_speed = round(random.random() * 100 + 50,2)
    answer = name
    test_inputs = [current_lap, name, average_speed]
    print(f"Test Inputs: {test_inputs}")
    fstring = f"Average Speed (mph): {average_speed}"
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
    specific_string = shared_functions.check_print(sink.getvalue(), fstring, True)
    
    if specific_string:
        test_passed = True
        feedback_msg = f"The printed value of:\n\t'{fstring}'\nis in your output"
    else:
        test_passed = False
        feedback_msg = f"The printed value of\n\t'{fstring}'\nis not in your output"
        feedback_msg += f"\nHINT:\n\tMake sure each value is printed on its own line\n\tCheck spelling, capitalization, and spacing"
    # Write feedback to the test_feedback object
    test_feedback.write(f"RESULTS: {feedback_msg}\n")
    return test_passed