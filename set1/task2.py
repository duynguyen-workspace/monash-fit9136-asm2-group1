# ============== TASK 1 FUNCTIONS ==============
from typing import Dict

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
    
    return {
        "average_mark": average_mark, 
        "invalid_count": invalid_count, 
        "valid_count": valid_count
    }
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

    # REUSABLE VARIABLES - username, password from user dict + marks to process
    valid_username = ""
    valid_password = ""
    marks_processed = process_multiple_students_marks(mark_unprocessed) # from task1

    for username, password in user_info.items():
        valid_username = username
        valid_password = password

    # DEFAULT CONSTANTS
    MENU_DEFAULT_PROMPT = "Welcome to the Mark system v0.0!\nPlease Login:\n1.Exit\n2.Login\nYour choice (number only): "
    
    MENU_DEFAULT_OPTIONS = ["1", "2"]

    MENU_LOGIN_PROMPT = "Welcome {}\nPlease choose one option below:\n1.Exit\n2.Re-Login\n3.Show mark records\n4.Show summarization\nYour choice (number only): ".format(valid_username)

    MENU_LOGIN_OPTIONS = ["1", "2", "3", "4"]

    # STATES 
    is_system_ended = False
    is_login = False

    # MAIN MENU starts
    while not is_system_ended:
        
        # Get user's input
        if not is_login:
            user_choice = get_menu_choice(MENU_DEFAULT_PROMPT, MENU_DEFAULT_OPTIONS)
        else:
            user_choice = get_menu_choice(MENU_LOGIN_PROMPT, MENU_LOGIN_OPTIONS)

        # @Action 1: Exit Program
        if user_choice == "1":
            is_system_ended = True
            exit()
        
        # @Action 2: Login / Relogin
        if user_choice == "2":
            if not is_login:
                is_login = login(valid_username, valid_password)
            else:
                is_login = False # logout -> reset login state
                print("You have logged off successfully!")
                

        # --- ONLY AVAILABLE FOR LOGIN USER ---
        if is_login:
            # @Action 3: Show mark records
            if user_choice == "3":
                show_mark_records(marks_processed)
            
            # @Action 4: Show summarization
            if user_choice == "4":
                show_summarization(marks_processed)

def login(valid_username: str, valid_password: str) -> bool:
    """
    This function performs the login action 

    Params:
        1. valid_username: <str> user's username 
        2. valid_password: <str> user's password

    Return:
        bool: the login status (success or failed)
    """
    # is_username_correct = False
    # is_password_correct = False

    print("==================================") # seperator

    input_username = input("Please key your account name: ")
    input_password = input("Please key your password: ")

    if input_username.lower() != valid_username.lower() or input_password != valid_password:
        print("==================================") # seperator
        print("Incorrect username or password!")
        return False
    
    return True

def exit() -> None:
    """
    This function finish (ends) the system

    Params: 
        None

    Return:
        None: the function only output a message to the console
    """
    print("==================================\nSee u!")

# copy your codes from task 1 to here if necessary
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

def show_summarization(marks: dict) -> None:
    """
    Params:
        1. marks: the dictionary containing the students and their marks

    Return:
        None: the output is print out to the console
    """
    MENU_SUMMARY_PROMPT = "Available Assignments: {'A3', 'A2', 'A1'}\nThe Assignment you want to check (e.g., A1): "
    
    MENU_SUMMARY_OPTIONS = ['A3', 'A2', 'A1']

    chosen_assignment = get_menu_choice(MENU_SUMMARY_PROMPT, MENU_SUMMARY_OPTIONS)
    marks_summary = summarize_marks(marks, chosen_assignment)

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
        user_option: <str> the valid user's choice 
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
        "Jueqing": "Jueqing123"
    }
    mark_unprocessed = {
        "Jueqing": "A1: 99, A2: 200, A3: -100",
        "Trang"  : "A1: 300, A2: 100, A3: 100"
    }
    main(user_info, mark_unprocessed)
    # print(process_multiple_students_marks(mark_unprocessed))