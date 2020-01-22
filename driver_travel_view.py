from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
import requests

Builder.load_file('driver_travel_view.kv')

class TravelViewWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def go_back(self):

        self.parent.parent.current = 'scrn_driver_panel'

    def refresh(self):

        f = open('current_driver.txt', 'r')
        self.pass_id = f.readline()
        x = open('driver_token.txt', 'r')
        self.tok = x.readline()
        auth = 'JWT {}'.format(self.tok)
        header = {"Authorization": auth}

        # city ro begir
        url = 'http://127.0.0.1:8000/user/{}'.format(self.pass_id)

        r = requests.get(url = url, headers = header).json()

        self.city = r['city']

        # hala travel hasho begir
        url = 'http://127.0.0.1:8000/get_travel_city/'
        data = {'id': self.city}
        r = requests.post(url = url, data = data, headers = header).json()
        print("R : ")
        print(r)
        container = self.ids.gd

        container.clear_widgets()

        for i in range(len(r)):

            details = BoxLayout(size_hint_y = None, height = 30, pos_hint = {'top': 1})
            container.add_widget(details)
            x = r[i]['fields']

            get_travel = Button(size_hint_y = None, height = 30, text = 'Accept', background_normal = '', background_color = (.06 , .25 , .25 , 1), size_hint_x = .2)
            get_travel.bind(on_release = lambda btn : self.accept(r[i]['pk']))
            cost = Label(text = str(x['cost'])[:3], color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .1)
            
            url = 'http://127.0.0.1:8000/get_location_2/'
            data = {'name': x['pickup']}
            req = requests.post(data = data, url = url, headers = header).json()
            pick_name = req[0]['fields']['place_name']
            pickup = Label(text = pick_name, color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .2)

            total_distance = Label(text = str(x['distance'])[:3], color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .2)
            total_stop = Label(text = str(x['total_stop']), color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30, size_hint_x = .1)
            
            details.add_widget(pickup)
            details.add_widget(total_distance)
            details.add_widget(total_stop)
            details.add_widget(cost)
            details.add_widget(get_travel)

    def accept(self, id):
        
        f = open('driver_travel.txt', 'w')
        f.write(str(id))
        f.close()
        self.parent.parent.current = 'scrn_driver_travelinfo'

class TravelViewApp(App):

    def build(self):

        return TravelViewWindow()


if __name__ == '__main__':

    TravelViewApp().run()