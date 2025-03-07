# Constants for eligibility criteria
MIN_EXPERIENCE = 2
MIN_SAFETY_SCORE = 75
MAX_INCIDENTS = 3
MIN_TRAINING_SCORE = 80
MIN_ATTENDANCE = 90

def check_basic_eligibility(safety_training, safety_score, experience, incidents):
    """Check if worker meets basic work requirements
    Requires: Safety training AND (good score OR experience) AND few incidents"""
    if not isinstance(safety_training, bool):
        raise ValueError("Safety training must be True/False")
    if not isinstance(safety_score, int) or not (0 <= safety_score <= 100):
        raise ValueError("Safety score must be 0-100")
    if not isinstance(experience, int) or experience < 0:
        raise ValueError("Experience must be non-negative")
    if not isinstance(incidents, int) or incidents < 0:
        raise ValueError("Incidents must be non-negative")
    
    # Check if worker has required performance level (score OR experience)
    has_required_performance = (safety_score >= MIN_SAFETY_SCORE or experience >= MIN_EXPERIENCE)
    
    # Check if worker has acceptable safety record
    has_safe_record = (incidents <= MAX_INCIDENTS)
    
    # Worker needs training AND performance AND safety record
    if safety_training and has_required_performance and has_safe_record:
        return "Eligible"
    return "Not Eligible"

def check_machine_operator(basic_eligible, certification, training_score):
    """Check if worker can operate machines
    Requires: Basic eligibility AND certification AND good training score"""
    if basic_eligible not in ["Eligible", "Not Eligible"]:
        raise ValueError("Basic eligibility must be 'Eligible' or 'Not Eligible'")
    if not isinstance(basic_eligible, str):
        raise ValueError("Basic eligibility must be string")
    if not isinstance(certification, bool):
        raise ValueError("Certification must be True/False")
    if not isinstance(training_score, int) or not (0 <= training_score <= 100):
        raise ValueError("Training score must be 0-100")
    
    # Check if training score meets minimum requirement
    has_sufficient_training = (training_score >= MIN_TRAINING_SCORE)
    
    # Need basic eligibility AND certification AND good training
    if basic_eligible == "Eligible" and certification and has_sufficient_training:
        return "Eligible"
    return "Not Eligible"

def check_safety_supervisor(machine_eligible, first_aid, attendance):
    """Check if worker can be safety supervisor
    Requires: Machine operator AND first aid AND good attendance"""
    if machine_eligible not in ["Eligible", "Not Eligible"]:
        raise ValueError("Machine eligibility must be 'Eligible' or 'Not Eligible'")
    if not isinstance(machine_eligible, str):
        raise ValueError("Machine eligibility must be string")
    if not isinstance(first_aid, bool):
        raise ValueError("First aid must be True/False")
    if not isinstance(attendance, int) or not (0 <= attendance <= 100):
        raise ValueError("Attendance must be 0-100")
    
    # Check attendance requirement
    has_good_attendance = (attendance >= MIN_ATTENDANCE)
    
    # Need machine qualification AND first aid AND attendance
    if machine_eligible == "Eligible" and first_aid and has_good_attendance:
        return "Eligible"
    return "Not Eligible"

def check_night_shift(basic_eligible, night_approved, team_leader, experience):
    """Check if worker can do night shifts
    Requires: Basic work AND night approval AND (team leader OR experienced)"""
    if basic_eligible not in ["Eligible", "Not Eligible"]:
        raise ValueError("Basic eligibility must be 'Eligible' or 'Not Eligible'")
    if not isinstance(basic_eligible, str):
        raise ValueError("Basic eligibility must be string")
    if not isinstance(night_approved, bool):
        raise ValueError("Night approval must be True/False")
    if not isinstance(team_leader, bool):
        raise ValueError("Team leader must be True/False")
    if not isinstance(experience, int) or experience < 0:
        raise ValueError("Experience must be non-negative")
    
    # Check if worker is qualified (team leader OR experienced)
    is_qualified = (team_leader or experience >= 5)
    
    # Need basic eligibility AND approval AND qualification
    if basic_eligible == "Eligible" and night_approved and is_qualified:
        return "Eligible"
    return "Not Eligible"

def check_trainer(supervisor_eligible, incidents, team_leader):
    """Check if worker can be a trainer
    Requires: Safety supervisor AND (perfect record OR team leader)"""
    if supervisor_eligible not in ["Eligible", "Not Eligible"]:
        raise ValueError("Supervisor eligibility must be 'Eligible' or 'Not Eligible'")
    if not isinstance(supervisor_eligible, str):
        raise ValueError("Supervisor eligibility must be string")
    if not isinstance(incidents, int) or incidents < 0:
        raise ValueError("Incidents must be non-negative")
    if not isinstance(team_leader, bool):
        raise ValueError("Team leader must be True/False")
    
    # Check if worker has perfect record or is team leader
    has_trainer_qualification = (incidents == 0 or team_leader)
    
    # Need supervisor status AND qualification
    if supervisor_eligible == "Eligible" and has_trainer_qualification:
        return "Eligible"
    return "Not Eligible"

if __name__ == "__main__":
    print("Worker Safety Eligibility Checker")
    print("-" * 30)
    
    # Get yes/no inputs
    safety_training = input("Has completed safety training? (yes/no): ").lower() == 'yes'
    certification = input("Has required certification? (yes/no): ").lower() == 'yes'
    first_aid = input("Has first aid certification? (yes/no): ").lower() == 'yes'
    team_leader = input("Is a team leader? (yes/no): ").lower() == 'yes'
    night_shift_approved = input("Approved for night shifts? (yes/no): ").lower() == 'yes'
    
    # Get numeric inputs
    experience = int(input("Years of experience: "))
    safety_score = int(input("Safety assessment score (0-100): "))
    incidents = int(input("Number of safety incidents: "))
    training_score = int(input("Training assessment score (0-100): "))
    attendance = int(input("Attendance percentage: "))
    
    # Check eligibilities
    basic_eligible = check_basic_eligibility(safety_training, safety_score, experience, incidents)
    machine_eligible = check_machine_operator(basic_eligible, certification, training_score)
    supervisor_eligible = check_safety_supervisor(machine_eligible, first_aid, attendance)
    night_eligible = check_night_shift(basic_eligible, night_shift_approved, team_leader, experience)
    trainer_eligible = check_trainer(supervisor_eligible, incidents, team_leader)
    
    # Display results
    print("\nEligibility Results:")
    print("-" * 30)
    print("Basic Work:", basic_eligible)
    print("Machine Operation:", machine_eligible)
    print("Safety Supervisor:", supervisor_eligible)
    print("Night Shift:", night_eligible)
    print("Trainer:", trainer_eligible)