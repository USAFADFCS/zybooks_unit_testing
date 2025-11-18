import shared_functions, random, math
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

# Update test_inputs as needed
# Update the fstring you are looking for in the output
# Update the patch "builtins.input" line
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

    players = [row for row in lines if row[1] == team]
    total_goals = sum(int(row[2]) for row in players)

    fstring = "\n".join(players) + "\n" + str(total_goals)
# Above is to create the answer and inputs

    try:
        sink = StringIO()
        with redirect_stdout(sink):
            # if you have test_inputs use side_effects = test_inputs
            # if you do not have any test_inputs use side_effects = shared_functions.dummy_input
            with patch("builtins.input", side_effect = shared_functions.dummy_input):
                stu_main = shared_functions.fresh_import('main', test_feedback)

    #except EOFError as e:
    #    test_feedback.write(f"There were more then the {len(test_inputs)} expected inputs.")
    #    return False
    except FileNotFoundError as e:
        test_feedback.write(f"{e.strerror}: {e.filename}")
        return False

    specific_string = shared_functions.check_print(sink.getvalue(), fstring, True)
    
    if specific_string:
        test_passed = True
        feedback_msg = f"The printed value of '{fstring}' was correct"
    else:
        test_passed = False
        feedback_msg = f"The printed value of '{fstring}' was not in you output"
        feedback_msg += f"\nHINT: Check your check your print statement"

    test_feedback.write(f"RESULTS: {feedback_msg}\n")
    return test_passed