from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import requests
from math import radians, sin, cos, acos
from geopy.distance import distance
from kivy.uix.label import Label

Builder.load_file('add_travel_passenger.kv')

class AddTravelWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def add_travel(self):
        
        # aval token

        f = open('passenger_token.txt', 'r')
        tok = f.readline()
        auth = 'JWT {}'.format(tok)
        header = {'Authorization': auth}

        m = False

        # moshkhasat:
        pick_up = self.ids.pick_up.text
        drop = self.ids.drop.text
        if ',' in drop:
            drop = drop.split(',')
            m = True

        payment_method = self.ids.method.text
        stop = self.ids.stop.text
        stop_ = stop * 1
        # inja lat o lng ro dar biar
        url = 'http://127.0.0.1:8000/get_location/'

        data = {
            'name':pick_up
        }

        r = requests.post(url = url, data = data, headers = header).json()
        id_ = r[0]['pk']
        pick_up_id = r[0]['pk']

        url = 'http://127.0.0.1:8000/location/{}/'.format(id_)
        r = requests.get(url = url, headers = header).json()
        city = r['city']
        
        pick_up_mokhtasat = []
        pick_up_mokhtasat.append(float(r['lat']))
        pick_up_mokhtasat.append(float(r['lng']))
        asli = []
        asli.append(pick_up_mokhtasat)
        drop_mokhtasat = []

        if m == False:
            url = 'http://127.0.0.1:8000/get_location/'

            data = {
            'name':drop
            }
            
            r = requests.post(url = url, data = data, headers = header).json()
            drop_id = r[0]['pk']
            url = 'http://127.0.0.1:8000/location/{}/'.format(drop_id)
            r = requests.get(url = url, headers = header).json()
            drop_mokhtasat.append(float(r['lat']))
            drop_mokhtasat.append(float(r['lng']))

            asli.append(drop_mokhtasat)

        else:
            drop_id2 = []
            for i in drop:
                url = 'http://127.0.0.1:8000/get_location/'

                data = {
                    'name':i,
                }
                temp = []
                r = requests.post(url = url, data = data, headers = header).json()
                x = r[0]['pk']
                drop_id2.append(x)
                url = 'http://127.0.0.1:8000/location/{}/'.format(x)
                r = requests.get(url = url, headers = header).json()
                temp.append(float(r['lat']))
                temp.append(float(r['lng']))

                asli.append(temp)

                del temp

        total = .0

        total_distance = self.calculate(asli)
        print(total_distance)
        # cost
        url = 'http://127.0.0.1:8000/city/{}'.format(city)
        r = requests.get(url = url, headers = header).json()
        per_k = r['price']
        x = open('current_passenger.txt', 'r')
        user_phone = x.readline()
        
        url = 'http://127.0.0.1:8000/passenger/{}'.format(user_phone)
        r = requests.get(url = url , headers = header).json()
        
        user_balance = float(r['balance'])
        cost = (total_distance * per_k) + float(stop_)
        p_m = 'CASH' if user_balance < cost else payment_method
        
        url = 'http://127.0.0.1:8000/createtravel/'

        if m == False:

            data = {
                'cost' : cost,
                'total_stop': stop,
                'payment_status': p_m,
                'passenger': user_phone,
                'pickup': pick_up_id,
                'drop': drop_id,
                'distance': total_distance,
                'end': False,
                'accepted': False,
                'city':city
            }

        else:

            data = {
                'cost' : cost,
                'total_stop': stop,
                'payment_status': p_m,
                'passenger': user_phone,
                'pickup': pick_up_id,
                'drop': drop_id2,
                'distance': total_distance,
                'end': False,
                'accepted': False,
                'city': city
            }

        r = requests.post(url = url, data = data, headers = header).json()

        if 'id' in r.keys():
            x = open('travel_id.txt', 'w')
            x.write(str(r['id']))
            self.parent.parent.current = 'scrn_passenger_travelinfo'

    def calculate(self, arr):
        
        destination = sum([distance(arr[i], arr[i+1]).m for i in range(len(arr) - 1)])
        print(destination)
        return destination/10000

    def go_back(self):

        self.parent.parent.current = 'scrn_passenger_panel'

    def refresh(self):
        f = open('passenger_token.txt', 'r')
        tok = f.readline()
        auth = 'JWT {}'.format(tok)
        header = {'Authorization': auth}

        f.close()

        f = open('current_passenger.txt', 'r')
        self.pass_id = f.readline()
        f.close()

        url = 'http://127.0.0.1:8000/get_common/'

        data = {'id': self.pass_id}

        r = requests.post(url = url, data = data, headers = header).json()
        
        container = self.ids.gd
        container.clear_widgets()
        
        self.ids.info.text = 'Your Common Places :'

        for i in range(len(r)):
            
            common = BoxLayout(size_hint_y = None, height = 30, pos_hint = {'top': 1})
            container.add_widget(common)
            x = r[i]['fields']

            place = x['place']

            url = 'http://127.0.0.1:8000/get_location_2/'
            data = {"name": place}

            req = requests.post(url = url, data = data, headers = header).json()

            place_name = Label(text = req[0]['fields']['place_name'], color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30)
            print(req[0]['fields']['place_name'])
            
            common.add_widget(place_name)



class AddTravelApp(App):

    def build(self):

        return AddTravelWindow()

if __name__ == "__main__":

    AddTravelApp().run()