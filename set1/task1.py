from typing import Dict


def mark_str_to_dict(mark_str: str) -> Dict[str, int | float]:
    mark_dict: Dict[str, int | float] = {}
    marks = mark_str.split(",")
    for mark in marks:
        key , value = mark.split(":")
        mark_dict[key.strip()] = float(value) if "." in value else int(value)
    return mark_dict

def fix_invalid_value(mark: int | float) -> int | float:
    if mark > 100 or mark < 0:
        return float("-inf")
    else:
         return mark

def mark_str_to_dict_revised(mark_str: str) -> Dict[str, int | float]:
    mark_dict: Dict[str, int | float] = {}
    marks = mark_str.split(",")
    for mark in marks:
        key , value = mark.split(":")
        value = float(value) if "." in value else int(value)
        mark_dict[key.strip()] = fix_invalid_value(value)
    return mark_dict


def process_multiple_students_marks(mark_dict: Dict[str, str]) -> Dict[str, int | float]:
    for key in mark_dict.keys():
        mark_dict[key] = mark_str_to_dict_revised(mark_dict[key])
    return mark_dict

def summarize_marks(marks: Dict[str, Dict], split: str) -> dict:
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