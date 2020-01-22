from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import requests
from kivy.uix.label import Label

Builder.load_file('passenger_travel_info.kv')

class TravelInfoWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def refresh(self):

        x = open('travel_id.txt', 'r')
        self.tr_id = x.readline()
        url = 'http://127.0.0.1:8000/travel/{}/'.format(self.tr_id)
        
        
        f = open('passenger_token.txt', 'r')
        self.tok = f.readline()
        auth = 'JWT {}'.format(self.tok)

        header = {'Authorization': auth}
        w = open('current_passenger.txt', 'r')
        self.pass_id = w.readline()

        x.close()
        w.close()
        f.close()

        # get info
        r = requests.get(url = url, headers = header).json()
        if r['end'] == True:

            self.parent.parent.current = 'scrn_passenger_panel'

        else:
            container = self.ids.gd
            container.clear_widgets()

            details = BoxLayout(size_hint_y = None, height = 30, pos_hint = {'top':1})
            container.add_widget(details)

            total_distance = r['distance']
            total_stop = r['total_stop']
            driver = r['driver']
            payment_status = r['payment_status']
            cost = float(r['cost'])
            url = 'http://127.0.0.1:8000/passenger/{}'.format(self.pass_id)
            r = requests.get(url = url, headers = header).json()
            if r['offer'] != None:
                x = float(r['offer'])
            #offer
                if x != 0:
                    cost -= x * .01 * cost

            Cost = Label(text = str(cost)[:3], color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30)
            Distance = Label(text = str(total_distance)[:4], color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30)
            Stop = Label(text = str(total_stop), color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30)
            if driver == None:
                Driver = Label(text = '', color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30)
            else:
                Driver = Label(text = str(driver), color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30)
            Payment = Label(text = payment_status, color = (.06, .45 , .45 , 1), bold = True, size_hint_y = None, height = 30)



            details.add_widget(Driver)
            details.add_widget(Distance)
            details.add_widget(Stop)
            details.add_widget(Cost)
            details.add_widget(Payment)

    
    def cancel(self):
        
        print(self.tok)
        print(self.tr_id)
        url = 'http://127.0.0.1:8000/travel/{}/delete'.format(self.tr_id)

        auth = 'JWT {}'.format(self.tok)
        header = {'Authorization': auth}

        r = requests.delete(url = url, headers = header)
        print(r)
        self.parent.parent.current = 'scrn_passenger_panel'
        


class TravelInfoApp(App):

    def build(self):
        return TravelInfoWindow()

if __name__ == '__main__':

    TravelInfoApp().run()