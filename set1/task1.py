from typing import Dict

def mark_str_to_dict(mark_str: str) -> Dict[str, int | float]:
    """
    This function converts the assignment marks, where each pair 
    has form "A{1,2,3,...}: score" into a dictionary.

    Args:
        1. mark_str: <str> String of assignment names and marks in the format 
        "A1: 100, A2: 95, A3: 91.5"

    Returns:
        mark_dict: <Dict[str, int | float]> A dictionary with assignment names 
        as keys and their corresponding marks as values.
    """
    if not mark_str:
        return {}
    
    mark_dict = {}
    
    # extract and clean assignment mark(s), store them corresponding to their int / float value in the dictionary
    marks = mark_str.split(",")
    for mark in marks:
        asm_name, asm_mark = mark.split(":")
        # prevent whitespace in key & value
        asm_name = asm_name.strip()
        asm_mark = asm_mark.strip()
        
        asm_mark = float(asm_mark) if "." in asm_mark else int(asm_mark) # int / float corresponding conversion
        mark_dict[asm_name] = asm_mark
    
    return mark_dict

def fix_invalid_value(mark: int | float) -> int | float:
    """
    This function fixes invalid assignment marks that are greater than 100 or 
    less than 0 by replacing them with -inf.
    
    Args:
        1. mark (int | float): The mark to be validated and fixed.

    Returns:
        int | float: The original mark if valid, otherwise -inf (float) for invalid marks.
    """
    if mark > 100 or mark < 0:
        return float("-inf")
    else:
        return mark

def mark_str_to_dict_revised(mark_str: str) -> Dict[str, int | float]:
    """
    This function converts a string of assignment marks into a dictionary 
    while fixing invalid marks (greater than 100 or less than 0).
    
    Args:
        1. mark_str: <str> String of assignment names and marks in the format 
        "A1: 100, A2: 95, A3: 91.5"

    Returns:
        mark_dict: Dict[str, int | float]: A dictionary with assignment names 
        as keys and their corresponding marks as values, with correct type and valid value.
    """
    if not mark_str:
        return {}
    
    # Get assignment names and marks, store them corresponding to the dictionary
    mark_dict = {}
    
    marks = mark_str.split(",")
    for mark in marks:
        asm_name, asm_mark = mark.split(":")
        # prevent whitespace in key & value
        asm_name = asm_name.strip()
        asm_mark = asm_mark.strip()
        
        asm_mark = float(asm_mark) if "." in asm_mark else int(asm_mark) # int / float corresponding conversion
        mark_dict[asm_name] = fix_invalid_value(asm_mark)
    return mark_dict


def process_multiple_students_marks(mark_dict: Dict[str, str]) -> Dict[str, int | float]:
    """
    This function processes the marks of multiple students by converting 
    their assignment mark strings into dictionaries and fixing invalid values.
    
    Args:
        1. mark_dict (Dict[str, str]): A dictionary where the keys are 
        student names and values are their assignment marks as strings.

    Returns:
        Dict[str, int | float]: A dictionary with student names as keys, 
        and their processed marks as sub-dictionaries.
    """
    for student in mark_dict.keys():
        mark_dict[student] = mark_str_to_dict_revised(mark_dict[student])

    return mark_dict

def summarize_marks(marks: Dict[str, Dict[str, int | float]], split: str) -> Dict[str, int | float]:
    """
    This function summarizes the result for a specific assignment: 
    calculating the average, number of invalid and valid marks.
    
    Args:
        1. marks (Dict[str, Dict[str, int | float]): Dictionary which is contains the marks for all students.
        2. split (str): Assignment want to summarize.

    Returns:
        Dict[str, int | float]: A dictionary containing the average mark, invalid count, 
        and valid count for the specified assignment.
    """
    total_sum = 0
    invalid_count = 0
    valid_count = 0
    
    for student in marks.keys():
        student_marks = marks[student]
        mark = student_marks.get(split)

        # Skip student who don't have mark on assignment
        if mark is None:
            continue

        if mark != float("-inf"):
            valid_count += 1
            total_sum +=mark
        else:
            invalid_count += 1
            
    # calculate average mark and convert to appropriate data type (int | float)
    if valid_count == 0:
        average_mark = 0
    else:
        average_mark = total_sum / valid_count
        
    final_average_mark = int(average_mark) if isinstance(average_mark, float) and average_mark.is_integer() else average_mark
    
    return {
        "average_mark": final_average_mark,
        "invalid_count": invalid_count,
        "valid_count": valid_count
    }

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # Your testing code goes here
    m = {
        "Jueqing": "A1: 99, A2: 200, A3: -100",
        "Trang"  : "A1: 300, A2: 100, A3: 100"
    }
    res = process_multiple_students_marks(m)
    print(summarize_marks(res, "A2"))