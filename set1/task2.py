from typing import Dict, List

# ============== TASK 1 FUNCTIONS ==============
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

def summarize_marks(marks: Dict[str, Dict], split: str) -> Dict[str, int]:
    """
    This function summarizes the result for a specific assignment: 
    calculating the average, number of invalid and valid marks.
    
    Args:
        1. marks (Dict[str, Dict]): Dictionary which is collection for all students.
        2. split (str): Assignment want to summarize.

    Returns:
        Dict[str, int]: A dictionary containing the average mark, invalid count, 
        and valid count for the specified assignment.
    """
    total_sum = 0
    invalid_count = 0
    valid_count = 0
    
    for student in marks.keys():
        mark = marks[student][split]

        # Skip student who don't have mark on assignment
        if not mark:
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

#####################################################

# ------------------ MAIN FUNCTION ------------------
def main(user_info: Dict[str, str], mark_unprocessed: Dict[str, str]) -> None:
    """
    This function starts the main Program

    Args:
        1. user_info (Dict[str, str]): the dictionary contains user's information (username, password)
        2. mark_unprocessed (Dict[str, str]): contain the list of marks 

    Returns:
        None - this function only control the logic of the main program
    """

    # DEFAULT CONSTANTS
    MENU_DEFAULT_PROMPT = "Welcome to the Mark system v0.0!\nPlease Login:\n1.Exit\n2.Login\nYour choice (number only): "
    MENU_DEFAULT_OPTIONS = ["1", "2"]
    MENU_LOGIN_OPTIONS = ["1", "2", "3", "4"]

    # STATES 
    login_user = None
    user_choice = None
    
    # Processed student's marks dictionary
    marks_processed = process_multiple_students_marks(mark_unprocessed)

    # MAIN MENU starts
    while user_choice != "1":

        # Get user's input
        if not login_user:
            user_choice = get_menu_choice(MENU_DEFAULT_PROMPT, MENU_DEFAULT_OPTIONS)
        else:
            username = login_user.get('username')
            MENU_LOGIN_PROMPT = f"Welcome {username}\nPlease choose one option below:\n1.Exit\n2.Re-Login\n3.Show mark records\n4.Show summarization\nYour choice (number only): "

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

    Args:
        1. user_info (Dict[str, str]): contain all the users info: including usernames and passwords

    Returns:
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

    Args: 
        None

    Return:
        None: the function only output a message to the console
    """
    print("==================================\nSee u!")

def show_mark_records(marks: Dict[str, int | float]) -> None:
    """
    This function show the marks records from the dictionary

    Args:
        1. marks (Dict[str, int | float]): the dictionary containing the student names and their marks

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

    Args:
        1. login_user (Dict[str, str]): the user info dictionary containing
        student's username and password
        2. marks(Dict[str, Dict[str, int]]): the dictionary containing 
        the students and their marks

    Return:
        None: the output is print out to the console
    """
    # Get available marks from the user and compute the menu prompt
    username = login_user.get('username')
    available_marks = marks.get(username).keys()
    
    if not available_marks:
        return
    
    asm_names = ", ".join(f"'{name}'" for name in available_marks)
    
    MENU_SUMMARY_PROMPT = (
        f"Available Assignments: {{{asm_names}}}\n" 
        "The Assignment you want to check (e.g., A1): "
    ) # escape characters {{ }}
    MENU_SUMMARY_OPTIONS = list(available_marks)

    chosen_assignment = get_menu_choice(MENU_SUMMARY_PROMPT, MENU_SUMMARY_OPTIONS)
    marks_summary = summarize_marks(marks, chosen_assignment)

    print("==================================") # seperator

    for label, value in marks_summary.items():
        print(f"{label}: {value}")

# UTILITY FUNCTIONS --------------------------------------
def get_menu_choice(prompt: str, options: List[str]) -> str:
    """
    This function gets valid input from user based on the available options
    
    Args:
        1. prompt (str): the message print to the console when request user's input
        2. options (List[str]): the available options for user to input 

    Returns
        user_input (str): the valid user's choice 
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