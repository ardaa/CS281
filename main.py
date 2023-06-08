import login
import signup
import splash
from driver import driver_gui
from passenger import passenger_gui
from admin import admin_gui

import PySimpleGUI as sg
from database import Database

def main_gui():
    #initialize database 
    db = Database(db='project.sqlite')
    sg.theme('LightGrey1')   # Add a touch of color
    splash.splash_screen()
    acc_type = login.login_gui(db)
    while acc_type != None:
        if acc_type == 'D':
            driver_gui(db)
        elif acc_type == 'P':
            passenger_gui(db)
        elif acc_type == 'A':
            admin_gui(db)
        acc_type = login.login_gui(db)

if __name__ == '__main__':
    main_gui()


