import pytest
import re
from test.TestUtils import TestUtils
from worker_safety_eligibility_checker import *

test_obj = TestUtils()

def test_required_variables():
    """Test if required variables are correctly defined"""
    try:
        with open('worker_safety_eligibility_checker.py', 'r') as file:
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
        
        all_vars_found = True
        for var_set in [logical_vars, result_vars]:
            for var_name, pattern in var_set.items():
                if not re.search(pattern, content):
                    all_vars_found = False
                    break
        
        test_obj.yakshaAssert("TestRequiredVariables", all_vars_found, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestRequiredVariables", False, "functional")

def test_logical_operators_usage():
    """Test if required logical operators are used in functions"""
    try:
        # Get function source codes
        functions = {
            'basic': check_basic_eligibility,
            'machine': check_machine_operator,
            'supervisor': check_safety_supervisor,
            'night': check_night_shift,
            'trainer': check_trainer
        }
        
        # Check operators in each function
        operators_used = True
        
        # Check basic eligibility (needs AND, OR)
        basic_code = functions['basic'].__code__.co_code.decode('latin-1')
        if 'and' not in str(functions['basic'].__code__.co_consts) or 'or' not in str(functions['basic'].__code__.co_consts):
            operators_used = False
        
        # Check machine operator (needs AND)
        machine_code = functions['machine'].__code__.co_code.decode('latin-1')
        if 'and' not in str(functions['machine'].__code__.co_consts):
            operators_used = False
        
        # Check night shift (needs OR)
        night_code = functions['night'].__code__.co_code.decode('latin-1')
        if 'or' not in str(functions['night'].__code__.co_consts):
            operators_used = False
        
        # Check trainer (needs OR)
        trainer_code = functions['trainer'].__code__.co_code.decode('latin-1')
        if 'or' not in str(functions['trainer'].__code__.co_consts):
            operators_used = False
        
        test_obj.yakshaAssert("TestLogicalOperatorsUsage", operators_used, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestLogicalOperatorsUsage", False, "functional")

def test_logic_implementation():
    """Test if the logic in functions is correctly implemented"""
    try:
        # Test basic eligibility OR logic
        score_pass = check_basic_eligibility(True, MIN_SAFETY_SCORE, 1, 0) == "Eligible"
        exp_pass = check_basic_eligibility(True, 50, MIN_EXPERIENCE, 0) == "Eligible"
        both_fail = check_basic_eligibility(True, 50, 1, 0) == "Not Eligible"
        incidents_fail = check_basic_eligibility(True, 90, 5, MAX_INCIDENTS + 1) == "Not Eligible"
        
        # Test machine operator AND logic
        machine_pass = check_machine_operator("Eligible", True, MIN_TRAINING_SCORE) == "Eligible"
        machine_fail1 = check_machine_operator("Not Eligible", True, MIN_TRAINING_SCORE) == "Not Eligible"
        machine_fail2 = check_machine_operator("Eligible", False, MIN_TRAINING_SCORE) == "Not Eligible"
        machine_fail3 = check_machine_operator("Eligible", True, MIN_TRAINING_SCORE - 1) == "Not Eligible"
        
        # Test night shift OR logic
        night_leader = check_night_shift("Eligible", True, True, 1) == "Eligible"
        night_exp = check_night_shift("Eligible", True, False, 5) == "Eligible"
        night_fail = check_night_shift("Eligible", True, False, 4) == "Not Eligible"
        
        # Test trainer OR logic
        trainer_incidents = check_trainer("Eligible", 0, False) == "Eligible"
        trainer_leader = check_trainer("Eligible", 2, True) == "Eligible"
        trainer_fail = check_trainer("Eligible", 1, False) == "Not Eligible"
        
        all_tests_pass = all([
            score_pass, exp_pass, both_fail, incidents_fail,
            machine_pass, machine_fail1, machine_fail2, machine_fail3,
            night_leader, night_exp, night_fail,
            trainer_incidents, trainer_leader, trainer_fail
        ])
        
        test_obj.yakshaAssert("TestLogicImplementation", all_tests_pass, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestLogicImplementation", False, "functional")