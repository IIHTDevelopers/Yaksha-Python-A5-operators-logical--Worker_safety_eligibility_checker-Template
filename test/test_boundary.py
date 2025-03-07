import pytest
from test.TestUtils import TestUtils
from worker_safety_eligibility_checker import (
    check_basic_eligibility, check_machine_operator,
    check_safety_supervisor, check_night_shift,
    check_trainer, MIN_EXPERIENCE, MIN_SAFETY_SCORE,
    MAX_INCIDENTS, MIN_TRAINING_SCORE, MIN_ATTENDANCE
)

test_obj = TestUtils()

def test_minimum_thresholds():
    """Test exact minimum threshold values across functions"""
    try:
        # Test minimum values that should pass
        basic_min = check_basic_eligibility(True, MIN_SAFETY_SCORE, 1, MAX_INCIDENTS) == "Eligible"
        machine_min = check_machine_operator("Eligible", True, MIN_TRAINING_SCORE) == "Eligible"
        supervisor_min = check_safety_supervisor("Eligible", True, MIN_ATTENDANCE) == "Eligible"
        night_min = check_night_shift("Eligible", True, False, 5) == "Eligible"
        trainer_min = check_trainer("Eligible", 0, False) == "Eligible"
        
        # Test values just below minimum that should fail
        basic_below = check_basic_eligibility(True, MIN_SAFETY_SCORE - 1, 1, MAX_INCIDENTS) == "Not Eligible"
        machine_below = check_machine_operator("Eligible", True, MIN_TRAINING_SCORE - 1) == "Not Eligible"
        supervisor_below = check_safety_supervisor("Eligible", True, MIN_ATTENDANCE - 1) == "Not Eligible"
        night_below = check_night_shift("Eligible", True, False, 4) == "Not Eligible"
        trainer_below = check_trainer("Eligible", 1, False) == "Not Eligible"
        
        test_obj.yakshaAssert("TestMinimumThresholds", 
                             all([basic_min, machine_min, supervisor_min, night_min, trainer_min,
                                 basic_below, machine_below, supervisor_below, night_below, trainer_below]), 
                             "boundary")
    except Exception as e:
        test_obj.yakshaAssert("TestMinimumThresholds", False, "boundary")

def test_alternative_criteria():
    """Test boundary cases with alternative criteria"""
    try:
        # Alternative criteria cases
        basic_alt = check_basic_eligibility(True, MIN_SAFETY_SCORE - 1, MIN_EXPERIENCE, MAX_INCIDENTS) == "Eligible"
        night_alt = check_night_shift("Eligible", True, True, 0) == "Eligible"
        trainer_alt = check_trainer("Eligible", 10, True) == "Eligible"
        
        # Test with failing eligibility from previous function
        machine_fail = check_machine_operator("Not Eligible", True, 100) == "Not Eligible"
        supervisor_fail = check_safety_supervisor("Not Eligible", True, 100) == "Not Eligible"
        
        test_obj.yakshaAssert("TestAlternativeCriteria", 
                             all([basic_alt, night_alt, trainer_alt, machine_fail, supervisor_fail]), 
                             "boundary")
    except Exception as e:
        test_obj.yakshaAssert("TestAlternativeCriteria", False, "boundary")