from typing import Optional
import os
from task7 import TextProcessor

class Role:
    """
    Role class to define an user when login.

    Instance Variables:
        1. user_name(str): user name of user.
        2. access (str): access level of user.
        3. name (str): full name of user.
    """
    def __init__(self, user_name: str, access: str, name: str):
        # YOUR CODES START HERE
        """
        ========== Role Constructor ==========
        
        Initialise a new Role instance (a new user).
        
        Args:
            1. user_name (str): value when init user name of user.
            2. access (str): value when init access level of user.
            3. name (str): value when init name of user.
        """
        self.user_name = user_name
        self.access = access
        self.name = name

    # ==================== GETTERS ====================
    def get_user_name(self):
        # YOUR CODES START HERE
        """
        This function return user name
        Returns:
            user_name (str): user name of instance.
        """
        return self.user_name

    def get_access(self):
        # YOUR CODES START HERE
        """
        This function return access
        Returns:
            access (str): instance's level of access .
        """
        return self.access

    def get_name(self):
        # YOUR CODES START HERE
        """
        This function return name
        Returns:
            name (str): full name of instance.
        """
        return self.name


class RoleBasedVocabSys:
    """
    RoleBasedVocabSys class to define instance of role-based vocabulary system.
    
    Instance Variables:
        1. users_info (dict): Dictionary of collection of users
        2. current_user (Role): current user log in
        3. text_processor (TextProcessor): Text processor
        4. exit (boolean): Check is system exit or not.
    """
    def __init__(
            self,
            users_info,
            stopwords_filepath,
            corpus_filepath,
            idx2label_filepath
    ):
        # YOUR CODES START HERE
        """
        ========== Role Constructor ==========
        
        Initialise a RoleBasedVocabSys instance
        
        Args:
            1. users_info: Dictionary of collection of users.
            2. stopwords_filepath: Path of stopwords file.
            3. corpus_filepath: Path of corpus file.
            4. idx2label_filepath: Path of idx2label file.
        """
        self.users_info = users_info
        self.current_user = None
        self.text_processor = TextProcessor(stopwords_filepath,
                                            corpus_filepath,
                                            idx2label_filepath)

    def start(self):
        # YOUR CODES START HERE
        """
        This function start role based vocabulary system.
        
        Returns:
            This function return nothing. It will start role based vocabulary system and exit
            when user choose option exit.
        """
        user_choice = None
        
        # Main program loop -> until user quit
        while user_choice != "1":
            # Print the menu promt and get user choice
            menu = self.generate_menu()
            print(menu)
            
            user_choice = self.get_user_choice()

            # Login action
            if self.current_user is None:
                if user_choice == "1":
                    print("Exited")
                    continue
                elif user_choice == "2":
                    self.login()
                continue

            # Get user access for different menu choices and word list for according actions
            access = self.current_user.get_access()
            word_freq = self.text_processor.get_word_freq()
            word_list = self.text_processor.get_word_sorted_by_freq(word_freq)

            # Action when user log in for both reader and admin
            if user_choice == "1":
                print("Exited")
                continue
            elif user_choice == "2":
                self.current_user = None # logout - reset current_user state
                print("Logged out.")
                continue
            # Print top 10 frequency words
            elif user_choice == "3":
                print("====================")
                for wrd, frq in word_list[:10]:
                    print(f"{wrd} {frq}")
                print("====================")
                continue
            # Print bottom 10 frequency words
            elif user_choice == "4":
                print("====================")
                for wrd, frq in word_list[-10:]:
                    print(f"{wrd} {frq}")
                print("====================")
                continue
            # Actions of modifying vocabulary only for admin
            if access == "admin":
                # Add vocabulary
                if user_choice == "5":
                    add_file_path = self._check_existing_path("Enter the file path: ")
                    self.text_processor.add_file(add_file_path)
                    print("done.")
                    continue
                # Delete vocabulary
                elif user_choice == "6":
                    delete_file_path = self._check_existing_path("Enter the file path: ")
                    self.text_processor.delete_file(delete_file_path)
                    print("done.")
                    continue

    def _check_existing_path(self,prompt: str) -> str:
        """
        Check if path exists.
        Args:
            prompt (str): prompt string.

        Returns:
            file_path (str): path to file.
        """

        is_valid_path = False
        filepath = ""
        while not is_valid_path:
            filepath = input(prompt).strip()
            if os.path.isfile(filepath):
                is_valid_path = True

        return filepath

    def generate_menu(self) -> str:
        # YOUR CODES START HERE
        """
        This function generate_menu which based on user role
        Returns:
            str: The CLI of system in terminal based on user's role.
        """
        if self.current_user is None:
            return ("Welcome to the Mark system v0.0!\n"
                    "Please Login:\n"
                    "1.Exit\n"
                    "2.Login\n")

        if self.current_user.get_access() == "reader":
            return (
                f"Welcome {self.current_user.get_name()}\n"
                "Please choose one option below:\n"
                "1.Exit\n"
                "2.Logout/Re-Login\n"
                "3.Show top 10 frequency vocabularies\n"
                "4.Show last 10 frequency vocabularies"
            )

        if self.current_user.get_access() == "admin":
            return (
                f"Welcome {self.current_user.get_name()}\n"
                "Please choose one option below:\n"
                "1.Exit\n"
                "2.Logout/Re-Login\n"
                "3.Show top 10 frequency vocabularies\n"
                "4.Show last 10 frequency vocabularies\n"
                "5.Updating Vocabulary for adding\n"
                "6.Updating Vocabulary for excluding"
            )

    def verify_user_choice(self, user_choice) -> bool:
        # YOUR CODES START HERE
        """
        This function verify_user_choice which based on user role.
        
        Args:
            user_choice str: user choice from 1 to 6 and verified by user's role

        Returns:
            bool: True if user choice is valid, False otherwise.
        """
        # List of choice
        choices = ["1", "2", "3", "4", "5", "6"]
        if self.current_user is None:
            return user_choice in choices[:2]
        # Verify for reader
        elif self.current_user.get_access() == "reader":
            return user_choice in choices[:4]
        # Verify for admin
        elif self.current_user.get_access() == "admin":
            return user_choice in choices
        else:
            return False

    def get_user_choice(self):
        """
        This function read a single valid menu choice and dispatch the action based on state/role.
        
        Returns:
            This fucntion return nothing. This return is used for exiting the function
        """
        check_user_valid = False
        while not check_user_valid:
            user_choice = input("Enter your choice: ").strip()
            check_user_valid = self.verify_user_choice(user_choice)
        return user_choice


    def login(self):
        """
        This function allow user login their account when the system starts.
        
        Returns:
            This function return nothing.
        """
        username_in = input("Please key your account name: ").strip()
        password = input("Please key your password: ").strip()

        uname = username_in.lower()
        matched_key = None
        user = None
        for key, value in self.users_info.items():
            if key.lower() == uname:
                matched_key, user = key, value
                break

        if not user:
            print("Login failed: user not found.")
            return
        if user.get("password") != password:
            print("Login failed: wrong password.")
            return

        print(f"Welcome {user['name']}")
        self.current_user = Role(
            user_name=matched_key,
            name=user["name"],
            access=user["role"]
        )


if __name__ == "__main__":
    users_info = {
        "Jueqing": {
            "role": "reader",
            "password": "jueqing123",
            "name": "Jueqing Lu"
        },
        "Trang": {
            "role": "admin",
            "password": "trang123",
            "name": "Trang Vu"
        },
        "land": {
            "role": "admin",
            "password": "landu123",
            "name": "Lan Du"
        }

    }
    a_sys = RoleBasedVocabSys(users_info, stopwords_filepath="data/stop_words_english.txt",
                              corpus_filepath="data/ag_news_test.csv",
                              idx2label_filepath="data/idx2label.json")
    a_sys.start()