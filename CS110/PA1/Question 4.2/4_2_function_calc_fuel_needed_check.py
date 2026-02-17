import shared_functions, random, math
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

# Framework version identifier
VERSION = 1.0

# Framework-style test function to check return value of the given function from student code
def test_passed(test_feedback):
    # -------------------------
    # SECTION: Generate answer and inputs
    # -------------------------
    def calc_fuel_needed(burn_rate,flight_time):
        total_fuel = round(burn_rate * flight_time,2)
        return total_fuel
    
    jet_burn_rate = random.random() * (250 - 50) + 50
    msn_time = random.random() * (10000 - 150) + 150

    test_inputs = [jet_burn_rate, msn_time]
    print(f"Test Inputs: {test_inputs}")

    answer = calc_fuel_needed(jet_burn_rate, msn_time)
    check_fun = "calc_fuel_needed"

    # Above section is intended to be updated per specific test case

    # Initialize test result as True
    test_passed = True

    # -------------------------
    # SECTION: Execute student's code with mocked input
    # -------------------------
    try:
        sink = StringIO()  # Capture stdout for analysis
        with redirect_stdout(sink):
            # Patch input() to provide controlled test inputs
            # Replace side_effect with either test_inputs or dummy_input as needed
            with patch("builtins.input", side_effect=test_inputs):
                stu_main = shared_functions.fresh_import('main', test_feedback)
    
    except EOFError as e:
        test_feedback.write(f"There were more than the {len(test_inputs)} expected inputs.")
        return False
    
    except FileNotFoundError as e:
        test_feedback.write(f"{e.strerror}: {e.filename}")
        return False
            
    # -------------------------
    # SECTION: Verify student's function existence and signature
    # -------------------------
    test_passed, feedback_msg = shared_functions.check_function(check_fun, stu_main, *test_inputs)

    if not test_passed:
        test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
        return test_passed
    else:
        # Retrieve the student's function for further testing
        stu_fun = getattr(stu_main, check_fun)

    # -------------------------
    # SECTION: Compare student's output with expected answer
    # -------------------------
    if stu_fun(jet_burn_rate, msn_time) == answer:
        feedback_msg += f"\tThe return from '{check_fun}' was the expected value '{answer}'"
    elif math.isclose(stu_fun(jet_burn_rate, msn_time), answer, abs_tol=0.01):
        feedback_msg += f"\tThe return from '{check_fun}' was '{stu_fun(jet_burn_rate, msn_time)}' instead of '{answer}'"
        feedback_msg += f"\nHINT: Check that you rounded to 2 decimal places"
        test_passed = False
    else:
        feedback_msg += f"\tThe return from '{check_fun}' was '{stu_fun(jet_burn_rate, msn_time)}' instead of '{answer}'"
        feedback_msg += f"\nHINT: Check your return statement and math"
        test_passed = False

    # -------------------------
    # SECTION: Output final feedback
    # -------------------------
    test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
    return test_passed
