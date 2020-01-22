from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import requests

Builder.load_file('passenger_login.kv')

class PassengerLoginWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def login(self):
        
        phone_number = self.ids.username_field.text

        data = {'username': phone_number, 'password': 'admin'}
        url = 'http://127.0.0.1:8000/api-token-auth/'
        r = requests.post(url = url, data = data).json()
        if 'token' in r.keys():

            x = open('current_passenger.txt', 'w')
            f = open('passenger_token.txt', 'w')
            x.write(phone_number)
            f.write(r['token'])
            f.close()
            x.close()
            self.parent.parent.current = 'scrn_passenger_panel'
        else:
            self.ids.sp.text = 'user does not exist !'

    def go_back(self):
        self.parent.parent.current = 'scrn_passenger_first'

class PassengerLoginApp(App):

    def build(self):

        return PassengerLoginWindow()

if __name__ == "__main__":

    PassengerLoginApp().run()