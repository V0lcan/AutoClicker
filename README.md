# Volcan's Autoclicker

A simple and customizable autoclicker designed for Minecraft fishing farms, but useful for any repetitive clicking task.

<p align="center">
    <img src="https://github.com/V0lcan/autoclicker-gif/blob/main/autoclicker.gif?raw=true" alt="Autoclicker Demo">
</p>

---

## Features

- **Customizable Delay:** Set your click interval in milliseconds.
- **Button Selection:** Choose (M1) for left mouse button or (M2) for right mouse button.
- **Easy Controls:** Start/stop and toggle the autoclicker with keyboard shortcuts.
- **UI:** Clean and simple interface built with PyQt5.

---

## How to Use

1. **Set Delay:** Enter the delay you want (in milliseconds) in the input field.
2. **Select Button:** Choose whether to use the left mouse button (M1) or right mouse button (M2).
3. **Start:** Click the **Start** button to **Start** the autoclicker.
4. **Controls:**
    - Press **O** to toggle the autoclicker on/off.
    - Press **P** to stop the autoclicker entirely.

---

## Requirements

- Python 3.x
- [PyQt5](https://pypi.org/project/PyQt5/)
- [pynput](https://pypi.org/project/pynput/)

Install dependencies:
```sh
pip install PyQt5 pynput
```

---

## Release v1.0

The release includes a pre-built `.exe` for convenience. If you prefer not to run executables from unknown sources, you can clone the repository:

```sh
git clone https://github.com/V0lcan/AutoClicker
```

Run as a Python script:

```sh
python3 Autoclicker.py
```

Or build your own `.exe` using [PyInstaller](https://pyinstaller.org/en/stable/):

```sh
pyinstaller --onefile --noconsole --icon=assets/icon.ico Autoclicker.py
```