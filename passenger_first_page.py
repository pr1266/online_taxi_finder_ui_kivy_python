from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file('passenger_first_page.kv')

class PassengerFirstPage(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def go_to_register(self):
        self.parent.parent.current = 'scrn_passenger_register'
    
    def go_to_login(self):
        self.parent.parent.current = 'scrn_passenger_login'

    def go_back(self):
        self.parent.parent.current = 'scrn_first_page'
        
class PassengerFirstApp(App):

    def build(self):

        return PassengerFirstPage()

if __name__ == "__main__":

    PassengerFirstApp().run()