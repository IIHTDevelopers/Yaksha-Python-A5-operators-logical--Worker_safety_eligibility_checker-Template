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

def check_raises(func, args, expected_exception=Exception):
    """Check if a function raises an expected exception."""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            func(*args)
        return False
    except expected_exception:
        return True
    except Exception:
        return False

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

    def test_input_type_validations(self):
        """Test type validations across all functions"""
        try:
            if self.module is None:
                self.test_obj.yakshaAssert("test_input_type_validations", False, "exceptional")
                print("test_input_type_validations = Failed")
                return
            
            error_count = 0
            
            # Test boolean type validation for check_basic_eligibility
            if check_function_exists(self.module, "check_basic_eligibility"):
                func = getattr(self.module, "check_basic_eligibility")
                result = check_raises(func, ["yes", 80, 2, 1], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test boolean type validation for check_machine_operator
            if check_function_exists(self.module, "check_machine_operator"):
                func = getattr(self.module, "check_machine_operator")
                result = check_raises(func, ["Eligible", "yes", 80], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test boolean type validation for check_night_shift
            if check_function_exists(self.module, "check_night_shift"):
                func = getattr(self.module, "check_night_shift")
                result = check_raises(func, ["Eligible", True, "yes", 5], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test integer type validation for check_basic_eligibility
            if check_function_exists(self.module, "check_basic_eligibility"):
                func = getattr(self.module, "check_basic_eligibility")
                result = check_raises(func, [True, "80", 2, 1], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test integer type validation for check_safety_supervisor
            if check_function_exists(self.module, "check_safety_supervisor"):
                func = getattr(self.module, "check_safety_supervisor")
                result = check_raises(func, ["Eligible", True, "90"], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test integer type validation for check_trainer
            if check_function_exists(self.module, "check_trainer"):
                func = getattr(self.module, "check_trainer")
                result = check_raises(func, ["Eligible", "0", True], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test string type validation for check_machine_operator
            if check_function_exists(self.module, "check_machine_operator"):
                func = getattr(self.module, "check_machine_operator")
                result = check_raises(func, [True, True, 80], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test string format validation for check_safety_supervisor
            if check_function_exists(self.module, "check_safety_supervisor"):
                func = getattr(self.module, "check_safety_supervisor")
                result = check_raises(func, ["maybe", True, 90], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            if error_count > 0:
                self.test_obj.yakshaAssert("test_input_type_validations", False, "exceptional")
                print("test_input_type_validations = Failed")
                return
            
            # Success case
            self.test_obj.yakshaAssert("test_input_type_validations", True, "exceptional")
            print("test_input_type_validations = Passed")
            
        except Exception as e:
            self.test_obj.yakshaAssert("test_input_type_validations", False, "exceptional")
            print("test_input_type_validations = Failed")

    def test_range_validations(self):
        """Test value range validations across all functions"""
        try:
            if self.module is None:
                self.test_obj.yakshaAssert("test_range_validations", False, "exceptional")
                print("test_range_validations = Failed")
                return
            
            error_count = 0
            
            # Test negative score validation
            if check_function_exists(self.module, "check_basic_eligibility"):
                func = getattr(self.module, "check_basic_eligibility")
                result = check_raises(func, [True, -1, 2, 1], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test score over 100 validation
            if check_function_exists(self.module, "check_basic_eligibility"):
                func = getattr(self.module, "check_basic_eligibility")
                result = check_raises(func, [True, 101, 2, 1], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test training score over 100 validation
            if check_function_exists(self.module, "check_machine_operator"):
                func = getattr(self.module, "check_machine_operator")
                result = check_raises(func, ["Eligible", True, 101], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test attendance over 100 validation
            if check_function_exists(self.module, "check_safety_supervisor"):
                func = getattr(self.module, "check_safety_supervisor")
                result = check_raises(func, ["Eligible", True, 101], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test negative experience validation
            if check_function_exists(self.module, "check_basic_eligibility"):
                func = getattr(self.module, "check_basic_eligibility")
                result = check_raises(func, [True, 80, -1, 1], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test negative incidents validation
            if check_function_exists(self.module, "check_basic_eligibility"):
                func = getattr(self.module, "check_basic_eligibility")
                result = check_raises(func, [True, 80, 2, -1], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test negative night experience validation
            if check_function_exists(self.module, "check_night_shift"):
                func = getattr(self.module, "check_night_shift")
                result = check_raises(func, ["Eligible", True, True, -1], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test negative trainer incidents validation
            if check_function_exists(self.module, "check_trainer"):
                func = getattr(self.module, "check_trainer")
                result = check_raises(func, ["Eligible", -1, True], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            if error_count > 0:
                self.test_obj.yakshaAssert("test_range_validations", False, "exceptional")
                print("test_range_validations = Failed")
                return
            
            # Success case
            self.test_obj.yakshaAssert("test_range_validations", True, "exceptional")
            print("test_range_validations = Passed")
            
        except Exception as e:
            self.test_obj.yakshaAssert("test_range_validations", False, "exceptional")
            print("test_range_validations = Failed")

    def test_eligibility_string_format(self):
        """Test validation of eligibility string formats"""
        try:
            if self.module is None:
                self.test_obj.yakshaAssert("test_eligibility_string_format", False, "exceptional")
                print("test_eligibility_string_format = Failed")
                return
            
            error_count = 0
            
            # Test wrong case validation for check_machine_operator
            if check_function_exists(self.module, "check_machine_operator"):
                func = getattr(self.module, "check_machine_operator")
                result = check_raises(func, ["eligible", True, 80], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test wrong format validation for check_safety_supervisor
            if check_function_exists(self.module, "check_safety_supervisor"):
                func = getattr(self.module, "check_safety_supervisor")
                result = check_raises(func, ["YES", True, 90], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test wrong format validation for check_night_shift
            if check_function_exists(self.module, "check_night_shift"):
                func = getattr(self.module, "check_night_shift")
                result = check_raises(func, ["no", True, True, 5], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            # Test invalid value validation for check_trainer
            if check_function_exists(self.module, "check_trainer"):
                func = getattr(self.module, "check_trainer")
                result = check_raises(func, ["Possibly", 0, True], ValueError)
                if not result:
                    error_count += 1
            else:
                error_count += 1
            
            if error_count > 0:
                self.test_obj.yakshaAssert("test_eligibility_string_format", False, "exceptional")
                print("test_eligibility_string_format = Failed")
                return
            
            # Success case
            self.test_obj.yakshaAssert("test_eligibility_string_format", True, "exceptional")
            print("test_eligibility_string_format = Passed")
            
        except Exception as e:
            self.test_obj.yakshaAssert("test_eligibility_string_format", False, "exceptional")
            print("test_eligibility_string_format = Failed")

if __name__ == '__main__':
    unittest.main()