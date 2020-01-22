from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import first_page
import driver_first_page
import driver_vote
import driver_login
import driver_dashboard
import driver_register
import driver_add_car
import driver_edit
import driver_travel_view
import passenger_first_page
import passenger_login
import passenger_register
import passenger_dashboard
import passenger_charge
import passenger_edit
import add_travel_passenger
import passenger_common
import passenger_travel_info
import passenger_vote
import driver_travel_info

#Builder.load_file('base.kv')

class BaseWindow(BoxLayout):

    first = first_page.MainWindow()
    driver_first = driver_first_page.DriverFirstPage()
    driver_log = driver_login.DriverLoginWindow()
    driver_reg = driver_register.DriverRegisterWindow()
    passenger_first = passenger_first_page.PassengerFirstPage()
    passenger_log = passenger_login.PassengerLoginWindow()
    passenger_reg = passenger_register.PassengerRegisterWindow()
    driver_panel = driver_dashboard.DriverPanelWindow()
    passenger_panel = passenger_dashboard.PassengerPanelWindow()
    driver_car = driver_add_car.DriverCarWindow()
    passenger_edit_page = passenger_edit.PassengerEditWindow()
    passenger_charge_page = passenger_charge.PassengerChargeWindow()
    passenger_travel = add_travel_passenger.AddTravelWindow()
    passenger_com = passenger_common.PassengerCommonWindow()
    passenger_travel_info = passenger_travel_info.TravelInfoWindow()
    driver_info_edit = driver_edit.DriverEditWindow()
    driver_info_travel = driver_travel_info.DriverTravelInfoWindow()
    travel_view = driver_travel_view.TravelViewWindow()
    vote_pass = passenger_vote.PassengerVoteWindow()
    vote_driver = driver_vote.DriverVoteWindow()

    def __init__(self , **kwargs):
    
        super().__init__(**kwargs)
        
        self.ids.scrn_first_page.add_widget(self.first)
        self.ids.scrn_passenger_charge.add_widget(self.passenger_charge_page)
        self.ids.scrn_passenger_travel.add_widget(self.passenger_travel)
        self.ids.scrn_passenger_edit.add_widget(self.passenger_edit_page)
        self.ids.scrn_passenger_first.add_widget(self.passenger_first)
        self.ids.scrn_passenger_register.add_widget(self.passenger_reg)
        self.ids.scrn_passenger_login.add_widget(self.passenger_log)
        self.ids.scrn_driver_first.add_widget(self.driver_first)
        self.ids.scrn_driver_register.add_widget(self.driver_reg)
        self.ids.scrn_driver_login.add_widget(self.driver_log)
        self.ids.scrn_driver_panel.add_widget(self.driver_panel)
        self.ids.scrn_passenger_panel.add_widget(self.passenger_panel)
        self.ids.scrn_passenger_common.add_widget(self.passenger_com)
        self.ids.scrn_passenger_travelinfo.add_widget(self.passenger_travel_info)
        self.ids.scrn_driver_car.add_widget(self.driver_car)
        self.ids.scrn_driver_edit.add_widget(self.driver_info_edit)
        self.ids.scrn_travel_view.add_widget(self.travel_view)
        self.ids.scrn_passenger_vote.add_widget(self.vote_pass)
        self.ids.scrn_driver_vote.add_widget(self.vote_driver)
        self.ids.scrn_driver_travelinfo.add_widget(self.driver_info_travel)

class BaseApp(App):

    def build(self):

        return BaseWindow()

if __name__ == "__main__":
    BaseApp().run()