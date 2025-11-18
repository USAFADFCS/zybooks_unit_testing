#Functions to use for unit tests
import builtins
import sys, importlib, random, math, inspect, re
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from types import ModuleType

VERSION = 1.0
real_open = open

def fake_open(expected_file_name, file_name, redirect_file, expected_mode, mode = 'r'):
    if file_name == expected_file_name and expected_mode in mode:
        return real_open(redirect_file, expected_mode)
    else:
        return real_open(file_name, mode)
    
def fresh_import(module_name: str = 'main', feedback_file = None) -> ModuleType:
    try:
        if module_name in sys.modules:
            del sys.modules[module_name]
    except ValueError as e:
        if feedback_file:
            feedback_file.write(f"Check your input variable data types and conversions")
    except EOFError as e:
        if feedback_file:
            feedback_file.write(f"There are more inputs then expected")
    return importlib.import_module(module_name)

def dummy_input(prompt=None):
    return "0"

def check_function(name, program, *args):
    if not hasattr(program, name):
        return False, (f"The function '{name}' should exist, but it is not present in your program.")
    else:
        test_fun = getattr(program, name)
    
    if not callable(test_fun):
        return False, (f"The function '{name}' is not callable")
    
    sig = inspect.signature(test_fun)
    if len(sig.parameters) != len(args):
        return False, (f"The function '{name}' should take {len(args)} parameter(s), but it takes {len(sig.parameters)}.\n")

    return True, (f"The function '{name}' exists, has the correct number of parameters, and is callable\n")

def compare_lists(stu_list, expected_list, float_tol=1e-9, field_names=None):
    differences = []
    if len(stu_list) != len(expected_list):
        differences.append(f"The length of the your list ({len(stu_list)}) does not match the expected length ({len(expected_list)})")
        return False, differences

    for i, (rec_a, rec_b) in enumerate(zip(stu_list, expected_list)):
        try:
            iter(rec_a)
        except TypeError:
            rec_a = (rec_a,)
        try:
            iter(rec_b)
        except TypeError:
            rec_b = (rec_b,)
 
        if len(rec_a) != len(rec_b):
            differences.append(f"Record field count ({len(rec_a)}) does not match expected ({len(rec_b)})")
            continue

        for j, (a, b) in enumerate(zip(rec_a, rec_b)):
            # Determine field name for messages
            fname = None
            if field_names and j < len(field_names):
                fname = field_names[j]
            else:
                fname = f"Field {j}"
 
            # Try numeric comparison if both can be converted to float
            try:
                fa = float(a)
                fb = float(b)
                is_num = True
            except (TypeError, ValueError):
                is_num = False
 
            if is_num:
                if abs(fa - fb) > float_tol:
                    differences.append(f"Record did not match expected for field '{fname}'")
            else:
                sa = "" if a is None else str(a).strip().lower()
                sb = "" if b is None else str(b).strip().lower()
                if sa != sb:
                    differences.append(f"record did not match expected for field '{fname}'")
 
    return (len(differences) == 0), differences

def check_print(sink, expected_fstring, case_sensitive = False):
    if case_sensitive:
        if re.search(expected_fstring, sink):
            return True
    elif not case_sensitive:
        if re.search(expected_fstring, sink, re.IGNORECASE):
            return True
    return False   

def check_variable(name, program, var_type):
    if not hasattr(program, name):
        return False, (f"The variable '{name}' should exist, but it is not present in your program.")
    else:
        test_var = getattr(program, name)

    if type(test_var) != var_type:
        return False, (f"The variable '{name}' is a {type(test_var)} and should be a {var_type}")

    return True, (f"The variable '{name}' exists, and is the correct variable type\n")

def check_import(program, libary):
    return libary in sys.modules

REAL_OPEN = open  # keep the real open() reference

def make_mocked_open(target_file=None):
    accessed = False
    read_written = False

    def mocked_open(path, mode='r', *args, **kwargs):
        nonlocal accessed, read_written
        file_obj = REAL_OPEN(path, mode, *args, **kwargs)

        # Intercept writes to the target file
        if 'w' in mode and path == target_file:
            accessed = True

            class FileWrapper:
                def __init__(self, wrapped):
                    self._wrapped = wrapped

                def write(self, *a, **kw):
                    nonlocal read_written
                    read_written = True
                    return self._wrapped.write(*a, **kw)

                def __enter__(self):
                    self._wrapped = self._wrapped.__enter__()
                    return self

                def __exit__(self, exc_type, exc_val, exc_tb):
                    return self._wrapped.__exit__(exc_type, exc_val, exc_tb)

                def __getattr__(self, name):
                    return getattr(self._wrapped, name)

            return FileWrapper(file_obj)
        
        if 'r' in mode and path == target_file:
            accessed = True

            class FileWrapper:
                def __init__(self, wrapped):
                    self._wrapped = wrapped

                def read(self, *a, **kw):
                    nonlocal read_written
                    read_written = True
                    return self._wrapped.read(*a, **kw)

                def readline(self, *a, **kw):
                    nonlocal read_written
                    read_written = True
                    return self._wrapped.readline(*a, **kw)

                def readlines(self, *a, **kw):
                    nonlocal read_written
                    read_written = True
                    return self._wrapped.readlines(*a, **kw)

                def __iter__(self):
                    nonlocal read_written
                    read_written = True
                    return iter(self._wrapped)

                def __enter__(self):
                    self._wrapped = self._wrapped.__enter__()
                    return self

                def __exit__(self, exc_type, exc_val, exc_tb):
                    return self._wrapped.__exit__(exc_type, exc_val, exc_tb)

                def __getattr__(self, name):
                    return getattr(self._wrapped, name)

            # Return wrapped version so reads are tracked
            return FileWrapper(file_obj)

        return file_obj

    # Return both the mock and tracking functions
    def get_flags():
        return accessed, read_written

    return mocked_open, get_flags