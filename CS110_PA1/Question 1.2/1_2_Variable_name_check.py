import shared_functions, random, math
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

# Framework version identifier
VERSION = 1.0

# Framework-style test function to check the value of a variable in student code
def test_passed(test_feedback):

    # -------------------------
    # Section to create the answer and inputs
    # -------------------------
    names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley"]
    name = random.choice(names)
    current_lap = random.randint(1,100)
    average_speed = round(random.random() * 100 + 50,2)
    answer = name
    test_inputs = [current_lap, name, average_speed]
    print(f"Test Inputs: {test_inputs}")
    check_var = "name"
    # -------------------------
    # End of section to create the answer and inputs
    # -------------------------

    test_passed = True

    try:
        sink = StringIO()
        with redirect_stdout(sink):
            # Patch input to simulate student input
            with patch("builtins.input", side_effect=test_inputs):
                # Import the student module fresh each time
                stu_main = shared_functions.fresh_import('main', test_feedback)

    except EOFError:
        # Handle case where student requests more inputs than provided
        test_feedback.write(f"There were more than the {len(test_inputs)} expected inputs.")
        return False
    except FileNotFoundError as e:
        # Handle missing student file
        test_feedback.write(f"{e.strerror}: {e.filename}")
        return False

    # Check that the variable exists and is of the correct type
    test_passed, feedback_msg = shared_functions.check_variable(check_var, stu_main, str)

    if not test_passed:
        # If variable check fails, write feedback and exit
        test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
        return test_passed
    else:
        stu_var = getattr(stu_main, check_var)

    # Compare the student's variable to the expected answer
    if stu_var == answer:
        feedback_msg += f"\tThe value ({answer}) stored in the variable '{check_var}' is correct"
    else:
        # Show a preview of the first few items if incorrect
        feedback_msg += f"\tThe variable '{check_var}' is {stu_var} and it should be {answer}"
        feedback_msg += f"\nHINT:\n\tCheck your input order"
        test_passed = False

    # Write final feedback
    test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
    return test_passed
