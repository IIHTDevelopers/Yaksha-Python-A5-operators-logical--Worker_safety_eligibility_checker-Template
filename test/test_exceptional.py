import pytest
from test.TestUtils import TestUtils
from worker_safety_eligibility_checker import (
    check_basic_eligibility, check_machine_operator,
    check_safety_supervisor, check_night_shift,
    check_trainer
)

test_obj = TestUtils()

def test_input_type_validations():
    """Test type validations across all functions"""
    try:
        # Boolean type validation
        with pytest.raises(ValueError):
            check_basic_eligibility("yes", 80, 2, 1)  # String instead of bool
        with pytest.raises(ValueError):
            check_machine_operator("Eligible", "yes", 80)  # String instead of bool
        with pytest.raises(ValueError):
            check_night_shift("Eligible", True, "yes", 5)  # String instead of bool
            
        # Integer type validation
        with pytest.raises(ValueError):
            check_basic_eligibility(True, "80", 2, 1)  # String instead of int
        with pytest.raises(ValueError):
            check_safety_supervisor("Eligible", True, "90")  # String instead of int
        with pytest.raises(ValueError):
            check_trainer("Eligible", "0", True)  # String instead of int
            
        # Function eligibility string validation
        with pytest.raises(ValueError):
            check_machine_operator(True, True, 80)  # Bool instead of string
        with pytest.raises(ValueError):
            check_safety_supervisor("maybe", True, 90)  # Invalid string
            
        test_obj.yakshaAssert("TestInputTypeValidations", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestInputTypeValidations", False, "exception")

def test_range_validations():
    """Test value range validations across all functions"""
    try:
        # Score range validations
        with pytest.raises(ValueError):
            check_basic_eligibility(True, -1, 2, 1)  # Negative score
        with pytest.raises(ValueError):
            check_basic_eligibility(True, 101, 2, 1)  # Score > 100
        with pytest.raises(ValueError):
            check_machine_operator("Eligible", True, 101)  # Score > 100
        with pytest.raises(ValueError):
            check_safety_supervisor("Eligible", True, 101)  # Attendance > 100
            
        # Negative value validations
        with pytest.raises(ValueError):
            check_basic_eligibility(True, 80, -1, 1)  # Negative experience
        with pytest.raises(ValueError):
            check_basic_eligibility(True, 80, 2, -1)  # Negative incidents
        with pytest.raises(ValueError):
            check_night_shift("Eligible", True, True, -1)  # Negative experience
        with pytest.raises(ValueError):
            check_trainer("Eligible", -1, True)  # Negative incidents
            
        test_obj.yakshaAssert("TestRangeValidations", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestRangeValidations", False, "exception")

def test_eligibility_string_format():
    """Test validation of eligibility string formats"""
    try:
        # Invalid eligibility string formats
        with pytest.raises(ValueError):
            check_machine_operator("eligible", True, 80)  # Wrong case
        with pytest.raises(ValueError):
            check_safety_supervisor("YES", True, 90)  # Wrong format
        with pytest.raises(ValueError):
            check_night_shift("no", True, True, 5)  # Wrong format
        with pytest.raises(ValueError):
            check_trainer("Possibly", 0, True)  # Invalid value
            
        test_obj.yakshaAssert("TestEligibilityStringFormat", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestEligibilityStringFormat", False, "exception")