# -------------------------------
# Shared Utility Functions for Unit Tests
# -------------------------------

import builtins
import sys, importlib, random, math, inspect, re
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from types import ModuleType

# Framework version identifier
VERSION = 1.0
real_open = open   # Keep a reference to Python’s real open()

# ---------------------------------------------------------
# fake_open()
# Redirects specific file opens to a different file for testing
# ---------------------------------------------------------
def fake_open(expected_file_name, file_name, redirect_file, expected_mode, mode='r'):
    """
    If the student's code attempts to open the expected file in the correct mode,
    this function instead returns a handle to 'redirect_file'.  
    Otherwise, it behaves like normal open().
    """
    if file_name == expected_file_name and expected_mode in mode:
        return real_open(redirect_file, expected_mode)
    else:
        return real_open(file_name, mode)

# ---------------------------------------------------------
# fresh_import()
# Re-imports the student's module so tests run on a clean copy
# ---------------------------------------------------------
def fresh_import(module_name: str = 'main', feedback_file = None) -> ModuleType:
    """
    Deletes the imported module from memory (if it exists) and reloads it.
    Ensures a fresh environment for each test.
    """
    try:
        if module_name in sys.modules:
            del sys.modules[module_name]
    except ValueError:
        if feedback_file:
            feedback_file.write("Check your input variable data types and conversions")
    except EOFError:
        if feedback_file:
            feedback_file.write("There are more inputs than expected")
    
    return importlib.import_module(module_name)

# ---------------------------------------------------------
# dummy_input()
# Replacement for input() when testing
# ---------------------------------------------------------
def dummy_input(prompt=None):
    """ Always returns '0'. Useful when the program expects input but tests don't care. """
    return "0"

# ---------------------------------------------------------
# check_function()
# Validates function existence, parameter count, and callability
# ---------------------------------------------------------
def check_function(name, program, *args):
    """
    Ensures that:
    - The function exists
    - It is callable
    - It takes the correct number of parameters
    """
    if not hasattr(program, name):
        return False, f"The function '{name}' should exist, but it is not present in your program."
    
    test_fun = getattr(program, name)

    if not callable(test_fun):
        return False, f"The function '{name}' is not callable"

    # Verify parameter count
    sig = inspect.signature(test_fun)
    if len(sig.parameters) != len(args):
        return False, f"The function '{name}' should take {len(args)} parameter(s), but it takes {len(sig.parameters)}.\n"

    return True, f"The function '{name}' exists, has the correct number of parameters, and is callable\n"

# ---------------------------------------------------------
# compare_lists()
# Compares two structured lists (list of lists) with numeric tolerances
# ---------------------------------------------------------
def compare_lists(stu_list, expected_list, float_tol=1e-9, field_names=None):
    """
    Compares two lists of records. Handles:
    - Different lengths
    - Numeric comparisons with tolerance
    - String comparisons (case-insensitive)
    - Optional field names for better error messages
    """
    differences = []

    # Compare list sizes
    if len(stu_list) != len(expected_list):
        differences.append(
            f"The length of your list ({len(stu_list)}) does not match the expected length ({len(expected_list)})"
        )
        return False, differences

    # Compare each row
    for i, (rec_a, rec_b) in enumerate(zip(stu_list, expected_list)):

        # Ensure both are iterable
        rec_a = rec_a if hasattr(rec_a, "__iter__") else (rec_a,)
        rec_b = rec_b if hasattr(rec_b, "__iter__") else (rec_b,)

        if len(rec_a) != len(rec_b):
            differences.append(
                f"Record field count ({len(rec_a)}) does not match expected ({len(rec_b)})"
            )
            continue

        # Compare field-by-field
        for j, (a, b) in enumerate(zip(rec_a, rec_b)):

            fname = field_names[j] if field_names and j < len(field_names) else f"Field {j}"

            # Attempt numeric comparison
            try:
                fa, fb = float(a), float(b)
                if abs(fa - fb) > float_tol:
                    differences.append(f"Record did not match expected for numeric field '{fname}'")
                continue
            except (TypeError, ValueError):
                pass  # Not numeric, fall back to string compare

            # Compare strings (case-insensitive, strip whitespace)
            sa = "" if a is None else str(a).strip().lower()
            sb = "" if b is None else str(b).strip().lower()

            if sa != sb:
                differences.append(f"Record did not match expected for field '{fname}'")

    return (len(differences) == 0), differences

# ---------------------------------------------------------
# check_print()
# Searches captured print output using regex
# ---------------------------------------------------------
def check_print(sink, expected_fstring, case_sensitive=False):
    """
    Searches the captured output (sink) for the expected text.
    Can perform case-sensitive or case-insensitive match.
    """
    flags = 0 if case_sensitive else re.IGNORECASE
    return bool(re.search(expected_fstring, sink, flags))

# ---------------------------------------------------------
# check_variable()
# Verifies variable existence and type
# ---------------------------------------------------------
def check_variable(name, program, var_type):
    if not hasattr(program, name):
        return False, f"The variable '{name}' should exist, but it is not present."
    
    test_var = getattr(program, name)

    if type(test_var) != var_type:
        return False, f"The variable '{name}' is type {type(test_var)} but should be {var_type}"

    return True, f"The variable '{name}' exists and is the correct type\n"

# ---------------------------------------------------------
# check_import()
# Validates that the student imported a library
# ---------------------------------------------------------
def check_import(program, library):
    """ Checks whether a library appears in sys.modules. """
    return library in sys.modules

# ---------------------------------------------------------
# make_mocked_open()
# Creates a custom mock open() that tracks reads/writes to a specific file
# ---------------------------------------------------------
REAL_OPEN = open

def make_mocked_open(target_file=None):
    """
    Wraps open() and tracks:
    - whether the file was accessed
    - whether it was read/written

    Used to check whether the student opened the correct file.
    """

    accessed = False
    read_written = False

    def mocked_open(path, mode='r', *args, **kwargs):
        nonlocal accessed, read_written

        file_obj = REAL_OPEN(path, mode, *args, **kwargs)

        # --- Intercept write mode ---
        if 'w' in mode and path == target_file:
            accessed = True

            class FileWrapper:
                """ Wraps the file object and tracks writes. """

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

        # --- Intercept read mode ---
        if 'r' in mode and path == target_file:
            accessed = True

            class FileWrapper:
                """ Wraps the file object and tracks reads. """

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

            return FileWrapper(file_obj)

        # Normal open() for all other files
        return file_obj

    # Helper so tests can check the results
    def get_flags():
        """ Returns (accessed, read_or_written). """
        return accessed, read_written

    return mocked_open, get_flags
