import PySimpleGUI as sg

def sign_up_gui(db):
    sg.theme('LightGrey1')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Image(r'logo50.png'),sg.Text('Welcome to RideLink!')],
                [sg.Text('Please enter your information')],
                [sg.Text('Name', size=(15, 1)), sg.InputText()],
                [sg.Text('Surname', size=(15, 1)), sg.InputText()],
                [sg.Text('Email', size=(15, 1)), sg.InputText()],
                [sg.Text('Password', size=(15, 1)), sg.InputText(password_char='*')],
                [sg.Text('User Type', size=(15, 1))],
                [sg.Radio('Driver', "RADIO1", default=False, size=(15,1)), sg.Radio('Passenger', "RADIO1", default=False, size=(15,1))],
                [sg.Button('Sign Up'), sg.Button('Cancel')] ]

    # Create the Window
    window = sg.Window('Sign Up', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        if event == 'Sign Up':
            print(values)
            #valifation
            if values[1] == '' or values[2] == '' or values[3] == '' or values[4] == '' or (values[5] == False and values[6] == False):
                sg.popup('Please fill all the fields')
                continue
            if values[5] == True:
                values[5] = 'D'
            elif values[6] == True:
                values[5] = 'P'
            if db.signup(values[4], values[3], values[1], values[2], values[5]):
                break
            else:
                sg.popup('Sign Up failed')
                break
    window.close()
