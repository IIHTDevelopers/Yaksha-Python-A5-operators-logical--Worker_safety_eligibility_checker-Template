"""
You need to implement the logic for checking worker eligibility for different roles.
Each function will return "Eligible" or "Not Eligible" based on the conditions.

Required Variables:
- Constants:
    MIN_EXPERIENCE = 2
    MIN_SAFETY_SCORE = 75
    MAX_INCIDENTS = 3
    MIN_TRAINING_SCORE = 80
    MIN_ATTENDANCE = 90

- Intermediate calculation variables:
    has_required_performance = (safety_score >= MIN_SAFETY_SCORE or experience >= MIN_EXPERIENCE)
    has_safe_record = (incidents <= MAX_INCIDENTS)
    has_sufficient_training = (training_score >= MIN_TRAINING_SCORE)
    has_good_attendance = (attendance >= MIN_ATTENDANCE)
    is_qualified = (team_leader or experience >= 5)
    has_trainer_qualification = (incidents == 0 or team_leader)

IMPORTANT: Use logical operators (AND, OR) and comparison operators (>, <, >=, <=, ==)
"""

# Constants must be defined at module level
MIN_EXPERIENCE = 2
MIN_SAFETY_SCORE = 75
MAX_INCIDENTS = 3
MIN_TRAINING_SCORE = 80
MIN_ATTENDANCE = 90

def check_basic_eligibility(safety_training, safety_score, experience, incidents):
    """Check if worker meets basic work requirements
    
    TODO: Implement the logic checking these requirements:
    1. Must have safety training AND
    2. Must have either:
       - Safety score >= MIN_SAFETY_SCORE OR
       - Experience >= MIN_EXPERIENCE AND
    3. Must have incidents <= MAX_INCIDENTS
    
    Store intermediate results in:
    - has_required_performance = (safety_score >= MIN_SAFETY_SCORE or experience >= MIN_EXPERIENCE)
    - has_safe_record = (incidents <= MAX_INCIDENTS)
    
    Return "Eligible" if all conditions are met, "Not Eligible" otherwise
    """
    return "Not Eligible"  # Replace with your implementation

def check_machine_operator(basic_eligible, certification, training_score):
    """Check if worker can operate machines
    
    TODO: Implement the logic checking these requirements:
    1. Must be basic eligible ("Eligible") AND
    2. Must have certification AND
    3. Must have training score >= MIN_TRAINING_SCORE
    
    Example: A worker who is basic eligible, has certification (True),
            and training score 85 should return "Eligible"
    """
    return "Not Eligible"

def check_safety_supervisor(machine_eligible, first_aid, attendance):
    """Check if worker can be safety supervisor
    
    TODO: Implement the logic checking these requirements:
    1. Must be machine eligible ("Eligible") AND
    2. Must have first aid certification AND
    3. Must have attendance >= MIN_ATTENDANCE
    
    Example: A worker who is machine eligible, has first aid (True),
            and attendance 95 should return "Eligible"
    """
    return "Not Eligible"

def check_night_shift(basic_eligible, night_approved, team_leader, experience):
    """Check if worker can do night shifts
    
    TODO: Implement the logic checking these requirements:
    1. Must be basic eligible ("Eligible") AND
    2. Must be approved for nights AND
    3. Must either:
       - Be a team leader OR
       - Have experience >= 5 years
    
    Example: A worker who is basic eligible, night approved (True),
            not team leader but has 6 years experience should return "Eligible"
    """
    return "Not Eligible"

def check_trainer(supervisor_eligible, incidents, team_leader):
    """Check if worker can be a trainer
    
    TODO: Implement the logic checking these requirements:
    1. Must be supervisor eligible ("Eligible") AND
    2. Must either:
       - Have zero incidents OR
       - Be a team leader
    
    Example: A worker who is supervisor eligible and has 0 incidents
            should return "Eligible" even if not a team leader
    """
    return "Not Eligible"

if __name__ == "__main__":
    print("Worker Safety Eligibility Checker")
    print("-" * 30)
    
    # 1. Get boolean inputs (convert yes/no to True/False)
    # Example: safety_training = input("Has completed safety training? (yes/no): ").lower() == 'yes'
    
    # 2. Get numeric inputs (convert to int)
    # Example: experience = int(input("Years of experience: "))
    
    # 3. Check eligibilities in sequence
    # Example: basic_eligible = check_basic_eligibility(safety_training, safety_score, experience, incidents)
    
    # 4. Display results
    print("\nEligibility Results:")
    print("-" * 30)
    # Print each eligibility result