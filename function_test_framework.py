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
    num_cadets = random.randint(2,10)
    test_inputs = [num_cadets]
    list1 = []

    for _ in range(num_cadets):
        first_name = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Cameron", "Jamie", "Avery", "Quinn"]
        last_name = ["Smith", "Johnson", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas"]
        name = random.choice(first_name) + ' ' + random.choice(last_name)
        time = round(random.uniform(5.0, 20.0),2)
        test_inputs.append(name)
        test_inputs.append(time)
        list1.append([name, time])
    print("Test inputs:",test_inputs[1:])

    def analyze_run_times(cadet_data):
        total_time = 0
        fastest_time = None
        fastest_cadet = ""

        for cadet in cadet_data:
            name, time = cadet
            total_time += time
            if fastest_time is None or time < fastest_time:
                fastest_time = time
                fastest_cadet = name

        average = round(total_time / len(cadet_data),2)

        faster_count = 0
        for cadet in cadet_data:
            if cadet[1] < average:
                faster_count += 1

        return [average, faster_count, fastest_cadet]
   
    answer = analyze_run_times(list1)
    check_fun = "analyze_run_times"
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
            
    test_passed, feedback_msg = shared_functions.check_function(check_fun, stu_main, test_inputs)

    if test_passed == False:
        test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
        return test_passed
    else:
        stu_fun = getattr(stu_main, check_fun)

    if stu_fun(list1) == answer:
        feedback_msg += f"\tThe return from '{check_fun}' was the expect value of '{answer}'"
    elif math.isclose(stu_fun(list1),answer, abs_tol=0.01):
        feedback_msg += f"\tThe return from '{check_fun}' was '{stu_fun(list1)}' instead of the expected '{answer}'"
        feedback_msg += f"\nHINT: Check that you rounded to 2 decimal places"
        test_passed = False
    else:
        feedback_msg += f"\tThe return from '{check_fun}' was '{stu_fun(list1)}' instead of the expected '{answer}'"
        feedback_msg += f"\nHINT: Check your return statement and math"
        test_passed = False

    test_feedback.write(f"RESULTS:\n\t{feedback_msg}")
    return test_passed