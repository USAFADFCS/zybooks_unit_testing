import shared_functions, random, math
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

# Framework version identifier
VERSION = 1.0

# Framework-style test function to check if a specific file is opened and read by student code
def test_passed(test_feedback):

    # -------------------------
    # Section to generate test inputs
    # -------------------------
    read_write_file = "usafa_intramurals.csv"
    test_input = []

    with open(read_write_file, 'r') as f:
        contents = f.read().strip().split("\n")

    start = random.randint(1, len(contents) - 10)
    lines = [line.strip().split(',') for line in contents[start:start+10]]

    team = random.choice([row[1] for row in lines])
    test_input.append(team)
    # -------------------------
    # End of section to generate test inputs
    # -------------------------

    # Default test result
    test_passed = True

    # Create a mocked open function for the target file and track file access flags
    mocked, flags = shared_functions.make_mocked_open(read_write_file)

    try:
        sink = StringIO()
        with redirect_stdout(sink):
            # Patch input to provide controlled test inputs
            with patch("builtins.input", side_effect=test_input):
                # Patch open() to intercept and monitor file access
                with patch("builtins.open", side_effect=mocked):
                    stu_main = shared_functions.fresh_import('main', test_feedback)

    except EOFError as e:
        # Handle case where student program requests more inputs than provided
        test_feedback.write(f"There were more than the {len(test_input)} expected inputs.")
        return False
    except FileNotFoundError as e:
        # Handle missing student file
        test_feedback.write(f"{e.strerror}: {e.filename}")
        return False

    # Retrieve flags to determine if the file was accessed and read
    accessed, read_written = flags()

    # Provide feedback based on whether the student program opened the file
    if accessed:
        feedback_msg = f"\tThe read file ({read_write_file}) was opened\n"
    else:
        feedback_msg = f"\tThe read file ({read_write_file}) was not opened\n"
        feedback_msg += f"HINT: Check spelling and that you opened the file to read"
        test_passed = False

    # Provide feedback based on whether the file was actually read from
    if test_passed and read_written:
        feedback_msg += f"\tThe file was read from\n"
    elif test_passed and not read_written:
        feedback_msg += f"\tThe file was not read from\n"
        feedback_msg += f"HINT: Check that you read from the file"
        test_passed = False

    # Write feedback for the unit test
    test_feedback.write(f"RESULTS:\n{feedback_msg}")
    return test_passed
