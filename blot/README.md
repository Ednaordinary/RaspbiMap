# Blot files

These are files for the blot

## reblot

Customized firmware that adds
- Speed (SetSpeed)
- Acceleration (SetAccel)
- Max speed (SetMaxSpeed)
- Motor offset (GoFor)

The following values work well:
speed: 120 (lower is faster)
accel: 0.99999 (lower is faster)
max speed: 50 (30 seems to be a minimum)

Interfacing with this firmware uses a modification of blot-cli, available in the pi directory
