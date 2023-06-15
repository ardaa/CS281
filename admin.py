import PySimpleGUI as sg
from signup import sign_up_gui
def admin_gui(db):
    sg.theme('LightGrey1')   # Add a touch of color
    # All the stuff inside your window.
    # get the list of cars that belong to the driver
    username = db.get_username()
    addresses = db.get_addresses()
    page = "main"
    layout = set_layout(page, addresses)

    # Create the Window
    window = sg.Window('RideLink - Driver', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            if page=="adress":
                page ="main"
                window.close()
                layout = set_layout(page, addresses)
                window = sg.Window('RideLink - Admin', layout)
            elif page=="previous_trip":
                page ="main"
                window.close()
                layout = set_layout(page, addresses)
                window = sg.Window('RideLink - Admin', layout)
            elif page=="main":
                break

        elif event == "Adresses":
            page = "adress"
            window.close()
            layout = set_layout(page, addresses)
            window = sg.Window('RideLink - Admin', layout)

        elif event == "Previous Trips":
            page = "previous_trip"
            trip = db.get_all_trips_and_ranks()
            window.close()
            layout = set_layout(page, addresses, trip)
            window = sg.Window('RideLink - Admin', layout)

        elif event == 'Add adress':
            new_adress = values['adress']
            try:
                x_cor, y_cor, name = new_adress.split(',')
                x_cor, y_cor = format(float(x_cor), '.4f'), format(float(y_cor), '.4f')
                print(x_cor, y_cor, name)
            except:
                sg.popup("Please enter the adress as comma seperated list of X coordinate, Y coordinate, Adress name. Example: 38.87, -78.32, Home")
                continue
            db.add_adress(x_cor, y_cor, name)
            page = "main"
            sg.popup("New adress has been added.")
            layout = set_layout(page, addresses)
            window = sg.Window('RideLink - Admin', layout)

        elif event == 'Delete Review':
            selected_item = values['selectedTrip'][0] if values['selectedTrip'] else None
            review_id = selected_item.split(', ')[-3]
            db.delete_trip_review(review_id)
            sg.popup("Trip has been deleted.")
            trip = db.get_all_trips_and_ranks()
            window["selectedTrip"].update(values=trip)

        try:
            if page == "previous_trip":
                selected_item = values['selectedTrip'][0] if values['selectedTrip'] else None
                status = selected_item.split(', ')[-1]
                print(status)
                window['Delete Review'].update(disabled=(status == "None"))
        except:
            pass


    window.close()

def set_layout(page, addresses, trips=None):
    
    if page == "main":
        layout = [  [sg.Image(r'logo50.png')],
                    [sg.Text("Welcome to RideLink. You can edit adresses and trip comments")],
                    [sg.Button('Adresses'),sg.Button('Previous Trips'),sg.Button('Cancel')] ]
    elif page == "adress":
        layout = [  [sg.Image(r'logo50.png')],
                    [sg.Text('You can add a new adress')],
                    [sg.Text('Please write the adress as comma seperated list of X coordinate, Y coordinate, Adress name')],
                    [sg.Text('Adress', size=(15, 1)), sg.InputText(key='adress')],
                    [sg.Button("Add adress"), sg.Button('Cancel')] ]
    elif page == "previous_trip":
        layout = [  [sg.Image(r'logo50.png')],
                    [sg.Text('Here are your previous trips.')],
                    [sg.Listbox(values=trips, size=(60, 6), key='selectedTrip', enable_events=True)],
                    [sg.Button('Delete Review', disabled_button_color="grey", disabled = True), sg.Button('Cancel')] ]

        
                    
    return layout

def register_car_gui(db):
    print('s')