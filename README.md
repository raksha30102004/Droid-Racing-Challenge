# 🏆 Droid Racing Challenge 2024 — Champions

> **1st Place** at the Droid Racing Challenge 2024, held in Brisbane, Australia, with competitors from across the country.

## About the Competition

The [Droid Racing Challenge](https://www.qut.edu.au/study/professional-and-executive-education/droid-racing-challenge) is an autonomous robotics competition where teams build and program a droid that uses **computer vision** to navigate a colour-coded track as fast as possible. The droid must detect lane boundaries, avoid obstacles, and follow directional arrows — all in real time, with no remote control.

## How It Works

The droid is powered by a **Raspberry Pi** with a camera module. It captures a live video feed, processes each frame to detect coloured lane markers and obstacles, and drives two DC motors through GPIO to steer itself along the track.

### Track Layout

| Colour | Meaning |
|--------|---------|
| 🟡 Yellow | Left lane boundary |
| 🔵 Blue | Right lane boundary |
| 🟢 Green | Finish / end zone |
| 🟣 Purple/Pink | Obstacle |
| 🟠 Arrow | Directional indicator |

## Architecture

```
main.py              ← Main control loop (capture → process → drive)
├── helper.py        ← Computer vision pipeline (filtering, line detection, perspective warp, error calculation)
├── colours.py       ← HSV colour threshold definitions for each track element
├── motor.py         ← Raspberry Pi GPIO motor driver (PWM speed control)
├── pid.py           ← PID controller for smooth steering
├── colour_picker.py ← Utility: live HSV trackbar for tuning colour thresholds
└── keyboard_control.py ← Utility: manual keyboard control for testing motors
```

## Key Techniques

- **Perspective Warp** — Transforms the camera's angled view into a top-down bird's-eye perspective for more accurate lane detection.
- **HSV Colour Filtering** — Isolates lane boundaries and obstacles by filtering specific hue/saturation/value ranges.
- **Contour-Based Line Detection** — Finds the longest contour in each filtered region and computes its angle relative to the droid.
- **Split-Frame Processing** — The image is split into left and right halves so each lane boundary is detected independently.
- **Proportional Steering Control** — Angular error and distance error are combined with tuned proportional gains to calculate differential motor speeds.
- **Obstacle Avoidance** — Obstacles detected on either side of the frame bias the steering error to steer the droid away.

## Hardware

- Raspberry Pi (with Pi Camera)
- L298N (or similar) dual H-bridge motor driver
- 2× DC motors with wheels
- Chassis and power supply

## Getting Started

### Prerequisites

- Python 3
- OpenCV (`cv2`)
- NumPy
- `RPi.GPIO` (on Raspberry Pi)

### Installation

```bash
pip install opencv-python numpy RPi.GPIO
```

### Calibrating Colours

Use the colour picker utility to find the right HSV thresholds for your lighting conditions:

```bash
python colour_picker.py
```

Adjust the trackbars until only the target colour is visible, then update the values in `colours.py`.

### Running the Droid

```bash
python main.py
```

Press **Enter** to start. The droid will begin navigating autonomously. Press **q** to quit.

### Manual Motor Testing

```bash
python keyboard_control.py
```

Use the arrow keys to drive the droid manually.

## Tuning

The key parameters to adjust in `main.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `speed` | 80 | Base forward speed (0–100) |
| `turnSpeed` | 60 | Speed during turns (0–100) |
| `angle_p` | 0.47 | Proportional gain for angular error |
| `dist_p` | 0.3 | Proportional gain for distance error |
| `d_thresh` | 250 | Distance threshold for lane proximity correction |
| `thresh` | 5 | Minimum angular error to trigger a turn |

## License

This project was built for the Droid Racing Challenge 2024. Feel free to use it as a reference for your own autonomous droid projects.
