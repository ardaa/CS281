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
    trip = db.get_driver_trip(username)
    print(trip)
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
    else:
        layout = [[sg.Image(r'logo50.png')],
                    [sg.Text('Hey! Here is your trip information.')],
                    [sg.Listbox(values=trip, size=(60, 6), key='trip')],
                    [sg.Button('Select Trip'), sg.Button('Exit')]]
        
    

    # Create the Window
    window = sg.Window('RideLink - Driver', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == 'Register a car':
            register_car_gui(db)
            break
        if event == 'Start':
            driver_gui(db)
            break
        if event == 'Select Trip':
            try:
                if values['trip'] == []:
                    sg.popup('Please select a trip!')
                    continue

                #['21, 1, 34 ALP 64, 2023-05-21 21:13:11, Waiting for approval', '7, 2, 35 FT 454, 2023-04-27 07:06:39, Passenger in the car']
                selected_trip = values['trip'][0].split(', ') # Get the first selected item
                layout = [[sg.Image(r'logo50.png')],
                        [sg.Text('Hey! Here is your trip information.')],
                        [sg.Text('Trip ID: ' + selected_trip[0])],
                        [sg.Text('Car Plate: ' + selected_trip[2])],
                        [sg.Text('Start Time: ' + selected_trip[3])],
                        [sg.Combo(['Waiting for approval', 'Passenger in the car', 'Delivered', 'Cancelled', 'On the way'], default_value=selected_trip[4], key='status')],


                        [sg.Button('Change Status'), sg.Button('Cancel')]]
                window.close()
                window = sg.Window('RideLink - Driver', layout)
            except:
                sg.popup('Please select a trip!')
                continue

        if event == 'Change Status':
            if values['status'] == selected_trip[4]:
                sg.popup('Status not changed!')
                continue
            db.update_trip_status(selected_trip[0], values['status'])
            sg.popup('Status changed!')
            

            driver_gui(db)
            break
        if event == 'Cancel':
            window.close()
            driver_gui(db)
            

    window.close()

def register_car_gui(db):
    print('s')