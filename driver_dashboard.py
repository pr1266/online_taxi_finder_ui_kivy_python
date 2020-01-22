from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
import requests


Builder.load_file('driver_dashboard.kv')

class DriverPanelWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
    
    def add_car(self):
        
        # ye safhe jadid baz kon
        self.parent.parent.current = 'scrn_driver_car'
    
    def edit_info(self):
        
        self.parent.parent.current = 'scrn_driver_edit'

    def new_travel(self):

        self.parent.parent.current = 'scrn_travel_view'
    
    def refresh(self):

        x = open('driver_token.txt', 'r')
        self.tok = x.readline()
        x.close()

        auth = 'JWT {}'.format(self.tok)

        url = 'http://127.0.0.1:8000/get_travel_driver/'

        header = {'Authorization': auth}

        f = open('current_driver.txt', 'r')
        self.pass_id = f.readline()
        f.close()

        data = {'id': self.pass_id}

        r = requests.post(url = url, headers = header, data = data).json()
        self.r = r
        container = self.ids.gd
        container.clear_widgets()

        #count
        url = 'http://127.0.0.1:8000/travel_count_driver/'
        data = {'id': self.pass_id}
        r = requests.post(url = url, data = data, headers = header).json()

        self.ids.travel_count.text = str(r['result'])

        #balance
        url = 'http://127.0.0.1:8000/driver/{}'.format(self.pass_id)
        r = requests.get(url = url, headers = header).json()
        self.ids.balance.text = str(r['balance'])
        #vote

      

        self.ids.vote.text = str(0)

        for i in range(len(self.r)):
            
            x = self.r[i]['fields']
            details = BoxLayout(size_hint_y = None, height = 30, pos_hint = {'top': 1})
            container.add_widget(details)    
            
            if x['passenger'] == None:
                driver = Label(text = '', color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .2)
            else:
                url = 'http://127.0.0.1:8000/user/{}'.format(x['passenger'])

                req = requests.get(url = url, headers = header).json()
                passenger_name = req['first_name'] + " " + req['last_name']
                driver = Label(text =passenger_name, color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .2)
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


class DriverPanelApp(App):

    def build(self):

        return DriverPanelWindow()

if __name__ == "__main__":

    DriverPanelApp().run()