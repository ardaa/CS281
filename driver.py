import PySimpleGUI as sg
from signup import sign_up_gui
def driver_gui(db):
    sg.theme('LightGrey1')   # Add a touch of color
    # All the stuff inside your window.
    # get the list of cars that belong to the driver
    username = db.get_username()
    print(username)

    user_data = db.get_driver_info(username)
    print(user_data)
    cars = db.get_cars(username)
    cars = [car[0] for car in cars]
    trip = db.get_trips(username)
    if cars == []:
        layout = [  [sg.Image(r'logo50.png')],
                    [sg.Text('Hey! You have no cars registered yet!')],
                    [sg.Button('Register a car'), sg.Button('Cancel')] ]
    elif user_data[-3] == 0:
        layout = [  [sg.Image(r'logo50.png')],
                    [sg.Text('Hey! You seem to be not available to drive. Please select the car you want to use and start on accepting trips.')],
                    [sg.Text('Select a car')],
                    [sg.Listbox(values=cars, size=(60, 6), key='car')],
                    [sg.Button('Start'), sg.Button('Cancel')] ]
        
    elif trip == []:
        layout = [[sg.Image(r'logo50.png')],
                    [sg.Text('Hey! You have no trips registered yet! Wait for a passenger to request a trip. Your trips will appear here.')]]
    

    # Create the Window
    window = sg.Window('RideLink - Driver', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        if event == 'Register a car':
            register_car_gui(db)
            break
        if event == 'Start':
            driver_gui(db)
            break
    window.close()

def register_car_gui(db):
    print('s')