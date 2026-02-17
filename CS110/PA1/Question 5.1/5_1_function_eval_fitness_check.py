import shared_functions, random, math
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

# Framework version identifier
VERSION = 1.0

# Framework-style test function to check return value of the given function from student code
def test_passed(test_feedback):
    # -------------------------
    # SECTION: Generate answer and inputs
    # -------------------------
    def eval_fitness(run_time, pushups, situps):
        points = 0

        if run_time <= 12.5:
            points += 2
        elif run_time <= 13.5:
            points += 1
        else:
            return "Unsatisfactory"

        if pushups >= 50:
            points += 2
        elif pushups >= 30:
            points += 1
        else:
            return "Unsatisfactory"

        if situps >= 48:
            points += 2
        elif situps >= 39:
            points += 1
        else:
            return "Unsatisfactory"

        if points <= 4:
            return "Satisfactory"
        else:
            return "Excellent"
    
    check_fun = "eval_fitness"

    run1 = round(random.random() * (12.5-10) + 10, 2)
    pushups1 = random.randint(31,75)
    situps1 = random.randint(40,75)

    test_inputs1 = [run1, pushups1, situps1]
    print(f"Test Inputs: {test_inputs1}")

    answer1 = eval_fitness(run1, pushups1, situps1)
    
    run2 = round(random.random() * (13.5-12.6) + 12.6, 2)
    pushups2 = random.randint(30,49)
    situps2 = random.randint(39,47)

    test_inputs2 = [run2, pushups2, situps2]
    print(f"Test Inputs: {test_inputs2}")

    answer2 = eval_fitness(run2, pushups2, situps2)

    run3 = round(random.random() * (25-13.6) + 13.6, 2)
    pushups3 = random.randint(10,29)
    situps3 = random.randint(10,39)

    test_inputs3 = [run3, pushups3, situps3]
    print(f"Test Inputs: {test_inputs3}")

    answer3 = eval_fitness(run3, pushups3, situps3)

    answers = [answer1,answer2,answer3]
    test_input = [test_inputs1, test_inputs2, test_inputs3]
    # Above section is intended to be updated per specific test case

    # Initialize test result as True
    test_passed = True
    feedback_msg = "Running 3 tests...\n"
    for answer, test_inputs in zip(answers,test_input):
        # -------------------------
        # SECTION: Execute student's code with mocked input
        # -------------------------
        try:
            sink = StringIO()  # Capture stdout for analysis
            with redirect_stdout(sink):
                # Patch input() to provide controlled test inputs
                # Replace side_effect with either test_inputs or dummy_input as needed
                with patch("builtins.input", side_effect=test_inputs):
                    stu_main = shared_functions.fresh_import('main', test_feedback)
        
        except EOFError as e:
            test_feedback.write(f"There were more than the {len(test_inputs)} expected inputs.")
            return False
        
        except FileNotFoundError as e:
            test_feedback.write(f"{e.strerror}: {e.filename}")
            return False
                
        # -------------------------
        # SECTION: Verify student's function existence and signature
        # -------------------------
        test_passed, msg = shared_functions.check_function(check_fun, stu_main, *test_inputs)
        feedback_msg += f"\n\n{answer} check\n" + msg

        if not test_passed:
            test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
            return test_passed
        else:
            # Retrieve the student's function for further testing
            stu_fun = getattr(stu_main, check_fun)

        # -------------------------
        # SECTION: Compare student's output with expected answer
        # -------------------------
        if stu_fun(*test_inputs) == answer:
            feedback_msg += f"\tThe return from '{check_fun}' was the expected value '{answer}'\n"
        else:
            feedback_msg += f"\tThe return from '{check_fun}' was '{stu_fun(*test_inputs)}' instead of '{answer}'"
            feedback_msg += f"\nHINT: Check your return statement and math\n"
            test_passed = False

        if not test_passed:
            break
    # -------------------------
    # SECTION: Output final feedback
    # -------------------------
    test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
    return test_passed
