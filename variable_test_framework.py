import shared_functions, random, math
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

# Update test_inputs as needed
# Update the answer you are expecting in the variable
# Update the variable name you are looking for
# Update the patch "builtins.input" line
# Update the variable type in the check_variable function
# Update the feedback messages as needed

def test_passed(test_feedback):
    test_passed = True

# Below is to create the answer and inputs
    read_write_file = "usafa_intramurals.csv"
    test_inputs = []
    with open(read_write_file, 'r') as f:
        contents = f.read().strip().split("\n")

    start = random.randint(1, len(contents) - 10)
    lines = [line.strip().split(',') for line in contents]

    team = random.choice([row[1] for row in lines])

    test_inputs.append(team)
    print("Test inputs:",test_inputs)

    answer = [row[0] for row in lines if row[1] == team]
    check_var = "team_players"
# Above is to create the answer and inputs

    try:
        sink = StringIO()
        with redirect_stdout(sink):
# if you have test_inputs use side_effects = test_inputs
# if you do not have any test_inputs use side_effects = shared_functions.dummy_input
            with patch("builtins.input", side_effect = test_inputs):
                stu_main = shared_functions.fresh_import('main', test_feedback)

    except EOFError as e:
        test_feedback.write(f"There were more then the {len(test_inputs)} expected inputs.")
        return False
    except FileNotFoundError as e:
        test_feedback.write(f"{e.strerror}: {e.filename}")
        return False

# Check the variable type (arguement 3)   
    test_passed, feedback_msg = shared_functions.check_variable(check_var, stu_main, list)

    if test_passed == False:
        test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
        return test_passed
    else:
        stu_var = getattr(stu_main, check_var)

    if stu_var == answer:
        feedback_msg += f"\tThe value stored in the variable '{check_var}' is correct"
    else:
        feedback_msg += f"\tThe variable '{check_var}' has {stu_var[0:4]} in the first 5 lines and it should be {answer[0:4]}"
        feedback_msg += f"\nHINT: Check that you saved the correct names in the variable"
        test_passed = False

    test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
    return test_passed