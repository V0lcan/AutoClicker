# Volcan's Autoclicker

A simple and customizable autoclicker designed for Minecraft fishing farms, but useful for any repetitive clicking task.

<p align="center">
    <img src="https://github.com/V0lcan/autoclicker-gif/blob/main/autoclicker.gif?raw=true" alt="Autoclicker Demo">
</p>

---

## Features

- **Customizable Delay:** Set your click interval in milliseconds.
- **Jitter:** Randomize each interval by up to ± a chosen amount for less uniform clicking.
- **Click Limit:** Stop automatically after a set number of clicks, or run until stopped.
- **Button Selection:** Choose (M1) for left mouse button or (M2) for right mouse button.
- **Configurable Hotkeys:** Pick your own toggle and stop keys (F6 and F7 by default).
- **UI:** Clean and simple interface built with PyQt5, with a live status readout.

---

## How to Use

1. **Set Delay:** Enter the delay you want (in milliseconds) in the input field.
2. **Set Jitter (optional):** Enter a value to randomize each interval by up to ± that many milliseconds. Leave at 0 for a fixed delay.
3. **Set a Click Limit (optional):** Stop after this many clicks. Leave at 0 to run until you stop it.
4. **Select Button:** Choose whether to use the left mouse button (M1) or right mouse button (M2).
5. **Choose Hotkeys:** Pick a toggle key and a stop key. They must be different.
6. **Start:** Click **Start** to arm the hotkeys, then use them to control the clicker:
    - Press the **toggle key** (**F6** by default) to start and pause clicking.
    - Press the **stop key** (**F7** by default) to stop and release the hotkeys.

Click **Stop** in the window, or just close it, to shut everything down.

---

## Requirements

- Python 3.x
- [PyQt5](https://pypi.org/project/PyQt5/)
- [pynput](https://pypi.org/project/pynput/)

Install dependencies:
```sh
pip install -r requirements.txt
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
pyinstaller --onefile --noconsole --icon=assets/icon.ico --add-data "assets;assets" Autoclicker.py
```

On Linux or macOS, use a colon instead of a semicolon: `--add-data "assets:assets"`.