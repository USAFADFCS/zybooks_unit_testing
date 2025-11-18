import shared_functions, random, math
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

# Framework version identifier
VERSION = 1.0

# Unit test function to check file writing functionality
def test_passed(test_feedback):
    test_passed = True

    # -------------------------
    # Section to create the answer and inputs
    # -------------------------
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
    # -------------------------
    # End of section to create the answer and inputs
    # -------------------------

    # Use a mocked open to intercept file operations and track if they happen
    mocked, flags = shared_functions.make_mocked_open(write_file)

    try:
        sink = StringIO()
        with redirect_stdout(sink):
            # Patch input and open to simulate the student's program execution
            with patch("builtins.input", side_effect=test_input):
                with patch("builtins.open", side_effect=mocked):
                    stu_main = shared_functions.fresh_import('main', test_feedback)

    except EOFError:
        # Student requested more inputs than were provided
        test_feedback.write(f"There were more than the {len(test_input)} expected inputs.")
        return False
    except FileNotFoundError as e:
        # Student file does not exist
        test_feedback.write(f"{e.strerror}: {e.filename}")
        return False

    # Check if the file was accessed and written to
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

    # If the file was written, compare the contents to the expected output
    if test_passed:
        with open("cadet_preferences.csv", "r") as f:
            file_contents = f.read().strip()
        # Normalize spacing between commas for comparison
        if file_contents.replace(", ", ",") == expected.strip().replace(", ", ","):
            feedback_msg += f"\tThe file contents match the expected values\n"
            feedback_msg += "FILE CONTENTS:" + expected
        else:
            feedback_msg += f"\tThe file contents did not match"
            feedback_msg += "EXPECTED CONTENTS: " + expected
            feedback_msg += "YOUR FILE: " + file_contents
            test_passed = False

    # Write feedback to the provided feedback object
    test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
    return test_passed
