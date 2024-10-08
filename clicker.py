import time, threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

def clicker(delay_input, button_toggle):

    # If m1 is selected, set the button to left, else set it to right
    if button_toggle:
        m1 = Button.left
    else:
        m1 = Button.right

    mouse = Controller()

    # Keycodes for the toggle and exit keys
    autoclick_toggle = KeyCode(char='o')
    autoclick_exit = KeyCode(char='p')

    # Convert the delay to seconds
    delay = delay_input / 1000

    class autoclicker(threading.Thread):
        def __init__(self, delay, button):
            super().__init__()
            self.delay = delay
            self.button = button
            self.running = False
            self.program_running = True

        # Functions used to toggle the clicking
        def start_clicking(self):
            self.running = True

        def stop_clicking(self):
            self.running = False

        # Function to exit the program
        def exit(self):
            self.stop_clicking()
            self.program_running = False

        def run(self):
            while self.program_running:
                while self.running:
                    mouse.click(self.button)
                    time.sleep(self.delay)
                time.sleep(0.1)

    click_thread = autoclicker(delay, m1)
    click_thread.start()

    def on_press(key):
        if key == autoclick_toggle:
            if click_thread.running:
                click_thread.stop_clicking()
            else:
                click_thread.start_clicking()
        elif key == autoclick_exit:
            click_thread.exit()
            listener.stop()

    with Listener(on_press=on_press) as listener:
        listener.join()