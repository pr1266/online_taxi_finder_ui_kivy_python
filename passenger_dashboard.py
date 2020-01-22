from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
import requests


Builder.load_file('passenger_dashboard.kv')

class PassengerPanelWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def charge(self):
        
        self.parent.parent.current = 'scrn_passenger_charge'

    def new_travel(self):

        self.parent.parent.current = 'scrn_passenger_travel'

    def edit_info(self):
        
        self.parent.parent.current = 'scrn_passenger_edit'
    
    def add_common(self):
        
        self.parent.parent.current = 'scrn_passenger_common'

    def refresh(self):
        
        x = open('passenger_token.txt', 'r')
        self.tok = x.readline()
        x.close()

        auth = 'JWT {}'.format(self.tok)

        url = 'http://127.0.0.1:8000/get_travel_passenger/'

        header = {'Authorization': auth}

        f = open('current_passenger.txt', 'r')
        self.pass_id = f.readline()
        f.close()

        data = {'id': self.pass_id}

        r = requests.post(url = url, headers = header, data = data).json()
        self.r = r
        container = self.ids.gd
        container.clear_widgets()

        #count
        url = 'http://127.0.0.1:8000/travel_count_passenger/'
        data = {'id': self.pass_id}
        r = requests.post(url = url, data = data, headers = header).json()

        self.ids.travel_count.text = str(r['result'])

        #balance
        url = 'http://127.0.0.1:8000/passenger/{}'.format(self.pass_id)
        r = requests.get(url = url, headers = header).json()
        self.ids.balance.text = str(r['balance'])
        #vote

        """url = 'http://127.0.0.1:8000/vote/'
        data = {'id': self.pass_id}
        r = requests.post(url = url, data = data, headers = header).json()"""

        self.ids.vote.text = str(0)

        for i in range(len(self.r)):
            
            x = self.r[i]['fields']
            details = BoxLayout(size_hint_y = None, height = 30, pos_hint = {'top': 1})
            container.add_widget(details)    
            print(x)

            url = 'http://127.0.0.1:8000/user/{}'.format(x['driver'])
            req = requests.get(url = url, headers = header).json()
            if req['first_name'] == None:
                driver = Label(text = '', color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .2)
            else:
                driver = Label(text = req['first_name'] + ' ' + req['last_name'], color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .2)
            if x['date'] != None:
                date = Label(text = x['date'], color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .2)
            else:
                date = Label(text = '', color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .2)
           
            url = 'http://127.0.0.1:8000/location/{}'.format(x['pickup'])
            req = requests.get(url = url, headers = header).json()
            pickup = Label(text = str(req['place_name']), color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .2)
            total_distance = Label(text = str(x['distance'])[:4], color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .2)
            total_stop = Label(text = str(x['total_stop']), color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .1)
            cost = Label(text = str(x['cost'])[:4], color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .1)

            details.add_widget(driver)
            details.add_widget(pickup)
            details.add_widget(total_distance)
            details.add_widget(total_stop)
            details.add_widget(date)
            details.add_widget(cost)


class PassengerPanelApp(App):

    def build(self):

        return PassengerPanelWindow()

if __name__ == "__main__":

    PassengerPanelApp().run()