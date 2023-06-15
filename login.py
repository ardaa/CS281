import PySimpleGUI as sg
from signup import sign_up_gui
import re
def login_gui(db):
    sg.theme('LightGrey1')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Image(r'logo50.png'),sg.Text('Welcome to RideLink!')],
                [sg.Text('Please enter your Email and password')],
                [sg.Text('Email', size=(15, 1)), sg.InputText(key='email')],
                [sg.Text('Password', size=(15, 1)), sg.InputText(password_char='*', key='pass')],
                [sg.Text('')],

                [sg.Button('Login'), sg.Button('Sign Up'), sg.Button('Cancel')] ]

    # Create the Window
    window = sg.Window('RideLink - Login', layout)
    
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        window['email'].bind("<Return>", "_Enter")
        window['pass'].bind("<Return>", "_Enter")

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            return None

        if event == 'Login' or event == '_Enter' or event == 'pass_Enter':
            if values['email'] == '' or values['pass'] == '':
                sg.popup('Please fill all the fields')
                continue
            if not re.match(r"[^@]+@[^@]+\.[^@]+", values['email']):
                sg.popup('Please enter a valid email address')
                continue
            acc_type = db.login(values['email'], values['pass'])
            if acc_type:
                sg.popup('Login successful')
                window.close()
                return acc_type
            else:
                sg.popup('Login failed')
        if event == 'TestLogin':
            acc_type = db.login('admin','123456')
            if acc_type:
                sg.popup('Login successful')
                window.close()
                return acc_type
        if event == 'TestDriver':
            acc_type = db.login('booker55@gmail.com','123456')
            if acc_type:
                sg.popup('Login successful')
                window.close()
                return acc_type
            
        if event == 'Sign Up':
            sign_up_gui(db)
        
            
    window.close()

if __name__ == '__main__':
    login_gui()
