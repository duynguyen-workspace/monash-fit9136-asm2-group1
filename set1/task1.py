from typing import Dict


def mark_str_to_dict(mark_str: str) -> Dict[str, int | float]:
    pass


def fix_invalid_value(mark: int | float) -> int | float:
    pass


def mark_str_to_dict_revised(mark_str: str) -> Dict[str, int | float]:
    pass


def process_multiple_students_marks(mark_dict: Dict[str, str]) -> Dict[str, int | float]:
    pass


def summarize_marks(marks: Dict[str, Dict], split: str) -> dict:
    pass


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # Your testing code goes here
    m = {
        "Jueqing": "A1: 99, A2: 200, A3: -100",
        "Trang"  : "A1: 300, A2: 100, A3: 100"
    }
    res = process_multiple_students_marks(m)
    print(res)