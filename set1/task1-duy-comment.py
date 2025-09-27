from typing import Dict

def mark_str_to_dict(mark_str: str) -> Dict[str, int | float]:
    """
    This function converts the assignment marks, where each pair 
    has form "A{1,2,3,...}: score" into a dictionary.

    Params:
        1. mark_str: <str> A string containing assignment names and marks in the format "A1: 100, A2: 95, A3: 91.5"

    Returns:
        mark_dict: <Dict[str, int | float]> A dictionary with assignment names as keys and their corresponding marks as values.
    """
    if not mark_str:
        return {}
    
    mark_dict = {}

    # get each assignment mark(s) and store them corresponding to their int / float value in the dictionary
    marks = mark_str.split(",")
    for mark in marks:
        asm_name, asm_mark = mark.split(":")
        asm_mark = float(asm_mark) if "." in asm_mark else int(asm_mark) # int / float corresponding conversion
        mark_dict[asm_name.strip()] = asm_mark
    
    return mark_dict

def fix_invalid_value(mark: int | float) -> int | float:
    """
    Fixes invalid assignment marks that are greater than 100 or less than 0 
    by replacing them with -inf.

    Params:
        1. mark: <int | float> The mark to be validated and fixed.

    Returns:
        <int | float>: The original mark if valid, otherwise -inf (float) for invalid marks.

    """
    if mark > 100 or mark < 0:
        return float("-inf")
    
    return mark

def mark_str_to_dict_revised(mark_str: str) -> Dict[str, int | float]:
    """
    This function converts a string of assignment marks into a dictionary 
    while fixing invalid marks (greater than 100 or less than 0).

    Params:
        1. mark_str: <str> A string containing assignment names and marks, where invalid marks will be handled.

    Returns:
        mark_dict: <Dict[str, int | float]> A dictionary with assignment names as keys and their corresponding valid or fixed marks as values.
    """
    if not mark_str:
        return {}

    # Get the assignment name + assignment mark and insert them accordingly to the dictionary
    mark_dict = {}

    marks = mark_str.split(",")
    for mark in marks:
        asm_name , asm_mark = mark.split(":")
        asm_mark = float(asm_mark) if "." in asm_mark else int(asm_mark) # int / float corresponding conversion
        mark_dict[asm_name.strip()] = fix_invalid_value(asm_mark)

    return mark_dict


def process_multiple_students_marks(mark_dict: Dict[str, str]) -> Dict[str, int | float]:
    """
    This function processes the marks of multiple students by converting 
    their assignment mark strings into dictionaries and fixing invalid values.

    Params:
        1. mark_dict: <Dict[str, str]> A dictionary where the keys are student names and values are their assignment marks as strings.

    Returns:
        <Dict[str, int | float]>: A dictionary with student names as keys, and their processed marks as sub-dictionaries.

    """
    for student in mark_dict.keys():
        mark_dict[student] = mark_str_to_dict_revised(mark_dict[student])

    return mark_dict

def summarize_marks(marks: Dict[str, Dict[str, int]], split: str) -> Dict[str, int]:
    """
    This function summarizes the result for a specific assignment: 
    calculating the average, invalid count, and valid count.

    Params:
        1. marks: <Dict[str, Dict]> A dictionary of students with their assignment name with corresponding marks.
        2. split: <str> The assignment name to summarize (e.g., "A1", "A2", "A3").

    Returns:
        <Dict[str, int]>: A dictionary containing the average mark, invalid count, and valid count for the specified assignment.
    """
    total_sum = 0
    invalid_count = 0
    valid_count = 0
    
    # Calculate the sum of student's assignment score, store the valid + invalid count 
    for student in marks.keys():
        mark = marks[student][split]

        if mark != float("-inf"):
            valid_count += 1
            total_sum +=mark
        else:
            invalid_count += 1

    # calculate average mark and convert to appropriate data type (int | float)
    average_mark = total_sum / valid_count
    average_mark = int(average_mark) if isinstance(average_mark, float) and average_mark.is_integer() else average_mark
    
    return {
        "average_mark": average_mark, 
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