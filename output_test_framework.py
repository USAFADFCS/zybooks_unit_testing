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
    read_write_file = "usafa_intramurals.csv"
    test_inputs = []

    with open(read_write_file, 'r') as f:
        contents = f.read().strip().split("\n")

    start = random.randint(1, len(contents) - 10)
    lines = [line.strip().split(',') for line in contents]

    team = random.choice([row[1] for row in lines])
    test_inputs.append(team)
    print("Test inputs:", test_inputs)

    players = [row for row in lines if row[1] == team]
    total_goals = sum(int(row[2]) for row in players)

    fstring = "\n".join(players) + "\n" + str(total_goals)
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
            with patch("builtins.input", side_effect=shared_functions.dummy_input):
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
        feedback_msg += f"\nHINT: Check your print statement"

    # Write feedback to the test_feedback object
    test_feedback.write(f"RESULTS: {feedback_msg}\n")
    return test_passed
