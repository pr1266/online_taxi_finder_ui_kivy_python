from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import requests

Builder.load_file('driver_add_car.kv')

class DriverCarWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def go_back(self):
        
        self.parent.parent.current = 'scrn_driver_panel'

    def add_car(self):

        f = open('current_driver.txt', 'r')
        self.pass_id = f.readline()
        x = open('driver_token.txt', 'r')
        self.tok = x.readline()
        auth = 'JWT {}'.format(self.tok)
        header = {"Authorization": auth}

        url = 'http://127.0.0.1:8000/get_car/'

        data = {
            'id': self.pass_id
        }

        r = requests.post(url = url, data = data, headers = header).json()

        if len(r) >= 3:
            self.ids.info.text = 'you cant add more cars'
        else:
            model = self.ids.model.text
            license_ = self.ids.license.text

            url = 'http://127.0.0.1:8000/createcar/'

            data = {
                'model': model,
                'license': license_,
                'owner': self.pass_id
            }

            r = requests.post(url = url, data = data, headers = header).json()
            
            if 'id' in r.keys():
                self.parent.parent.current = 'scrn_driver_panel'

class DriverCarWindowApp(App):

    def build(self):

        return DriverCarWindow()

if __name__ == "__main__":

    DriverCarWindowApp().run()