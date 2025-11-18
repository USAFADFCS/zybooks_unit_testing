import shared_functions, random, math
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

# Update test_inputs as needed
# Update the answer you are expecting returned
# Update the function name you are looking for
# Update the patch "builtins.input" line
# Update the feedback messages as needed

def test_passed(test_feedback):
    test_passed = True

# Below is to create the answer and inputs

    read_write_file = "usafa_intramurals.csv"
    test_input = []
    with open(read_write_file, 'r') as f:
        contents = f.read().strip().split("\n")

    start = random.randint(1, len(contents) - 10)
    lines = [line.strip().split(',') for line in contents[start:start+10]]

    team = random.choice([row[1] for row in lines])

    test_input.append(team)

# Above is to create the answer and inputs

    mocked, flags = shared_functions.make_mocked_open(read_write_file)

    try:
        sink = StringIO()
        with redirect_stdout(sink):
# if you have test_inputs use side_effects = test_inputs
# if you do not have any test_inputs use side_effects = shared_functions.dummy_input
            with patch("builtins.input", side_effect = test_input):
                with patch("builtins.open", side_effect = mocked):
                    stu_main = shared_functions.fresh_import('main', test_feedback)
    
    except EOFError as e:
        test_feedback.write(f"There were more then the {len(test_input)} expected inputs.")
        return False
    except FileNotFoundError as e:
        test_feedback.write(f"{e.strerror}: {e.filename}")
        return False
    
    accessed, read_written = flags()

    if accessed:
        feedback_msg = f"\tThe read file ({read_write_file}) was opened\n"
    else:
        feedback_msg = f"\tThe read file ({read_write_file}) was not opened\n"
        feedback_msg += f"HINT: Check spelling and that you opened the file to read"
        test_passed = False

    if test_passed and read_written:
        feedback_msg += f"\tThe file was read from\n"
    elif test_passed and not read_written:
        feedback_msg += f"\tThe file was not read from\n"
        feedback_msg += f"HINT: Check that you read from the file"
        test_passed = False
    
    test_feedback.write(f"RESULTS:\n{feedback_msg}")
    return test_passed