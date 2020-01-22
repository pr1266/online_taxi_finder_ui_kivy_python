from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import requests

Builder.load_file('driver_edit.kv')

class DriverEditWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def edit(self):
        
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        city = self.ids.city.text

    
        f = open('current_driver.txt', 'r')
        self.pass_id = f.readline()
        x = open('driver_token.txt', 'r')
        self.tok = x.readline()
        auth = 'JWT {}'.format(self.tok)
        header = {"Authorization": auth}

        data = {
            'username': self.pass_id,
            'password': 'admin',
            'first_name': first_name,
            'last_name': last_name,
            'city': city,
            'is_active': True
        }

        url = 'http://127.0.0.1:8000/user/{}/update/'.format(self.pass_id) 
        r = requests.put(url = url, data = data, headers = header).json()

        if 'username' in r.keys():
            self.parent.parent.current = 'scrn_driver_panel'

    def go_back(self):

        self.parent.parent.current = 'scrn_driver_panel'

class DriverEditApp(App):

    def build(self):

        return DriverEditWindow()

if __name__ == '__main__':

    DriverEditApp().run()