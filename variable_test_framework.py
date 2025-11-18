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
    read_write_file = "usafa_intramurals.csv"
    test_inputs = []

    with open(read_write_file, 'r') as f:
        contents = f.read().strip().split("\n")

    start = random.randint(1, len(contents) - 10)
    lines = [line.strip().split(',') for line in contents]

    team = random.choice([row[1] for row in lines])
    test_inputs.append(team)
    print("Test inputs:", test_inputs)

    answer = [row[0] for row in lines if row[1] == team]
    check_var = "team_players"
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
    test_passed, feedback_msg = shared_functions.check_variable(check_var, stu_main, list)

    if not test_passed:
        # If variable check fails, write feedback and exit
        test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
        return test_passed
    else:
        stu_var = getattr(stu_main, check_var)

    # Compare the student's variable to the expected answer
    if stu_var == answer:
        feedback_msg += f"\tThe value stored in the variable '{check_var}' is correct"
    else:
        # Show a preview of the first few items if incorrect
        feedback_msg += f"\tThe variable '{check_var}' has {stu_var[0:4]} in the first 5 lines and it should be {answer[0:4]}"
        feedback_msg += f"\nHINT: Check that you saved the correct names in the variable"
        test_passed = False

    # Write final feedback
    test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
    return test_passed
