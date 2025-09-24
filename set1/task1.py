from typing import Dict


def mark_str_to_dict(mark_str: str) -> Dict[str, int | float]:
    """
    Convert a string of marks where each pair has form "A{1,2,3,...}:score"
    into a dictionary.
    Args:
        mark_str: str: String of marks.

    Returns:
        Dict[str, int | float]: The dictionary which mapping
        each mark to its assignment.
    """
    mark_dict: Dict[str, int | float] = {}
    marks = mark_str.split(",")
    for mark in marks:
        key , value = mark.split(":")
        mark_dict[key.strip()] = float(value) if "." in value else int(value)
    return mark_dict

def fix_invalid_value(mark: int | float) -> int | float:
    """
    Fix the invalid value of a mark if it not in the interval (0,100).
    Args:
        mark: int | float: The mark to check value.

    Returns:
        int | float: Return -inf value if it is not in the interval (0,100)
        else return the original value.
    """
    if mark > 100 or mark < 0:
        return float("-inf")
    else:
         return mark

def mark_str_to_dict_revised(mark_str: str) -> Dict[str, int | float]:
    """
    Convert the strings of mark to dictionary with valid value.
    The value will have type float if it has . in string else its type is int.
    Args:
        mark_str: str: String of marks.

    Returns:
        Dict[str, int | float]: The dictionary which mapping each mark to its assignment
        with correct type and valid value.
    """
    mark_dict: Dict[str, int | float] = {}
    marks = mark_str.split(",")
    for mark in marks:
        key , value = mark.split(":")
        value = float(value) if "." in value else int(value)
        mark_dict[key.strip()] = fix_invalid_value(value)
    return mark_dict


def process_multiple_students_marks(mark_dict: Dict[str, str]) -> Dict[str, int | float]:
    """
    Handle multiple students marks with their values have type string then after conversion
    return the collection for all students.
    Args:
        mark_dict: Dict[str, str]: Multiple students' records.

    Returns:
         Dict[str, int | float]: Dictionary which is collection for all students.
    """
    for key in mark_dict.keys():
        mark_dict[key] = mark_str_to_dict_revised(mark_dict[key])
    return mark_dict

def summarize_marks(marks: Dict[str, Dict], split: str) -> dict:
    """
    Summarize the average score, number of students, number of marks in one Assignment in
    the collection of students.
    Args:
        marks: Dict[str, Dict]: Dictionary which is collection for all students.
        split: str: Assignment want to summarize.

    Returns:
        dict: which contain average score, number of invalid marks,
        number of valid marks of input assignment.
    """
    total_sum = 0
    invalid_count = 0
    valid_count = 0
    for key in marks.keys():
        mark = marks[key][split]
        if mark != float("-inf"):
            valid_count += 1
            total_sum +=mark
        else:
            invalid_count += 1
    average_mark = total_sum / valid_count
    average_mark = int(average_mark) if isinstance(average_mark, float) and average_mark.is_integer() else average_mark
    return {"average_mark": average_mark,
    "invalid_count": invalid_count,
    "valid_count": valid_count}



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