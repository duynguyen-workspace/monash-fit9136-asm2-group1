# ============== TASK 1 FUNCTIONS ==============
from typing import Dict

def mark_str_to_dict(mark_str: str) -> Dict[str, int | float]:
    """
    Convert a string of marks where each pair has form "A{1,2,3,...}:score"
    into a dictionary.
    Args:
        mark_str (str): String of marks.

    Returns:
        Dict[str, int | float]: The dictionary which mapping
        each mark to its assignment.
    """
    mark_dict: Dict[str, int | float] = {}
    marks = mark_str.split(",")
    for mark in marks:
        key , value = mark.split(":")
        # Prevent from having whitespace in value
        value = value.strip()
        mark_dict[key.strip()] = float(value) if "." in value else int(value)
    return mark_dict

def fix_invalid_value(mark: int | float) -> int | float:
    """
    Fix the invalid value of a mark if it not in the interval [0,100].
    Args:
        mark (int | float): The mark to check value.

    Returns:
        int | float: Return -inf value if it is not in the interval [0,100]
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
        mark_str (str): String of marks.

    Returns:
        Dict[str, int | float]: The dictionary which mapping each mark to its assignment
        with correct type and valid value.
    """
    mark_dict: Dict[str, int | float] = {}
    marks = mark_str.split(",")
    for mark in marks:
        key , value = mark.split(":")
        # Prevent from having whitespace in key and value
        value = value.strip()
        key = key.strip()
        value = float(value) if "." in value else int(value)
        mark_dict[key] = fix_invalid_value(value)
    return mark_dict


def process_multiple_students_marks(mark_dict: Dict[str, str]) -> Dict[str, int | float]:
    """
    Handle multiple students marks with their values have type string then after conversion
    return the collection for all students.
    Args:
        mark_dict (Dict[str, str]): Multiple students' records.

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
        marks (Dict[str, Dict]): Dictionary which is collection for all students.
        split (str): Assignment want to summarize.

    Returns:
        dict: which contain average score, number of invalid marks,
        number of valid marks of input assignment.
    """
    total_sum = 0.0
    invalid_count = 0
    valid_count = 0
    for key in marks.keys():
        mark = marks[key].get(split)

        # Skip student who don't have mark on assignment
        if mark is None:
            continue

        if mark != float("-inf"):
            valid_count += 1
            total_sum +=mark
        else:
            invalid_count += 1
    if valid_count == 0:
        average_mark = 0
    else:
        average_mark = total_sum / valid_count
    return {"average_mark": average_mark,
    "invalid_count": invalid_count,
    "valid_count": valid_count}

#####################################################

# ------------------ MAIN FUNCTION ------------------
def main(user_info, mark_unprocessed) -> None:
    """
    This function starts the main Program

    Params:
        1. user_info: <dict> the dictionary that contains user information (username, password)
        2. mark_unprocessed: <dict> contain the list of marks 

    Returns:
        None - this function only control the logic of the main program

    Notes: 
        - May implement checking for user_info dict (containing the key + value needed)
    """

    # REUSABLE VARIABLES - username, password from user dict + processed marks
    marks_processed = process_multiple_students_marks(mark_unprocessed) # from task1

    # for username, password in user_info.items():
    #     valid_username = username
    #     valid_password = password

    # DEFAULT CONSTANTS
    MENU_DEFAULT_PROMPT = "Welcome to the Mark system v0.0!\nPlease Login:\n1.Exit\n2.Login\nYour choice (number only): "

    MENU_DEFAULT_OPTIONS = ["1", "2"]

    MENU_LOGIN_OPTIONS = ["1", "2", "3", "4"]

    # STATES 
    login_user = None
    user_choice = None

    # MAIN MENU starts
    while user_choice != "1":

        # Get user's input
        if not login_user:
            user_choice = get_menu_choice(MENU_DEFAULT_PROMPT, MENU_DEFAULT_OPTIONS)
        else:
            username = login_user.get('username')
            MENU_LOGIN_PROMPT = "Welcome {}\nPlease choose one option below:\n1.Exit\n2.Re-Login\n3.Show mark records\n4.Show summarization\nYour choice (number only): ".format(username)

            user_choice = get_menu_choice(MENU_LOGIN_PROMPT, MENU_LOGIN_OPTIONS)

        # @Action 1: Exit Program
        if user_choice == "1":
            exit()

        # @Action 2: Login / Relogin
        if user_choice == "2":
            if not login_user:
                login_user = login(user_info)
            else:
                login_user = None # logout -> reset login state
                print("You have logged off successfully!")

        # --- ONLY AVAILABLE FOR LOGIN USER ---
        if login_user:
            # @Action 3: Show mark records
            if user_choice == "3":
                show_mark_records(marks_processed)

            # @Action 4: Show summarization
            if user_choice == "4":
                show_summarization(login_user, marks_processed)

