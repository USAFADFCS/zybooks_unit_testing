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

    write_file = "career_choices.csv"
    test_input = []

    afsc_reasons = {
        "11X": "Love of flying and leading operational missions.",
        "12X": "Enjoys navigation and mission coordination.",
        "13S": "Interested in space and satellite operations.",
        "14N": "Enjoys analysis and intelligence gathering.",
        "17X": "Fascinated by cybersecurity and digital warfare.",
        "62E": "Wants to design and develop new aerospace technologies.",
        "63A": "Interested in project management and acquisitions.",
        "21R": "Passionate about logistics and mission readiness.",
        "32E": "Enjoys civil engineering and base construction projects.",
        "36P": "Wants to support and develop Airmen through personnel management.",
        "38P": "Interested in leadership, event planning, and morale operations.",
        "65F": "Strong in finance and resource management.",
        "35P": "Enjoys public speaking and storytelling for the Air Force.",
        "13L": "Wants to integrate airpower with ground operations.",
        "18X": "Seeks elite-level physical and mental challenge.",
        "15A": "Loves data analysis and optimizing mission performance."
    }

    for _ in range(5):
        afsc, reason = random.choice(list(afsc_reasons.items()))
        test_input.append(afsc)
        test_input.append(reason)

    expected = "\n".join(f"{test_input[i]}, {test_input[i+1]}" for i in range(0, len(test_input), 2))
# Above is to create the answer and inputs

    mocked, flags = shared_functions.make_mocked_open(write_file)

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
    
    accessed, written = flags()

    if accessed:
        feedback_msg = f"\tThe write file ({write_file}) was opened\n"
    else:
        feedback_msg = f"\tThe write file ({write_file}) was not opened\n"
        feedback_msg += f"HINT: Check spelling and that you opened the file to write"
        test_passed = False

    if test_passed and written:
        feedback_msg += f"\tThe file was written to\n"
    elif test_passed and not written:
        feedback_msg += f"\tThe file was not written to\n"
        feedback_msg += f"HINT: Check that you wrote to the file"
        test_passed = False

    if test_passed:
        with open("cadet_preferences.csv", "r") as f:
            file_contents = f.read().strip()
        if file_contents == expected.strip():
            feedback_msg += f"\tThe file contents match the expected values\n"
            feedback_msg += "FILE CONTENTS:" + expected
        else:
            feedback_msg += f"\tThe file contents did not match"
            feedback_msg += "EXPECTED CONTENTS: " + expected
            feedback_msg += "YOUR FILE: " + file_contents
            test_passed = False
    
    test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
    return test_passed