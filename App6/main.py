import json
import glob
import random
from hoverable import HoverBehavior
from pathlib import Path
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from datetime import datetime

Builder.load_file('design.kv')

class LoginScreen(Screen): # Screen is parent, LoginScreen is child (Inheritance)
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def log_in(self, un, pwd):

        with open("users.json") as my_file:
            db = json.load(my_file)
        
        if un in db and db[un]['password'] == pwd:
            print("Logged in!")
            self.manager.current = "login_screen2"
        else:
            self.ids.wrong_id.text = "User name or password is incorrect!\nTry Again"

class LoginScreen2(Screen):
    def log_out(self):
        self.manager.transition.direction = 'up'
        self.manager.current = "login_screen"

    def response(self, feel):
        feel = feel.lower()
        get_file = glob.glob("quotes/*txt")
        get_file = [Path(filename).stem for filename in get_file]

        if feel in get_file:
            with open(f"quotes/{feel}.txt", encoding="utf8") as mf:
              quotes = mf.readlines() #stores as list
        
            # print(quotes)
            self.ids.quote.text = random.choice(quotes)

        else:
            self.ids.quote.text = "Try to write happy, sad or unloved."

class SignUpScreen(Screen):
    def new_user(self, un, pwd):
        with open("users.json") as my_file:
            #db = my_file.read() only reads the file
            db = json.load(my_file) #takes a file object and convert it into a Python dictionary 

        # for key un in db we store another dict.
        db[un] = {'username': un, 'password': pwd, 'created' : datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        print(db)

        with open("users.json", 'w') as my_file:
            json.dump(db, my_file)

        self.manager.current = "sign_up_screen2"

class SignUpScreen2(Screen):
    def sus(self):
        self.manager.transition.direction = 'up'
        self.manager.current = "login_screen"

class RootWidget(ScreenManager):
    pass

class ImageButton(HoverBehavior, ButtonBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
        MainApp().run() 
