from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import requests


Builder.load_file('passenger_common.kv')

class PassengerCommonWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def go_back(self):
        
        self.parent.parent.current = 'scrn_passenger_panel'

    def add_place(self):

        f = open('current_passenger.txt', 'r')
        self.pass_id = f.readline()
        x = open('passenger_token.txt', 'r')
        self.tok = x.readline()
        auth = 'JWT {}'.format(self.tok)
        header = {"Authorization": auth}

        url = 'http://127.0.0.1:8000/get_common/'

        data = {
            'id': self.pass_id
        }

        r = requests.post(url = url, data = data, headers = header).json()

        if len(r) >= 5:
            self.ids.info.text = 'you cant add more common places'
        else:
            place_name = self.ids.place.text
            
            url = 'http://127.0.0.1:8000/get_location/'

            data = {
                'name':place_name,
            }

            r = requests.post(url = url, data = data, headers = header).json()
            id_ = r[0]['pk']
            
            data = {
                'passenger': self.pass_id,
                'place': id_
            }

            url = 'http://127.0.0.1:8000/createcommonplace/'

            r = requests.post(url = url, data = data, headers = header).json()
            if 'id' in r.keys():
                self.parent.parent.current = 'scrn_passenger_panel'

class PassengerCommonApp(App):

    def build(self):

        return PassengerCommonWindow()

if __name__ == "__main__":

    PassengerCommonApp().run()