import unittest
import os
import importlib
import sys
import io
import contextlib
from test.TestUtils import TestUtils

def safely_import_module(module_name):
    """Safely import a module, returning None if import fails."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None

def check_function_exists(module, function_name):
    """Check if a function exists in a module."""
    return hasattr(module, function_name) and callable(getattr(module, function_name))

def safely_call_function(module, function_name, *args, **kwargs):
    """Safely call a function, returning None if it fails."""
    if not check_function_exists(module, function_name):
        return None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return getattr(module, function_name)(*args, **kwargs)
    except Exception:
        return None

def safely_get_constant(module, constant_name):
    """Safely get a constant from a module, returning None if it doesn't exist."""
    try:
        return getattr(module, constant_name, None)
    except:
        return None

def load_module_dynamically():
    """Load the student's module for testing"""
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    return module_obj

class TestAssignment(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module = load_module_dynamically()

    def test_minimum_thresholds(self):
        """Test exact minimum threshold values across functions"""
        try:
            if self.module is None:
                self.test_obj.yakshaAssert("test_minimum_thresholds", False, "boundary")
                print("test_minimum_thresholds = Failed")
                return
            
            error_count = 0
            
            # Get constants safely
            MIN_SAFETY_SCORE = safely_get_constant(self.module, "MIN_SAFETY_SCORE")
            MAX_INCIDENTS = safely_get_constant(self.module, "MAX_INCIDENTS")
            MIN_TRAINING_SCORE = safely_get_constant(self.module, "MIN_TRAINING_SCORE")
            MIN_ATTENDANCE = safely_get_constant(self.module, "MIN_ATTENDANCE")
            
            if any(x is None for x in [MIN_SAFETY_SCORE, MAX_INCIDENTS, MIN_TRAINING_SCORE, MIN_ATTENDANCE]):
                error_count += 1
            else:
                # Test minimum values that should pass
                if check_function_exists(self.module, "check_basic_eligibility"):
                    basic_min = safely_call_function(self.module, "check_basic_eligibility", True, MIN_SAFETY_SCORE, 1, MAX_INCIDENTS)
                    if basic_min is None or basic_min != "Eligible":
                        error_count += 1
                else:
                    error_count += 1
                
                if check_function_exists(self.module, "check_machine_operator"):
                    machine_min = safely_call_function(self.module, "check_machine_operator", "Eligible", True, MIN_TRAINING_SCORE)
                    if machine_min is None or machine_min != "Eligible":
                        error_count += 1
                else:
                    error_count += 1
                
                if check_function_exists(self.module, "check_safety_supervisor"):
                    supervisor_min = safely_call_function(self.module, "check_safety_supervisor", "Eligible", True, MIN_ATTENDANCE)
                    if supervisor_min is None or supervisor_min != "Eligible":
                        error_count += 1
                else:
                    error_count += 1
                
                if check_function_exists(self.module, "check_night_shift"):
                    night_min = safely_call_function(self.module, "check_night_shift", "Eligible", True, False, 5)
                    if night_min is None or night_min != "Eligible":
                        error_count += 1
                else:
                    error_count += 1
                
                if check_function_exists(self.module, "check_trainer"):
                    trainer_min = safely_call_function(self.module, "check_trainer", "Eligible", 0, False)
                    if trainer_min is None or trainer_min != "Eligible":
                        error_count += 1
                else:
                    error_count += 1
                
                # Test values just below minimum that should fail
                if check_function_exists(self.module, "check_basic_eligibility"):
                    basic_below = safely_call_function(self.module, "check_basic_eligibility", True, MIN_SAFETY_SCORE - 1, 1, MAX_INCIDENTS)
                    if basic_below is None or basic_below != "Not Eligible":
                        error_count += 1
            
            if error_count > 0:
                self.test_obj.yakshaAssert("test_minimum_thresholds", False, "boundary")
                print("test_minimum_thresholds = Failed")
                return
            
            # Success case
            self.test_obj.yakshaAssert("test_minimum_thresholds", True, "boundary")
            print("test_minimum_thresholds = Passed")
            
        except Exception as e:
            self.test_obj.yakshaAssert("test_minimum_thresholds", False, "boundary")
            print("test_minimum_thresholds = Failed")

    def test_alternative_criteria(self):
        """Test boundary cases with alternative criteria"""
        try:
            if self.module is None:
                self.test_obj.yakshaAssert("test_alternative_criteria", False, "boundary")
                print("test_alternative_criteria = Failed")
                return
            
            error_count = 0
            
            # Get constants safely
            MIN_SAFETY_SCORE = safely_get_constant(self.module, "MIN_SAFETY_SCORE")
            MIN_EXPERIENCE = safely_get_constant(self.module, "MIN_EXPERIENCE")
            MAX_INCIDENTS = safely_get_constant(self.module, "MAX_INCIDENTS")
            
            if any(x is None for x in [MIN_SAFETY_SCORE, MIN_EXPERIENCE, MAX_INCIDENTS]):
                error_count += 1
            else:
                # Test alternative criteria cases
                if check_function_exists(self.module, "check_basic_eligibility"):
                    basic_alt = safely_call_function(self.module, "check_basic_eligibility", True, MIN_SAFETY_SCORE - 1, MIN_EXPERIENCE, MAX_INCIDENTS)
                    if basic_alt is None or basic_alt != "Eligible":
                        error_count += 1
                else:
                    error_count += 1
                
                if check_function_exists(self.module, "check_night_shift"):
                    night_alt = safely_call_function(self.module, "check_night_shift", "Eligible", True, True, 0)
                    if night_alt is None or night_alt != "Eligible":
                        error_count += 1
                else:
                    error_count += 1
                
                if check_function_exists(self.module, "check_trainer"):
                    trainer_alt = safely_call_function(self.module, "check_trainer", "Eligible", 10, True)
                    if trainer_alt is None or trainer_alt != "Eligible":
                        error_count += 1
                else:
                    error_count += 1
                
                # Test with failing eligibility from previous function
                if check_function_exists(self.module, "check_machine_operator"):
                    machine_fail = safely_call_function(self.module, "check_machine_operator", "Not Eligible", True, 100)
                    if machine_fail is None or machine_fail != "Not Eligible":
                        error_count += 1
                else:
                    error_count += 1
            
            if error_count > 0:
                self.test_obj.yakshaAssert("test_alternative_criteria", False, "boundary")
                print("test_alternative_criteria = Failed")
                return
            
            # Success case
            self.test_obj.yakshaAssert("test_alternative_criteria", True, "boundary")
            print("test_alternative_criteria = Passed")
            
        except Exception as e:
            self.test_obj.yakshaAssert("test_alternative_criteria", False, "boundary")
            print("test_alternative_criteria = Failed")

if __name__ == '__main__':
    unittest.main()