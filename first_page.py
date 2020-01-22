from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file('first_page.kv')

class MainWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def go_to_driver(self):
        self.parent.parent.current = 'scrn_driver_first' 
    
    def go_to_passenger(self):
        self.parent.parent.current = 'scrn_passenger_first'
     

class MainApp(App):

    def build(self):

        return MainWindow()

if __name__ == '__main__':

    MainApp().run()