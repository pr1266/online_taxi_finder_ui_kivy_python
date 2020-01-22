from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file('driver_first_page.kv')

class DriverFirstPage(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def go_to_register(self):
        self.parent.parent.current = 'scrn_driver_register' 
    def go_to_login(self):
        self.parent.parent.current = 'scrn_driver_login' 
    def go_back(self):
        self.parent.parent.current = 'scrn_first_page'

class DriverFirstApp(App):

    def build(self):

        return DriverFirstPage()

if __name__ == "__main__":

    DriverFirstApp().run()