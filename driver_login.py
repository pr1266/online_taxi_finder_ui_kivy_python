from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import requests


Builder.load_file('driver_login.kv')

class DriverLoginWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def login(self):
        
        phone_number = self.ids.username_field.text

        data = {'username': phone_number, 'password': 'admin'}
        url = 'http://127.0.0.1:8000/api-token-auth/'
        r = requests.post(url = url, data = data).json()
        if 'token' in r.keys():
            f = open('driver_token.txt', 'w')
            f.write(r['token'])
            f.close()
            f = open('current_driver.txt', 'w')
            f.write(phone_number)
            f.close()
            url = f'http://127.0.0.1:8000/driver/{phone_number}'
            header = {'Authorization': 'JWT {}'.format(r['token'])}
            r = requests.get(url = url, headers = header).json()
            if r['permission'] == False:
                self.ids.sp.text = 'not accepted by admin yet !'
            else:
                self.parent.parent.current = 'scrn_driver_panel'
        else:
            self.ids.sp.text = 'user does not exist !'

         
    def go_back(self):
        self.parent.parent.current = 'scrn_driver_first'

class DriverLoginApp(App):

    def build(self):

        return DriverLoginWindow()

if __name__ == "__main__":

    DriverLoginApp().run()