# ------------------ MAIN FUNCTION ------------------
def main(user_info, mark_unprocessed):
    """
    """

    # REUSABLE VARIABLES
    valid_username = ""
    valid_password = ""

    for username, password in user_info.items():
        valid_username = username
        valid_password = password

    # DEFAULT CONSTANTS
    MENU_DEFAULT_PROMPT = """==================================
Welcome to the Mark system v0.0!
Please Login:
1.Exit
2.Login
Your choice (number only): """
    
    MENU_DEFAULT_OPTIONS = ["1", "2"]

    MENU_LOGIN_PROMPT = """==================================
Welcome {valid_username}!
Please choice one option below:
1.Exit
2.Re-Login
3.Show mark records
4.Show summarization
Your choice (number only): """

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

        # --- ONLY AVAILABLE FOR LOGIN USER ---
        if is_login:
            # @Action 3: Show mark records
            if user_choice == "3":
                show_mark_records(mark_unprocessed)
            
            # @Action 4: Show summarization
            if user_choice == "4":
                show_summarization()

def login(valid_username: str, valid_password: str) -> bool:
    """
    """

    # is_username_correct = False
    # is_password_correct = False

    input_username = input("Please key your account name: ")

    input_password = input("Please key your password: ")

    if input_username != valid_username or input_password != valid_password:
        return False
    
    return True

def exit() -> None:
    """
    This function finish (ends) the system
    """
    print("==================================\nSee u!")

# copy your codes from task 1 to here if necessary
def show_mark_records(mark_unprocessed: dict) -> None:
    """
    """
    print("==================================")
    print(f"Print {mark_unprocessed}")

def show_summarization() -> None:
    print("==================================")
    print("Print summarization")

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
        user_input = input(prompt)

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