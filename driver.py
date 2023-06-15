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
    state_list = ['Waiting for approval',  'On the way', 'Passenger in the car', 'Delivered', 'Cancelled']
    if cars == []:
        layout = [  [sg.Image(r'logo50.png')],
                    [sg.Text('Hey! You have no cars registered yet!')],
                    [sg.Button('Register a car'), sg.Button('Cancel')] ]
    elif len(cars)>0:
        layout = [[sg.Image(r'logo50.png')],
                [sg.Text('Hey! Here is your trip information.',visible=len(trip)>0), sg.Checkbox("Availability", user_data[-3], checkbox_color="blue", key="availability", visible=len(cars)>0)],
                [sg.Text('Hey! You have no trips registered yet! Wait for a passenger to request a trip. Your trips will appear here.', visible=len(trip)==0)],
                [sg.Listbox(values=trip, size=(60, 6), key='trip', visible=len(trip)>0)],
                [sg.Button('Select Trip',visible=len(trip)>0), sg.Button('Set Availability', visible = len(cars)>0), sg.Button('Exit')]]
        
    

    # Create the Window
    window = sg.Window('RideLink - Driver', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == 'Register a car':
            register_car_gui(db)
            break
        elif event == 'Start':
            driver_gui(db)
            break
        elif event == 'Select Trip':
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
                    [sg.Combo(state_list[state_list.index(selected_trip[4]):int(state_list.index(selected_trip[4]))+1 if state_list.index(selected_trip[4])>2   else int(len(state_list))], default_value=selected_trip[4], key='status')],
                    [sg.Button('Change Status'), sg.Button('Cancel')]]
            window.close()
            window = sg.Window('RideLink - Driver', layout)


        elif event == 'Change Status':
            if values['status'] == selected_trip[4]:
                sg.popup('Status not changed!')
                continue
            db.update_trip_status(selected_trip[0], values['status'])
            sg.popup('Status changed!')
            driver_gui(db)
            break
        elif event == 'Set Availability':
            if values['availability'] == user_data[-3]:
                sg.popup('Availability not changed!')
                continue
            db.update_driver_availability(username, values['availability'])
            sg.popup('Availability changed!')
            driver_gui(db)
            break
        elif event == 'Cancel':
            driver_gui(db)
            break
        elif event == 'Exit':
            break            
            

    window.close()

def register_car_gui(db):
    print('s')