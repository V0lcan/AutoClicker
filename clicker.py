import random, threading, time
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, KeyCode, Listener

# Hotkeys offered in the UI. Function keys are the default because a letter
# key fires even while typing in another window.
HOTKEYS = {
    "F6": Key.f6,
    "F7": Key.f7,
    "F8": Key.f8,
    "F9": Key.f9,
    "F10": Key.f10,
    "O": KeyCode(char='o'),
    "P": KeyCode(char='p'),
}


class Clicker(threading.Thread):

    # Constructor
    def __init__(self, on_stopped=None):
        super().__init__(daemon=True)
        self.delay = 1.0
        self.button = Button.left
        self.jitter = 0.0
        self.limit = 0
        self.clicks = 0
        self.on_stopped = on_stopped
        self.mouse = Controller()
        self._clicking = threading.Event()
        self._shutdown = threading.Event()

    @property
    def running(self):
        return self._clicking.is_set() and not self._shutdown.is_set()

    # Functions used to toggle the clicking
    def start_clicking(self):
        self.clicks = 0
        self._clicking.set()

    def stop_clicking(self):
        self._clicking.clear()

    def toggle(self):
        if self.running:
            self.stop_clicking()
        else:
            self.start_clicking()

    # Function to exit the program
    def shutdown(self):
        self._shutdown.set()
        # Wakes run() out of its idle wait so the thread can exit
        self._clicking.set()

    # Random interval within +/- jitter of the delay
    def interval(self):
        if not self.jitter:
            return self.delay
        return max(0.001, random.uniform(self.delay - self.jitter, self.delay + self.jitter))

    def run(self):
        while not self._shutdown.is_set():
            self._clicking.wait()
            if self._shutdown.is_set():
                break

            next_click = time.perf_counter()
            while self._clicking.is_set() and not self._shutdown.is_set():
                self.mouse.click(self.button)
                self.clicks += 1

                if self.limit and self.clicks >= self.limit:
                    self.stop_clicking()
                    if self.on_stopped:
                        self.on_stopped()
                    break

                # Advancing an absolute deadline keeps the interval from
                # drifting by however long each click takes
                next_click += self.interval()
                self._shutdown.wait(max(0.0, next_click - time.perf_counter()))


class HotkeyListener:

    # Constructor. Bindings map a pynput key to a callback, which is invoked
    # on the listener's own thread.
    def __init__(self, bindings):
        self.bindings = bindings
        self.listener = None

    def start(self):
        self.listener = Listener(on_press=self.on_press)
        self.listener.daemon = True
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

    def on_press(self, key):
        # Shift turns 'o' into 'O', which would otherwise miss the binding
        if isinstance(key, KeyCode) and key.char:
            key = KeyCode(char=key.char.lower())

        for bound, callback in self.bindings.items():
            if key == bound:
                callback()
                return