# ACTION FUNCTIONS --------------------------------------
def login(user_info: Dict[str, str]) -> Dict[str, str] | None:
    """
    This function performs the login action and return the login user

    Params:
        1. user_info: contain all the users info: including usernames and passwords

    Return:
        Dict[str, str] | None: the login user info, containing their 
        username and password. Or None (if incorrect username / password)

    Requirements:
        1. matching username (case insensitive)
        2. matching password (case sensitive)
    """
    print("==================================") # seperator

    input_username = input("Please key your account name: ")
    input_password = input("Please key your password: ")

    # If username found and corresponding password match -> return a dictionary of user info
    for valid_username, valid_password in user_info.items():
        if input_username.lower() == valid_username.lower() and input_password == valid_password:
            return {
                'username': valid_username,
                'password': valid_password
            }

    print("==================================") # seperator
    print("Incorrect username or password!")

    return None


def exit() -> None:
    """
    This function finish (ends) the system

    Params: 
        None

    Return:
        None: the function only output a message to the console
    """
    print("==================================\nSee u!")

def show_mark_records(marks: dict) -> None:
    """
    This function show the marks records (task1 function)

    Params:
        1. marks: the dictionary containing the students and their marks

    Return:
        None: the output is print out to the console
    """
    print("==================================") # seperator

    for person_name, person_marks in marks.items():
        print(f"{person_name}:")

        for asm_name, asm_mark in person_marks.items():
            print(f"\t{asm_name}: {asm_mark}")

def show_summarization(login_user: Dict[str, str], marks: Dict[str, Dict[str, int]]) -> None:
    """
    This function show the summarization of an assignment based on the given marks 
    (reuse task 1 function)

    Params:
        1. login_user: <Dict[str, str]> the user info dictionary containing
        student's username and password
        2. marks: <Dict[str, Dict[str, int]]> the dictionary containing 
        the students and their marks

    Return:
        None: the output is print out to the console
    """
    # Get available marks and compute the menu prompt
    assignments = set()
    for student in marks.values():
        assignments.update(student.keys())

    if not assignments:
        return

    assignments = sorted(assignments,reverse=True)
    assignments_count = set(assignments)
    MENU_SUMMARY_PROMPT = (
        f"Available Assignments: {assignments}\n"
        "The Assignment you want to check (e.g., A1): "
    )
    MENU_SUMMARY_OPTIONS = list(assignments)

    chosen_assignment = get_menu_choice(MENU_SUMMARY_PROMPT, MENU_SUMMARY_OPTIONS)
    marks_summary = summarize_marks(marks, chosen_assignment)

    print("==================================")
    print(f"Results For {chosen_assignment}:")



    print("==================================") # seperator

    for label, value in marks_summary.items():
        print(f"{label}: {value}")

# UTILITY FUNCTIONS --------------------------------------
def get_menu_choice(prompt: str, options: list) -> str:
    """
    This function gets valid input from user based on the available options
    
    Params:
        1. prompt: <str> the message print to the console when request user's input
        2. options: <list> the available options for user to input 

    Return
        user_input: <str> the valid user's choice 
    """
    is_input_valid = False

    while not is_input_valid:
        print("==================================") # seperator

        print(prompt, end="")
        user_input = input("")

        if user_input in options:
            is_input_valid = True

    return user_input


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    user_info = {
        "trang": "trang123"
    }
    mark_unprocessed = {
        "Jueqing": "A1: 99, A2: 200, A3: -100",
        "Trang"  : "A1: 300, A2: 100, A3: 100"
    }
    main(user_info, mark_unprocessed)
    # print(process_multiple_students_marks(mark_unprocessed))