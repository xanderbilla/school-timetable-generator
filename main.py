#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
School Timetable Generator

This program generates an optimal weekly timetable for a school based on 
classes, subjects, teachers, and period requirements.
"""

### DO NOT MODIFY THE CODE BELOW THIS LINE ###

# Define the input constraints
# Classes
classes = ["Class 6A", "Class 6B", "Class 7A", "Class 7B"]

# Subjects
subjects = ["Mathematics", "Science", "English", "Social Studies", "Computer Science", "Physical Education"]

# Weekly period requirements for each class and subject
# {class_name: {subject_name: number_of_periods_per_week}}
class_subject_periods = {
    "Class 6A": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 3, "Physical Education": 3},
    "Class 6B": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 3, "Physical Education": 3},
    "Class 7A": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 4, "Physical Education": 2},
    "Class 7B": {"Mathematics": 6, "Science": 6, "English": 6, "Social Studies": 6, "Computer Science": 4, "Physical Education": 2}
}

# Teachers and their teaching capabilities
# {teacher_name: [list_of_subjects_they_can_teach]}
teachers = {
    "Mr. Kumar": ["Mathematics"],
    "Mrs. Sharma": ["Mathematics"],
    "Ms. Gupta": ["Science"],
    "Mr. Singh": ["Science", "Social Studies"],
    "Mrs. Patel": ["English"],
    "Mr. Joshi": ["English", "Social Studies"],
    "Mr. Malhotra": ["Computer Science"],
    "Mr. Chauhan": ["Physical Education"]
}

# School timing configuration
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
periods_per_day = 6

### DO NOT MODIFY THE CODE ABOVE THIS LINE ###

def generate_timetable():
    """
    Generate a weekly timetable for the school based on the given constraints.
    
    Returns:
        dict: A data structure representing the complete timetable
              Format: {day: {period: {class: (subject, teacher)}}}
    """
    # Initialize an empty timetable
    timetable = {day: {period: {} for period in range(1, periods_per_day + 1)} for day in days_of_week}
    
    # Create a list of all periods to be scheduled
    periods_to_schedule = []
    for class_name in classes:
        for subject, count in class_subject_periods[class_name].items():
            for _ in range(count):
                periods_to_schedule.append((class_name, subject))
    
    # Shuffle the periods to randomize the assignment
    import random
    random.shuffle(periods_to_schedule)
    
    # Track teacher assignments to avoid double-booking
    teacher_assignments = {day: {period: set() for period in range(1, periods_per_day + 1)} for day in days_of_week}
    
    # Track subject counts for each class to ensure we don't exceed requirements
    subject_counts = {class_name: {subject: 0 for subject in subjects} for class_name in classes}
    
    # Track unassigned periods for reporting
    unassigned_periods = []
    
    # Try to assign each period
    for class_name, subject in periods_to_schedule:
        assigned = False
        
        # Try each day and period
        for day in days_of_week:
            if assigned:
                break
                
            for period in range(1, periods_per_day + 1):
                # Skip if this period is already assigned for this class
                if class_name in timetable[day][period]:
                    continue
                
                # Find a teacher who can teach this subject
                available_teacher = None
                for teacher, subjects_they_can_teach in teachers.items():
                    if subject in subjects_they_can_teach and teacher not in teacher_assignments[day][period]:
                        available_teacher = teacher
                        break
                
                # If we found an available teacher, assign the period
                if available_teacher:
                    timetable[day][period][class_name] = (subject, available_teacher)
                    teacher_assignments[day][period].add(available_teacher)
                    subject_counts[class_name][subject] += 1
                    assigned = True
                    break
        
        # If we couldn't assign this period, track it for reporting
        if not assigned:
            unassigned_periods.append((class_name, subject))
    
    # Report any unassigned periods
    if unassigned_periods:
        print("\nWarning: The following periods could not be assigned:")
        for class_name, subject in unassigned_periods:
            print(f"  - {subject} for {class_name}")
        print("The timetable may be incomplete or invalid.")
    
    return timetable


def display_timetable(timetable):
    """
    Display the generated timetable in a readable format.
    
    Args:
        timetable (dict): The generated timetable
    """
    # Display timetable for each class
    print("\n" + "="*100)
    print("CLASS TIMETABLES".center(100))
    print("="*100)
    
    for class_name in classes:
        print(f"\n{class_name} Timetable:")
        print("-" * 100)
        
        # Print header row with days
        print("Period |", end=" ")
        for day in days_of_week:
            print(f"{day:<20}", end=" ")
        print()
        print("-" * 100)
        
        # Print each period
        for period in range(1, periods_per_day + 1):
            print(f"{period:^6} |", end=" ")
            for day in days_of_week:
                if class_name in timetable[day][period]:
                    subject, teacher = timetable[day][period][class_name]
                    print(f"{subject} ({teacher})", end=" ")
                else:
                    print(" " * 20, end=" ")
            print()
    
    # Display timetable for each teacher
    print("\n" + "="*100)
    print("TEACHER TIMETABLES".center(100))
    print("="*100)
    
    for teacher in teachers:
        print(f"\n{teacher} Timetable:")
        print("-" * 100)
        
        # Print header row with days
        print("Period |", end=" ")
        for day in days_of_week:
            print(f"{day:<20}", end=" ")
        print()
        print("-" * 100)
        
        # Print each period
        for period in range(1, periods_per_day + 1):
            print(f"{period:^6} |", end=" ")
            for day in days_of_week:
                found = False
                for class_name in classes:
                    if class_name in timetable[day][period] and timetable[day][period][class_name][1] == teacher:
                        subject = timetable[day][period][class_name][0]
                        print(f"{subject} ({class_name})", end=" ")
                        found = True
                        break
                if not found:
                    print(" " * 20, end=" ")
            print()


def validate_timetable(timetable):
    """
    Validate that the generated timetable meets all constraints.
    
    Args:
        timetable (dict): The generated timetable
        
    Returns:
        bool: True if timetable is valid, False otherwise
        str: Error message if timetable is invalid
    """
    # Check if all classes have their required number of periods for each subject
    subject_counts = {class_name: {subject: 0 for subject in subjects} for class_name in classes}
    
    for day in days_of_week:
        for period in range(1, periods_per_day + 1):
            for class_name in classes:
                if class_name in timetable[day][period]:
                    subject, _ = timetable[day][period][class_name]
                    subject_counts[class_name][subject] += 1
    
    # Check if all required periods are scheduled
    missing_periods = []
    for class_name in classes:
        for subject, required_count in class_subject_periods[class_name].items():
            if subject_counts[class_name][subject] < required_count:
                missing_periods.append((class_name, subject, subject_counts[class_name][subject], required_count))
    
    if missing_periods:
        error_msg = "The following required periods are missing:\n"
        for class_name, subject, actual, required in missing_periods:
            error_msg += f"  - {class_name} has only {actual} periods of {subject}, but requires {required}\n"
        return False, error_msg
    
    # Check if teachers are not double-booked
    teacher_assignments = {day: {period: set() for period in range(1, periods_per_day + 1)} for day in days_of_week}
    double_bookings = []
    
    for day in days_of_week:
        for period in range(1, periods_per_day + 1):
            for class_name in classes:
                if class_name in timetable[day][period]:
                    _, teacher = timetable[day][period][class_name]
                    if teacher in teacher_assignments[day][period]:
                        double_bookings.append((teacher, day, period))
                    teacher_assignments[day][period].add(teacher)
    
    if double_bookings:
        error_msg = "The following teachers are double-booked:\n"
        for teacher, day, period in double_bookings:
            error_msg += f"  - {teacher} on {day} period {period}\n"
        return False, error_msg
    
    # Check if teachers are only teaching subjects they can teach
    invalid_assignments = []
    for day in days_of_week:
        for period in range(1, periods_per_day + 1):
            for class_name in classes:
                if class_name in timetable[day][period]:
                    subject, teacher = timetable[day][period][class_name]
                    if subject not in teachers[teacher]:
                        invalid_assignments.append((teacher, subject, class_name, day, period))
    
    if invalid_assignments:
        error_msg = "The following teachers are assigned to subjects they cannot teach:\n"
        for teacher, subject, class_name, day, period in invalid_assignments:
            error_msg += f"  - {teacher} is teaching {subject} to {class_name} on {day} period {period}\n"
        return False, error_msg
    
    return True, "Timetable is valid and meets all constraints."


def main():
    """
    Main function to generate and display the timetable.
    """
    print("\n" + "="*100)
    print("SCHOOL TIMETABLE GENERATOR".center(100))
    print("="*100)
    print("\nGenerating school timetable...")
    
    # Generate the timetable
    timetable = generate_timetable()
    
    # Validate the timetable
    print("\nValidating timetable...")
    is_valid, message = validate_timetable(timetable)
    
    if is_valid:
        print("\n" + "="*100)
        print("TIMETABLE GENERATION SUCCESSFUL".center(100))
        print("="*100)
        print(f"\n{message}")
        
        # Display the timetable
        display_timetable(timetable)
    else:
        print("\n" + "="*100)
        print("TIMETABLE GENERATION FAILED".center(100))
        print("="*100)
        print(f"\n{message}")
        print("\nPlease try running the program again. The algorithm uses randomization,")
        print("so each attempt may produce different results.")


if __name__ == "__main__":
    main()
