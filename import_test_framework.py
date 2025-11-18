import shared_functions
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

# Update test_inputs as needed
# Update the fstring you are looking for in the output
# Update the patch "builtins.input" line
# Update the feedback messages as needed

def test_passed(test_feedback):
    import_name = "math"

    try:
        sink = StringIO()
        with redirect_stdout(sink):
            # if you have test_inputs use side_effects = test_inputs
            # if you do not have any test_inputs use side_effects = shared_functions.dummy_input
            with patch("builtins.input", side_effect = shared_functions.dummy_input):
                stu_main = shared_functions.fresh_import('main', test_feedback)

    #except EOFError as e:
        #test_feedback.write(f"There were more then the {len(test_inputs)} expected inputs.")
        #return False
    except FileNotFoundError as e:
        test_feedback.write(f"{e.strerror}: {e.filename}")
        return False
    
    if shared_functions.check_import(stu_main,import_name):
        test_feedback.write(f"RESULTS: The {import_name} module was imported.")
        return True
    else:
        test_feedback.write(f"RESULTS: The {import_name} module was not imported.")
        return False