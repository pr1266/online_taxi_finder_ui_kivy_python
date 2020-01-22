from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import requests 

Builder.load_file('driver_register.kv')

class DriverRegisterWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def register(self):
         
        username = self.ids.phone_number.text
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        city = self.ids.city.text

        """f = open('token.txt', 'r')
        tok = f.readline()
        auth = 'JWT {}'.format(tok)
        header = {'Authorization': auth}"""

        data = {'username':'09169561266', 'password': 'admin'}
        url = 'http://127.0.0.1:8000/api-token-auth/'
        r = requests.post(url = url, data = data).json()

        tok = r['token']
        auth = 'JWT {}'.format(tok)
        header = {"Authorization": auth}

        url = 'http://127.0.0.1:8000/city/{}/'.format(city)
        #inaja vas shahr
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
        if r['username'] != 'user with this username already exists.':
            username = r['username']
            car_model = self.ids.car.text
            car_license = self.ids.car_l.text
            #inja mashino besaz
            url = 'http://127.0.0.1:8000/createcar/'
            data = {
                'license': car_license,
                'model': car_model,
                'owner': username
            }
            r = requests.post(url = url, data = data, headers = header).json()
            car_id = r['id']
            #inja driver ro besaz
            url = 'http://127.0.0.1:8000/createdriver/'
            data = {
                'user': username,
            }

            r = requests.post(url = url, data = data, headers = header).json()
            if 'id' in r.keys():
                self.parent.parent.current = 'scrn_driver_login'
            else:
                pass
    
    def go_back(self):
        self.parent.parent.current = 'scrn_driver_first'
class DriverRegisterApp(App):

    def build(self):

        return DriverRegisterWindow()

if __name__ == "__main__":

    DriverRegisterApp().run()