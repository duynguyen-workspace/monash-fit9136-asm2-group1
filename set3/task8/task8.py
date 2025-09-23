from typing import Optional
import os
from task7 import TextProcessor

WELCOME_MESSAGE = "Welcome to the Mark system v0.0!"


class Role:
    def __init__(self, user_name: str, access: str, name: str):
        # YOUR CODES START HERE
        """Role class store and return the user's user_name
        display name, and acess level"""
        self.user_name = user_name
        self.access = access
        self.name = name

    def get_user_name(self):
        # YOUR CODES START HERE
        """This function return user name"""
        return self.user_name

    def get_access(self):
        # YOUR CODES START HERE
        """This function return access"""
        return self.access

    def get_name(self):
        # YOUR CODES START HERE
        """This function return name"""
        return self.name


class RoleBasedVocabSys:

    def __init__(
            self,
            users_info,
            stopwords_filepath,
            corpus_filepath,
            idx2label_filepath
    ):
        """Define user"""
        # YOUR CODES START HERE
        # replace with correct initialization
        self.users_info = users_info
        self.current_user = None
        self.text_processor = TextProcessor(stopwords_filepath,
                                            corpus_filepath,
                                            idx2label_filepath)
        self.exit = False

    def start(self):
        # YOUR CODES START HERE
        while not self.exit:
            menu = self.generate_menu()
            print(menu)
            self.get_user_choice()

    def generate_menu(self) -> str:
        # YOUR CODES START HERE
        """This function generate_menu"""
        if self.current_user is None:
            return ("Welcome to the Mark system v0.0!\n"
                    "Please Login:\n"
                    "1.Exit\n"
                    "2.Login\n")
        if self.current_user.get_access() == "reader":
            return (
                "Please choose one option below:\n"
                "1.Exit\n"
                "2.Logout / Re-Login\n"
                "3.Show top 10 frequency vocabularies\n"
                "4.Show last 10 frequency vocabularies"
            )
        if self.current_user.get_access() == "admin":
            return (
                "Please choose one option below:\n"
                "1.Exit\n"
                "2.Logout / Re-Login\n"
                "3.Show top 10 frequency vocabularies\n"
                "4.Show last 10 frequency vocabularies"
            )

    def verify_user_choice(self, user_choice) -> bool:
        # YOUR CODES START HERE
        choices = ["1", "2", "3", "4", "5", "6"]
        if self.current_user is None:
            return user_choice in choices[:2]
        elif self.current_user.get_access() == "reader":
            return user_choice in choices[:5]
        elif self.current_user.get_access() == "admin":
            return user_choice in choices
        else:
            return False

    def get_user_choice(self):
        """Read a single valid menu choice and dispatch the action based on state/role."""

        while True:
            user_choice = input("Enter your choice: ").strip()
            if self.verify_user_choice(user_choice):
                break
            print("Invalid choice. Please try again.")

        if self.current_user is None:
            if user_choice == "1":
                print("Exited")
                self.exit = True
            elif user_choice == "2":
                self.login()
            return


        access = self.current_user.get_access()

        if user_choice == "1":
            print("Exited")
            self.exit = True
            return
        elif user_choice == "2":
            self.current_user = None
            print("Logged out.")
            return
        elif user_choice == "3":
            # TODO: show vocab
            print("Showing vocabulary...")
            return
        elif user_choice == "4":
            # TODO: top 10 vocab

            print("Showing statistics (top/bottom 10)...")
            return

        if access == "admin":
            if user_choice == "5":
                path = input("Path to add: ").strip()

                self.text_processor.add_file(path)
                print("Vocabulary updated (added).")

                return
            elif user_choice == "6":
                path = input("Path to remove: ").strip()

                self.text_processor.delete_file(path)
                print("Vocabulary updated (removed).")




    def login(self):
        username_in = input("Please key your account name: ").strip()
        password = input("Please key your account password: ").strip()

        uname = username_in.lower()
        matched_key = None
        user = None
        for k, v in self.users_info.items():
            if k.lower() == uname:
                matched_key, user = k, v
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