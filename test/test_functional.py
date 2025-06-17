import unittest
import os
import importlib
import sys
import io
import contextlib
import inspect
import re
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

def check_file_exists(filename):
    """Check if a file exists in the current directory."""
    return os.path.exists(filename)

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

    def test_required_variables(self):
        """Test if required variables are correctly defined"""
        try:
            # Check if file exists
            if not check_file_exists('skeleton.py'):
                self.test_obj.yakshaAssert("test_required_variables", False, "functional")
                print("test_required_variables = Failed")
                return
            
            with open('skeleton.py', 'r') as file:
                content = file.read()
            
            # Critical calculation variables to check
            logical_vars = {
                'has_required_performance': r'has_required_performance\s*=.*safety_score.*or.*experience',
                'has_safe_record': r'has_safe_record\s*=.*incidents',
                'has_sufficient_training': r'has_sufficient_training\s*=.*training_score',
                'has_good_attendance': r'has_good_attendance\s*=.*attendance',
                'is_qualified': r'is_qualified\s*=.*team_leader.*or.*experience',
                'has_trainer_qualification': r'has_trainer_qualification\s*=.*incidents.*or.*team_leader'
            }
            
            # Check main result variable assignments
            result_vars = {
                'basic_eligible': r'basic_eligible\s*=\s*check_basic_eligibility',
                'machine_eligible': r'machine_eligible\s*=\s*check_machine_operator',
                'supervisor_eligible': r'supervisor_eligible\s*=\s*check_safety_supervisor',
                'night_eligible': r'night_eligible\s*=\s*check_night_shift',
                'trainer_eligible': r'trainer_eligible\s*=\s*check_trainer'
            }
            
            # Check for missing variables (but be lenient about exact patterns)
            error_count = 0
            for var_set in [logical_vars, result_vars]:
                for var_name, pattern in var_set.items():
                    if not re.search(pattern, content, re.IGNORECASE):
                        error_count += 1
            
            if error_count > 0:
                self.test_obj.yakshaAssert("test_required_variables", False, "functional")
                print("test_required_variables = Failed")
                return
            
            # Success case
            self.test_obj.yakshaAssert("test_required_variables", True, "functional")
            print("test_required_variables = Passed")
            
        except Exception as e:
            self.test_obj.yakshaAssert("test_required_variables", False, "functional")
            print("test_required_variables = Failed")

    def test_logical_operators_usage(self):
        """Test if required logical operators are used in functions"""
        try:
            if self.module is None:
                self.test_obj.yakshaAssert("test_logical_operators_usage", False, "functional")
                print("test_logical_operators_usage = Failed")
                return
            
            error_count = 0
            
            # Check basic eligibility (needs AND, OR)
            if check_function_exists(self.module, "check_basic_eligibility"):
                try:
                    basic_code = inspect.getsource(getattr(self.module, "check_basic_eligibility"))
                    has_and_basic = " and " in basic_code.lower()
                    has_or_basic = " or " in basic_code.lower()
                    if not has_and_basic:
                        error_count += 1
                    if not has_or_basic:
                        error_count += 1
                except Exception as e:
                    error_count += 1
            else:
                error_count += 1
            
            # Check machine operator (needs AND)
            if check_function_exists(self.module, "check_machine_operator"):
                try:
                    machine_code = inspect.getsource(getattr(self.module, "check_machine_operator"))
                    has_and_machine = " and " in machine_code.lower()
                    if not has_and_machine:
                        error_count += 1
                except Exception as e:
                    error_count += 1
            else:
                error_count += 1
            
            # Check night shift (needs OR)
            if check_function_exists(self.module, "check_night_shift"):
                try:
                    night_code = inspect.getsource(getattr(self.module, "check_night_shift"))
                    has_or_night = " or " in night_code.lower()
                    if not has_or_night:
                        error_count += 1
                except Exception as e:
                    error_count += 1
            else:
                error_count += 1
            
            # Check trainer (needs OR)
            if check_function_exists(self.module, "check_trainer"):
                try:
                    trainer_code = inspect.getsource(getattr(self.module, "check_trainer"))
                    has_or_trainer = " or " in trainer_code.lower()
                    if not has_or_trainer:
                        error_count += 1
                except Exception as e:
                    error_count += 1
            else:
                error_count += 1
            
            if error_count > 0:
                self.test_obj.yakshaAssert("test_logical_operators_usage", False, "functional")
                print("test_logical_operators_usage = Failed")
                return
            
            # Success case
            self.test_obj.yakshaAssert("test_logical_operators_usage", True, "functional")
            print("test_logical_operators_usage = Passed")
            
        except Exception as e:
            self.test_obj.yakshaAssert("test_logical_operators_usage", False, "functional")
            print("test_logical_operators_usage = Failed")

    def test_logic_implementation(self):
        """Test if the logic in functions is correctly implemented"""
        try:
            if self.module is None:
                self.test_obj.yakshaAssert("test_logic_implementation", False, "functional")
                print("test_logic_implementation = Failed")
                return
            
            error_count = 0
            
            # Get constants safely
            MIN_SAFETY_SCORE = safely_get_constant(self.module, "MIN_SAFETY_SCORE")
            MIN_EXPERIENCE = safely_get_constant(self.module, "MIN_EXPERIENCE")
            MAX_INCIDENTS = safely_get_constant(self.module, "MAX_INCIDENTS")
            MIN_TRAINING_SCORE = safely_get_constant(self.module, "MIN_TRAINING_SCORE")
            
            if any(x is None for x in [MIN_SAFETY_SCORE, MIN_EXPERIENCE, MAX_INCIDENTS, MIN_TRAINING_SCORE]):
                error_count += 1
            else:
                # Test basic eligibility OR logic
                if check_function_exists(self.module, "check_basic_eligibility"):
                    score_pass = safely_call_function(self.module, "check_basic_eligibility", True, MIN_SAFETY_SCORE, 1, 0)
                    exp_pass = safely_call_function(self.module, "check_basic_eligibility", True, 50, MIN_EXPERIENCE, 0)
                    both_fail = safely_call_function(self.module, "check_basic_eligibility", True, 50, 1, 0)
                    incidents_fail = safely_call_function(self.module, "check_basic_eligibility", True, 90, 5, MAX_INCIDENTS + 1)
                    
                    if score_pass != "Eligible":
                        error_count += 1
                    if exp_pass != "Eligible":
                        error_count += 1
                    if both_fail != "Not Eligible":
                        error_count += 1
                    if incidents_fail != "Not Eligible":
                        error_count += 1
                else:
                    error_count += 1
                
                # Test machine operator AND logic
                if check_function_exists(self.module, "check_machine_operator"):
                    machine_pass = safely_call_function(self.module, "check_machine_operator", "Eligible", True, MIN_TRAINING_SCORE)
                    machine_fail1 = safely_call_function(self.module, "check_machine_operator", "Not Eligible", True, MIN_TRAINING_SCORE)
                    machine_fail2 = safely_call_function(self.module, "check_machine_operator", "Eligible", False, MIN_TRAINING_SCORE)
                    machine_fail3 = safely_call_function(self.module, "check_machine_operator", "Eligible", True, MIN_TRAINING_SCORE - 1)
                    
                    if machine_pass != "Eligible":
                        error_count += 1
                    if machine_fail1 != "Not Eligible":
                        error_count += 1
                    if machine_fail2 != "Not Eligible":
                        error_count += 1
                    if machine_fail3 != "Not Eligible":
                        error_count += 1
                else:
                    error_count += 1
                
                # Test night shift OR logic
                if check_function_exists(self.module, "check_night_shift"):
                    night_leader = safely_call_function(self.module, "check_night_shift", "Eligible", True, True, 1)
                    night_exp = safely_call_function(self.module, "check_night_shift", "Eligible", True, False, 5)
                    night_fail = safely_call_function(self.module, "check_night_shift", "Eligible", True, False, 4)
                    
                    if night_leader != "Eligible":
                        error_count += 1
                    if night_exp != "Eligible":
                        error_count += 1
                    if night_fail != "Not Eligible":
                        error_count += 1
                else:
                    error_count += 1
                
                # Test trainer OR logic
                if check_function_exists(self.module, "check_trainer"):
                    trainer_incidents = safely_call_function(self.module, "check_trainer", "Eligible", 0, False)
                    trainer_leader = safely_call_function(self.module, "check_trainer", "Eligible", 2, True)
                    trainer_fail = safely_call_function(self.module, "check_trainer", "Eligible", 1, False)
                    
                    if trainer_incidents != "Eligible":
                        error_count += 1
                    if trainer_leader != "Eligible":
                        error_count += 1
                    if trainer_fail != "Not Eligible":
                        error_count += 1
                else:
                    error_count += 1
            
            if error_count > 0:
                self.test_obj.yakshaAssert("test_logic_implementation", False, "functional")
                print("test_logic_implementation = Failed")
                return
            
            # Success case
            self.test_obj.yakshaAssert("test_logic_implementation", True, "functional")
            print("test_logic_implementation = Passed")
            
        except Exception as e:
            self.test_obj.yakshaAssert("test_logic_implementation", False, "functional")
            print("test_logic_implementation = Failed")

if __name__ == '__main__':
    unittest.main()