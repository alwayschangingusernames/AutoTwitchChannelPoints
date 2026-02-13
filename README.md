# AutoTwitchChannelPoints

A Python CLI tool that checks specific screen pixels and clicks matching Twitch UI buttons automatically.

## Requirements

- Python 3.9 or newer
- `pip`
- A desktop session (the script uses screen capture and mouse automation)

## Clone the Repository

```bash
git clone https://github.com/alwayschangingusernames/AutoTwitchChannelPoints.git
cd AutoTwitchChannelPoints
```

## Run on Windows (PowerShell)

```powershell
python .\program.py
```

On first run, the script installs dependencies from `requirements.txt`.

## Run on Linux (bash)

```bash
python3 program.py
```

## Using the Script

When started, the script opens a CLI menu:

1. `Check Pixels` (runs continuous checks every 60 seconds)
2. `Calibrate` (reads the color at an `x, y` coordinate)
3. `Debug Check` (tests whether a coordinate matches the target color)
4. `Exit`

Press `Ctrl+C` to stop continuous checking.

## Notes

- `program.py` installs requirements automatically at startup if `requirements.txt` exists.
- You may need to adjust monitor coordinates in `program.py` for your display layout and resolution.
