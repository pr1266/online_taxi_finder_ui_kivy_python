from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import requests

Builder.load_file('passenger_register.kv')

class PassengerRegisterWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def register(self):

        username = self.ids.phone_number.text
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        city = self.ids.city.text

        data = {'username':'09169561266', 'password': 'admin'}
        url = 'http://127.0.0.1:8000/api-token-auth/'
        r = requests.post(url = url, data = data).json()

        tok = r['token']
        print(tok)
        auth = 'JWT {}'.format(tok)
        header = {"Authorization": auth}

        #inaja vas shahr
        url = 'http://127.0.0.1:8000/city/{}'.format(city)
        
        r = requests.get(url = url, headers = header).json()
        print(r)
        city_ = r['city_name']
        #inja user ro besaz
        data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'city': city_,
            'password': 'admin',
            'is_active': True
        }

        url = 'http://127.0.0.1:8000/createuser/'
        r = requests.post(url = url, data = data, headers = header).json()
        username = r['username']

        #inja passenger ro

        url = 'http://127.0.0.1:8000/createpassenger/'
        data = {
            'user': username
        }

        r = requests.post(url = url, data = data, headers = header).json()
        if 'id' in r.keys():
            self.parent.parent.current = 'scrn_passenger_login'
        else:
            pass

        


    def go_back(self):
        self.parent.parent.current = 'scrn_passenger_first'

class PassengerRegisterApp(App):

    def build(self):

        return PassengerRegisterWindow()

if __name__ == "__main__":

    PassengerRegisterApp().run()