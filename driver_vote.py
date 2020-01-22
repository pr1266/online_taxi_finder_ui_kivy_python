from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label 
from kivy.lang import Builder

Builder.load_file('driver_vote.kv')

class DriverVoteWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def refresh(self):

        pass 

    def vote(self):

        pass 


class DriverVoteApp(App):

    def build(self):

        return DriverVoteWindow()

if __name__ == '__main__':

    DriverVoteApp().run()