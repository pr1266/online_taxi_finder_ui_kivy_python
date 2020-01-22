from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label 
from kivy.lang import Builder

Builder.load_file('passenger_vote.kv')

class PassengerVoteWindow(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def refresh(self):

        pass 

    def vote(self):

        number = self.ids.integer.text
        string = self.ids.vote.text

        f = open('current_passenger.txt', 'r')
        self.pass_id = f.readline()
        x = open('passenger_token.txt', 'r')
        self.tok = x.readline()
        auth = 'JWT {}'.format(self.tok)
        header = {"Authorization": auth}

        url = 'http://127.0.0.1:8000/createvote/'

        data = {
            'id': self.pass_id
        }

        #r = requests.post(url = url, data = data, headers = header).json()

class PassengerVoteApp(App):

    def build(self):

        return PassengerVoteWindow()

if __name__ == '__main__':

    PassengerVoteApp().run()