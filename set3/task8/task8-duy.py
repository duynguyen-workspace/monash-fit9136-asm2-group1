from typing import Optional
import os
from task7 import TextProcessor


class Role:
    """ Role Class """

    def __init__(self, user_name: str, access: str, name: str):
        """
        """
        self.user_name = user_name
        self.access = access
        self.name = name
    
    def get_user_name(self):
        """
        """
        return self.user_name
        
    
    def get_access(self):
        """
        """
        return self.access

    def get_name(self):
        """
        """
        return self.name


class RoleBasedVocabSys:
    """ """ 
    
    def __init__(
        self,
        users_info,
        stopwords_filepath,
        corpus_filepath,
        idx2label_filepath
        ):
        
        # YOUR CODES START HERE
        # replace with correct initialization
        self.users_info = users_info
        self.current_user = None
        self.text_processor = TextProcessor(stopwords_filepath, corpus_filepath, idx2label_filepath)
        
    def start(self):
        # YOUR CODES START HERE

        # STATES 
        user_choice = None

        # MAIN MENU starts
        while user_choice != "1":

            self.generate_menu()
            
            # Get user's input
            user_choice = self.get_user_choice()
    
            # @Action 1: Exit Program
            if user_choice == "1":
                self.exit()
                
            # @Action 2: Login / Relogin
            if user_choice == "2":
                if not self.current_user:
                    self.login()
                else:
                    self.current_user = None # logout -> reset login state
                    print("You have logged off successfully!")
                    
            # --- ONLY AVAILABLE FOR READER AND ADMIN USER ---
            if self.current_user and self.current_user.access in ["reader", "admin"]:
                # @Action 3: Show top 10 freqency vocabularies
                if user_choice == "3":
                    self.show_top_10_vocab_freq()
                
                # @Action 4: Show bottom 10 frequency vocabularies
                if user_choice == "4":
                    self.show_bottom_10_vocab_freq()

            if self.current_user and self.current_user.access == "admin":
                # @Action 5: Updating with add file
                if user_choice == "5":
                    self.text_processor.add_file("data/add.csv")
                    print("Vocabulary updated (added).")
                
                # @Action 6: Updating with delete file
                if user_choice == "6":
                    self.text_processor.delete_file("data/delete.csv")
                    print("Vocabulary updated (deleted).")

    def show_top_10_vocab_freq(self) -> None:
        """
        """
        # self.text_processor.load()
        word_freq = self.text_processor.get_word_freq()
    
    def show_bottom_10_vocab_freq(self) -> None:
        """
        """
        pass

    def exit(self) -> None:
        """
        This function finish (ends) the system

        Params: 
            None

        Return:
            None: the function only output a message to the console
        """
        print("==================================\nSee u!")

    def logout(self) -> None:
        """
        """
        self.current_user = None # logout -> reset login state
        print("You have logged off successfully!")

    def generate_menu(self) -> str:
        # YOUR CODES START HERE
        DEFAULT_MENU_PROMPT = "Welcome to the Mark system v0.0!\nPlease Login:\n1.Exit\n2.Login"

        if not self.current_user:
            print(DEFAULT_MENU_PROMPT)
        
        if self.current_user and self.current_user.access == "reader":
            READER_MENU_PROMPT = f'Welcome {self.current_user.name}\nPlease choose one option below:\n1.Exit\n2.Logout/Re-Login\n3.Show top 10 frequency vocabularies\n4.Show last 10 frequency vocabularies'
            print(READER_MENU_PROMPT)

        if self.current_user and self.current_user.access == "admin":
            ADMIN_MENU_PROMPT = f'Welcome {self.current_user.name}\nPlease choose one option below:\n1.Exit\n2.Logout/Re-Login\n3.Show top 10 frequency vocabularies\n4.Show last 10 frequency vocabularies\n5.Updating Vocabulary for adding\n6.Updating Vocabulary for excluding\nEnter your choice:'
            print(ADMIN_MENU_PROMPT)
        
    
    def verify_user_choice(self, user_choice) -> bool:
        """
        """
        if not user_choice.isdigit():
            return False

        user_choice = int(user_choice)
        
        if self.current_user is None:
            if user_choice == 1 or user_choice == 2:
                return True
        else:
            if self.current_user.access == "reader" and user_choice in [1, 2, 3, 4]:
                return True
            elif self.current_user.access == "admin" and user_choice in [1, 2, 3, 4, 5, 6]:
                return True

        return False
    
    def get_user_choice(self):
        """
        """
        is_input_valid = False 

        while not is_input_valid:
            # print("==================================") # seperator
            # print(prompt, end="")

            user_input = input("Enter your choice: ")
            
            if self.verify_user_choice(user_input):
                is_input_valid = True
    
        return user_input
    
    def login(self):
        """
        This function performs the login action 

        Params:
            1. valid_username: <str> user's username 
            2. valid_password: <str> user's password

        Return:
            bool: the login status (success or failed)
        """
        print("==================================") # seperator

        input_username = input("Please key your account name: ")
        input_password = input("Please key your password: ")

        user_found = None

        for username, info in self.users_info.items():
            if input_username.lower() == username.lower():
                print("YESSSSSS")
                if input_password == info.get('password'):
                    user_found = username
                    break
        
        print(user_found)

        if user_found:
            user_info = self.users_info[user_found]
            self.current_user = Role(user_found, user_info.get('role'), user_info.get('name'))
        else:
            print("==================================") # seperator
            print("Incorrect username or password!")
            
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
    a_sys = RoleBasedVocabSys(
        users_info, 
        stopwords_filepath="data/stop_words_english.txt",
        corpus_filepath="data/ag_news_test.csv",
        idx2label_filepath="data/idx2label.json"
        )
    a_sys.start()



    