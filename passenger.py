import PySimpleGUI as sg
from signup import sign_up_gui
def passenger_gui(db):
    sg.theme('LightGrey1')   # Add a touch of color
    # All the stuff inside your window.
    # get the list of cars that belong to the driver
    username = db.get_username()
    drivers = db.get_driver_avail()
    for i in range(len(drivers)):
        drivers[i] = ', '.join(list(map(str, drivers[i])))
    cars = []
    car_type = "All"
    addresses = db.get_addresses()
    trip = db.get_user_trip(username)
    print(trip)
    page = "main"
    screenList = ["Driver","Car","Payment","Start Address", "Destination Address"]
    screen = screenList[0]
    layout = set_layout(page, drivers, cars, addresses, screen)

    # Create the Window
    window = sg.Window('RideLink - Driver', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            if page=="create_trip":
                page ="main"
                window.close()
                layout = set_layout(page, drivers, cars, addresses, screen)
                window = sg.Window('RideLink - Passenger', layout)
            elif page=="previous_trip":
                page ="main"
                window.close()
                layout = set_layout(page, drivers, cars, addresses, screen)
                window = sg.Window('RideLink - Passenger', layout)
            elif page=="main":
                break

        elif event == "Call a Vehicle":
            page = "create_trip"
            screen = screenList[0]
            window.close()
            layout = set_layout(page, drivers, cars, addresses, screen)
            window = sg.Window('RideLink - Passenger', layout)
        elif event == "Previous Trips":
            page = "previous_trip"
            trip = db.get_user_trip(username)
            window.close()
            print(trip)
            layout = set_layout(page, drivers, cars, addresses, screen, trip)
            window = sg.Window('RideLink - Passenger', layout)
        elif event == 'Select Driver':
            try:
                try:   
                    selected_driver = values['selectedDriver'][0].split(', ')[0]  # Get the first selected item
                except:
                    selected_driver = values['selectedDriver'][0][0]
                cars = db.get_cars(selected_driver, car_type)
                for i in range(len(cars)):
                    cars[i] = ', '.join(list(map(str, cars[i])))
                screen = screenList[screenList.index(screen) + 1]
                window.close()
                layout = set_layout(page, drivers, cars, addresses, screen)
                window = sg.Window('RideLink - Passenger', layout)
            except:
                sg.popup("Please select a driver.")

        elif event == 'Cheap' or event=="Normal" or event=="Expensive" or event=="All":
            car_type = event
            drivers = db.get_driver_avail(car_type)
            layout = set_layout(page, drivers, cars, addresses, screen)
            window.close()
            window = sg.Window('RideLink - Passenger', layout)

        elif event == 'Select Car':
            try:    
                selected_car = values['selectedCar'][0].split(', ')[0]   # Get the first selected item
                screen = screenList[screenList.index(screen) + 1]
                window.close()
                layout = set_layout(page, drivers, cars, addresses, screen)
                window = sg.Window('RideLink - Passenger', layout)
            except:
                sg.popup("Please select a car.")

        elif event == 'Select Payment':
            try:        
                selected_payment = values['selectedPayment']  # Get the first selected item 
                screen = screenList[screenList.index(screen) + 1]
                window.close()
                layout = set_layout(page, drivers, cars, addresses, screen)
                window = sg.Window('RideLink - Passenger', layout)
            except:
                sg.popup("Please select a payment method.")
            
        elif event == 'Select Start Address':
            try:        
                selected_start_address = values['selectedStart'][0]  # Get the first selected item
                dest_adresses = addresses.copy()
                dest_adresses.remove(selected_start_address)
                print(dest_adresses)
                screen = screenList[screenList.index(screen) + 1]
                window.close()
                layout = set_layout(page, drivers, cars, dest_adresses, screen)
                window = sg.Window('RideLink - Passenger', layout)
            except:
                sg.popup("Please select a start address.")

        elif event == 'Select Destination Address':      
            try:
                selected_destination_address = values['selectedDestination'][0]  # Get the first selected item
            except:
                sg.popup("Please select a destination address.")
                continue
            page = "main"
            screen = screenList[0]
            db.create_trip(selected_driver, selected_car, selected_payment, selected_start_address, selected_destination_address)
            sg.popup("Your trip has been created.")
            window.close()
            layout = set_layout(page, drivers, cars, addresses.remove(selected_destination_address), screen)
            window = sg.Window('RideLink - Passenger', layout)
           

        elif event == "Back":
            screen = screenList[screenList.index(screen) - 1]
            window.close()
            layout = set_layout(page, drivers, cars, addresses, screen)
            window = sg.Window('RideLink - Passenger', layout)
        
        elif event == "Add Review":
            selected_item = values['selectedTrip'][0] if values['selectedTrip'] else None
            trip_id = selected_item.split(', ')[0]
            trip_rank = sg.popup_get_text("Please enter a rank between 1 and 5.")
            try:
                if trip_rank.isdigit() and int(trip_rank) in range(1,6):
                    trip_rank = int(trip_rank)
                else:
                    sg.popup("Please enter a valid rank.")
            except:
                continue
            trip_comment = sg.popup_get_text("Please enter a comment.")
            if trip_comment:
                db.add_trip_review(trip_id, trip_rank, trip_comment)
                sg.popup("Your review has been added.")
        try:
            if page == "previous_trip":
                selected_item = values['selectedTrip'][0] if values['selectedTrip'] else None
                status = selected_item.split(', ')[-2]
                window['Add Review'].update(disabled=(status!="Delivered"))
        except:
            pass

    window.close()

def set_layout(page, drivers, cars, addresses, screen, trips=None):
    
    if page == "main":
        layout = [  [sg.Image(r'logo50.png')],
                    [sg.Text("Welcome to RideLink. You can Call a Vehicle and show your previous trips.")],
                    [sg.Button('Call a Vehicle'),sg.Button('Previous Trips'),sg.Button('Cancel')] ]
    elif page == "create_trip":
        layout = [  [sg.Image(r'logo50.png')],
                    [sg.Text('Please select the driver you want to travel with.')],
                    [sg.Text('Select a driver')],
                    [sg.Button('All',visible=(screen=="Driver")),sg.Button('Cheap',visible=(screen=="Driver")),sg.Button('Normal',visible=(screen=="Driver")),sg.Button('Expensive',visible=(screen=="Driver"))],
                    [sg.Listbox(values=drivers, size=(60, 6), key='selectedDriver',visible=(screen=="Driver"))],
                    [sg.Listbox(values=["Card","Cash"], size=(60, 6), key='selectedPayment', visible=(screen=="Payment"))],
                    [sg.Listbox(values=cars, size=(60, 6), key='selectedCar', visible=(screen=="Car"))],
                    [sg.Listbox(values=addresses, size=(60, 6), key='selectedStart', visible=(screen=="Start Address"))],
                    [sg.Listbox(values=addresses, size=(60, 6), key='selectedDestination', visible=(screen=="Destination Address"))],
                    [sg.Button("Select {}".format(screen)), sg.Button('Cancel', visible=(screen=="Driver")), sg.Button('Back', visible=(screen!="Driver"))] ]
    elif page == "previous_trip":
        layout = [  [sg.Image(r'logo50.png')],
                    [sg.Text('Here are your previous trips.')],
                    [sg.Listbox(values=trips, size=(60, 6), key='selectedTrip', enable_events=True)],
                    [sg.Button('Cancel'), sg.Button('Add Review', disabled_button_color="grey", disabled = True)] ]

        
                    
    return layout

def register_car_gui(db):
    print('s')