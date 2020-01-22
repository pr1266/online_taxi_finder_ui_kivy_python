from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
import requests

Builder.load_file('driver_travel_info.kv')


class DriverTravelInfoWindow(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def cancel(self):
        
        auth = 'JWT {}'.format(self.tok)
        header = {
            'Authorization': auth
        }

        url = 'http://127.0.0.1:8000/travel/{}/delete'.format(self.tr_id)
        r = requests.delete(url = url, headers = header)

        self.parent.parent.current = 'scrn_travel_view'

    def end(self):
        
        auth = 'JWT {}'.format(self.tok)
        header = {
            'Authorization': auth
        }

        data = {
            'passenger': self.r['passenger'],
            'driver': self.phone_number,
            'cost': self.r['cost'],
            'distance': self.r['distance'],
            'total_stop': self.r['total_stop'],
            'payment_status': self.r['payment_status'],
            'accepted': True,
            'end': True,
            'pickup': self.r['pickup'],
            'drop': self.r['drop'],
            'city': self.r['city']
        }

        url = 'http://127.0.0.1:8000/travel/{}/update/'.format(self.tr_id)
        r = requests.put(url = url , data = data, headers = header).json()

        cost = r['cost']

        if 'id' in r.keys():
            
            f = open('driver_vote.txt', 'w')
            f.write(str(r['passenger']))
            f.close()


            if r['payment_status'] == 'ONLINE' or r['payment_status'] == 'online':
                
                url = 'http://127.0.0.1:8000/passenger/{}/'.format(r['passenger'])
                new_req = requests.get(url = url, headers = header).json()

                if new_req['balance'] > r['cost']:
                    url = 'http://127.0.0.1:8000/driver/{}/'.format(r['driver'])
                    req = requests.get(url = url, headers = header).json()
                    print(req)
                    curr_balance = req['balance']
                    new_balance = curr_balance + cost
                    new_balance_2 = curr_balance - cost
                    
                    print(new_balance)
                    
                    url = 'http://127.0.0.1:8000/driver/{}/update/'.format(r['driver'])
                    data = {
                    'user': r['driver'],
                    'balance': int(new_balance),
                    'permission': False
                    }
                    req_2 = requests.put(url = url, data = data, headers = header).json()
                    print(req_2)
                    url = 'http://127.0.0.1:8000/passenger/{}/update/'.format(r['passenger'])
                    data = {
                    'user': r['passenger'],
                    'balance': float(new_balance_2),
                    'permission': False
                    }
                    req_3 = requests.put(url = url, data = data, headers = header).json()
            self.parent.parent.current = 'scrn_driver_panel'
        

    def refresh(self):

        f = open('driver_travel.txt', 'r')
        self.tr_id = f.readline()
        f.close()

        x = open('driver_token.txt', 'r')
        self.tok = x.readline()
        x.close()

        w = open('current_driver.txt', 'r')
        self.phone_number = w.readline()
        w.close()

        auth = 'JWT {}'.format(self.tok)
        header = {
            'Authorization': auth
        }

        url = 'http://127.0.0.1:8000/travel/{}'.format(self.tr_id)

        r = requests.get(url = url, headers = header).json()
        self.r = r
        container = self.ids.gd1

        details = BoxLayout(size_hint_y = None, height = 30, pos_hint = {'top': 1})

        container.clear_widgets()
        container.add_widget(details)

        method = Label(text = str(r['payment_status']), size_hint_y = None, height = 30, color = (.06, .45 , .45 , 1), bold = True)
        url = 'http://127.0.0.1:8000/get_location_2/'
        print(r['pickup'])
        data = {'name': r['pickup']}
        
        req = requests.post(url = url, data = data, headers = header).json()
        print("REQ : ")
        print(req)
        pickup = Label(text = req[0]['fields']['place_name'], size_hint_y = None, height = 30, color = (.06, .45 , .45 , 1), bold = True)
        cost = Label(text = str(r['cost'])[:3], size_hint_y = None, height = 30, color = (.06, .45 , .45 , 1), bold = True)
        distance = Label(text = str(r['distance'])[:3], size_hint_y = None, height = 30, color = (.06, .45 , .45 , 1), bold = True)
        details.add_widget(method)
        details.add_widget(pickup)
        details.add_widget(distance)
        details.add_widget(cost)
        

class DriverTravelInfoApp(App):

    def build(self):

        return DriverTravelInfoWindow()

if __name__ == '__main__':

    DriverTravelInfoApp().run()