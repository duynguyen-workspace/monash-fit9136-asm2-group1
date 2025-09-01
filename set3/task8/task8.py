from typing import Optional
import os
from task7 import TextProcessor


class Role:
    def __init__(self, user_name: str, access: str, name: str):
        # YOUR CODES START HERE
        pass
    
    def get_user_name(self):
        # YOUR CODES START HERE
        pass
    
    def get_access(self):
        # YOUR CODES START HERE
        pass

    def get_name(self):
        # YOUR CODES START HERE
        pass


class RoleBasedVocabSys:
    
    def __init__(
        self,
        users_info,
        stopwords_filepath,
        corpus_filepath,
        idx2label_filepath
        ):
        
        # YOUR CODES START HERE
        # replace with correct initialization
        self.users_info = None
        self.current_user = None
        self.text_processor = None
        
    def start(self):
        # YOUR CODES START HERE
        pass
          
    def generate_menu(self) -> str:
        # YOUR CODES START HERE
        pass
    
    def verify_user_choice(self, user_choice) -> bool:
        # YOUR CODES START HERE
        pass
    
    def get_user_choice(self):
        # YOUR CODES START HERE
        pass
    
    def login(self):
        # YOUR CODES START HERE
        pass
            

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
    a_sys = RoleBasedVocabSys(users_info)
    a_sys.start()
    
