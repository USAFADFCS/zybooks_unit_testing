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
    def calc_fuel_needed(burn_rate,flight_time):
        total_fuel = round(burn_rate * flight_time,2)
        return total_fuel
    
    jet_burn_rate = random.random() * (250 - 50) + 50
    msn_time = random.random() * (10000 - 150) + 150
    fuel = jet_burn_rate*msn_time

    test_inputs = [jet_burn_rate, msn_time]
    print(f"Test Inputs: {test_inputs}")

    fstring = str(calc_fuel_needed(jet_burn_rate, msn_time))
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
        feedback_msg = f"The printed value of '{fstring}' was correct"
    else:
        test_passed = False
        feedback_msg = f"The printed value of '{fstring}' was not in your output"
        feedback_msg += f"\nHINT:\n\tCheck your math\n\tMake sure you rounded to 2 decimal places"
    # Write feedback to the test_feedback object
    test_feedback.write(f"RESULTS: {feedback_msg}\n")
    return test_passed
