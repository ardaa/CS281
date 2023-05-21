import PySimpleGUI as sg
from signup import sign_up_gui
def passenger_gui(db):
    sg.theme('LightGrey1')   # Add a touch of color
    # All the stuff inside your window.
    # get the list of cars that belong to the driver
    username = db.get_username()
    print(username)

    drivers = db.get_driver_avail()
    print(drivers)
    cars = []
    addresses = db.get_addresses()
    print(addresses)
    trip = db.get_trips(username)
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
            else:
                break

        elif event == "Create New Trip":
            page = "create_trip"
            window.close()
            layout = set_layout(page, drivers, cars, addresses, screen)
            window = sg.Window('RideLink - Passenger', layout)

        elif event == 'Select Driver':
            try:
                selected_driver = values['selectedDriver'][0][0]  # Get the first selected item
                cars = db.get_cars(selected_driver)
                screen = screenList[screenList.index(screen) + 1]
                window.close()
                layout = set_layout(page, drivers, cars, addresses, screen)
                window = sg.Window('RideLink - Passenger', layout)
            except:
                pass

        elif event == 'Select Car':
            try:    
                selected_car = values['selectedCar'][0]  # Get the first selected item
                screen = screenList[screenList.index(screen) + 1]
                window.close()
                layout = set_layout(page, drivers, cars, addresses, screen)
                window = sg.Window('RideLink - Passenger', layout)
            except:
                pass

        elif event == 'Select Payment':
            try:        
                selected_payment = values['selectedPayment']  # Get the first selected item 
                screen = screenList[screenList.index(screen) + 1]
                window.close()
                layout = set_layout(page, drivers, cars, addresses, screen)
                window = sg.Window('RideLink - Passenger', layout)
            except:
                pass
            
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
                pass

        elif event == 'Select Destination Address':
            try:        
                selected_destination_address = values['selectedDestination'][0]  # Get the first selected item
                page = "main"
                db.create_trip(selected_driver, selected_car, selected_payment, selected_start_address, selected_destination_address)
                window.close()
                layout = set_layout(page, drivers, cars, addresses.remove(selected_destination_address), screen)
                window = sg.Window('RideLink - Passenger', layout)
            except: 
                pass

        elif event == "Back":
            screen = screenList[screenList.index(screen) - 1]
            window.close()
            layout = set_layout(page, drivers, cars, addresses, screen)
            window = sg.Window('RideLink - Passenger', layout)
    window.close()

def set_layout(page, drivers, cars, addresses, screen):
    
    if page == "main":
        layout = [  [sg.Image(r'logo50.png')],
                    [sg.Text("Welcome to RideLink. You can create new trip and show your previous trips.")],
                    [sg.Button('Create New Trip'),sg.Button('Previous Trips'),sg.Button('Cancel')] ]
    elif page == "create_trip":
        layout = [  [sg.Image(r'logo50.png')],
                    [sg.Text('Please select the driver you want to travel with.')],
                    [sg.Text('Select a driver')],
                    [sg.Listbox(values=drivers, size=(60, 6), key='selectedDriver',visible=(screen=="Driver"))],
                    [sg.Listbox(values=["Card","Cash"], size=(60, 6), key='selectedPayment', visible=(screen=="Payment"))],
                    [sg.Listbox(values=cars, size=(60, 6), key='selectedCar', visible=(screen=="Car"))],
                    [sg.Listbox(values=addresses, size=(60, 6), key='selectedStart', visible=(screen=="Start Address"))],
                    [sg.Listbox(values=addresses, size=(60, 6), key='selectedDestination', visible=(screen=="Destination Address"))],
                    [sg.Button("Select {}".format(screen)), sg.Button('Cancel', visible=(screen=="Driver")), sg.Button('Back', visible=(screen!="Driver"))] ]
    return layout

def register_car_gui(db):
    print('s')