from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import requests


Builder.load_file('passenger_charge.kv')

class PassengerChargeWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def charge(self):

        charge = self.ids.charge.text
        if float(charge) > 5:
            self.ids.info.text = 'invalid charge'
        else:
            auth = 'JWT {}'.format(self.tok)
            header = {"Authorization": auth}
            url = 'http://127.0.0.1:8000/passenger/{}/update/'.format(self.pass_id)
            x = self.pass_balance + float(charge)
            data = {
                'user': self.pass_id,
                'balance': x
            }
            r = requests.put(url = url, headers = header, data = data).json()
            
            self.parent.parent.current = 'scrn_passenger_panel'
    
    def go_back(self):

        self.parent.parent.current = 'scrn_passenger_panel'

    def refresh(self):

        f = open('current_passenger.txt', 'r')
        self.pass_id = f.readline()
        x = open('passenger_token.txt', 'r')
        self.tok = x.readline()
        auth = 'JWT {}'.format(self.tok)
        header = {"Authorization": auth}
        url = 'http://127.0.0.1:8000/passenger/{}'.format(self.pass_id)
        r = requests.get(url = url, headers = header).json()
        balance = r['balance']
        self.pass_balance = balance
        self.ids.curr_balance.text = str(balance)

class PassengerChargeApp(App):

    def build(self):

        return PassengerChargeWindow()

if __name__ == "__main__":

    PassengerChargeApp().run()