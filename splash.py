import PySimpleGUI as sg

def splash_screen():
    sg.theme('LightGrey1')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Image(r'logo50.png')],
              [sg.Text('Welcome to RideLink!')]]
    # Create the Window
    window = sg.Window('RideLink', layout, element_justification='c', finalize=True)
    # Event Loop to process "events" and get the "values" of the inputs
    event, values = window.read(timeout=1000)
    window.close()
