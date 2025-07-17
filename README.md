# sage

sage is a clean and easy-to-use CLI timer and stopwatch that works the way you think it should.

## Installation

```bash
pip install sage
```

## Quick Start

```bash
sage timer 25m                  # Start a 25-minute timer
sage timer pomodoro             # Use the built-in pomodoro timer
sage stopwatch                  # Start a stopwatch
sage timers list                # See all your custom timers
```

## Features

- **Intuitive timer input** - Use human-readable time strings or flags
- **Custom timer management** - Create, update, and organize your own timers
- **Visual interface** - Clean curses-based display with pause/resume
- **Flexible usage** - Works however you intuitively expect it to
- **Sound notifications** - Audio alert when timers complete
- **Stopwatch with counter** - Track laps or intervals during timing sessions

## Usage

### Timer

The sage timer is built to be intuitive, working how you expect it to work. Since we all think differently about time, timers can be set in multiple ways.

#### Time unit flags

Use option flags to set the timer. Flags can be applied in any order and combined however makes sense to you.

```bash
sage timer -m 15                            # 15 minute timer
sage timer --hours 1 --minutes 30           # 1 hour 30 minute timer
sage timer -s 45                            # 45 second timer
sage timer --seconds 30 -m 2                # 2 minute 30 second timer
```

#### Human-readable time strings

We're not all robots, so `sage timer` also accepts human-readable time strings. You can even mix and match unit formats within the same string.

```bash
sage timer 25m                              # 25 minute timer
sage timer "10 minutes 30 sec"              # 10 minute 30 second timer
sage timer 3min25s                          # 3 minute 25 second timer
sage timer "1 hour 15m"                     # 1 hour 15 minute timer
sage timer 2h30m45s                         # 2 hours 30 minutes 45 seconds
```

#### Timer controls

Once your timer is running, you can control it with simple keystrokes:

- **Space** - Pause and resume the timer
- **Enter** - Increment the counter (useful for tracking cycles or intervals)
- **Q** - Quit the timer

#### Custom timers

Save your frequently used timers with custom names. This is perfect for work routines, exercise intervals, cooking times, or any recurring timing needs.

```bash
sage timer pomodoro                         # Use the built-in 25-minute pomodoro timer
sage timer potato                           # Use the built-in 50-minute potato timer
sage timer workout                          # Use your custom workout timer
```

### Managing Custom Timers

Custom timers are managed through the `sage timers` command family. This lets you create a personal library of timers for different activities.

```bash
sage timers                                 # List all timers (same as 'list')
sage timers list                            # List all custom timers
sage timers create <name> <duration>        # Create a new timer
sage timers update <name> <duration>        # Update an existing timer
sage timers rename <name> <new_name>        # Rename a timer
sage timers delete <name>                   # Delete a timer
```

#### Examples

```bash
# Create timers for different activities
sage timers create workout 45m
sage timers create meditation "10 minutes"
sage timers create presentation --hours 1 --minutes 15

# Update a timer duration
sage timers update workout 50m
sage timers update meditation -m 15

# Organize your timers
sage timers rename workout morning-workout
sage timers rename meditation daily-meditation

# Clean up timers you no longer need
sage timers delete old-timer-name
```

Custom timers accept the same flexible time formats as the main timer command - use whatever feels natural to you.

#### Built-in timers

sage comes with a few useful timers built in:

- **pomodoro** - 25 minutes (classic productivity timer)
- **potato** - 50 minutes (perfect for baked potatoes)
- **johncage** - 4 minutes 33 seconds (the length of John Cage's famous composition)
- **pika** - 5 seconds (for quick tests)
- **rest** - 10 minutes (short break timer)

### Stopwatch

sage also provides a stopwatch for timing activities where you don't know the duration in advance.

```bash
sage stopwatch                      # Start a stopwatch
```

#### Stopwatch controls

- **Space** - Start, pause, and resume the stopwatch
- **Enter** - Increment the counter (track laps, intervals, or repetitions)
- **Q** - Quit the stopwatch

The stopwatch displays elapsed time and includes a counter in the bottom right corner. This is perfect for tracking laps during runs, intervals during workouts, or cycles during any repetitive activity.

### Advanced Options

#### No-start mode

Both timers and stopwatch can be loaded in a paused state:

```bash
sage timer 25m --no-start           # Load timer but don't start immediately
sage stopwatch --no-start           # Load stopwatch but don't start immediately
```

This is useful when you want to set up your timer, then start it at the precise moment you're ready.

## Configuration

sage stores your custom timers in your system's standard configuration directory:

- **Linux/macOS**: `~/.config/sage/timers.json`
- **Windows**: `%APPDATA%\sage\timers.json`

The configuration file is created automatically when you save your first custom timer. You can back up this file to preserve your custom timers across different machines.

## Error Handling

sage provides helpful error messages to guide you toward correct usage:

- Invalid time formats suggest correct alternatives
- Missing timer names show available options
- Duration requirements are clearly explained
- Sound file warnings alert you if audio notifications might not work

## Requirements

- Python 3.8+
- Cross-platform support (Linux, macOS, Windows)
- Terminal with curses support

## Dependencies

sage uses a minimal set of well-maintained dependencies:

- **click** - Command-line interface framework
- **nava** - Cross-platform audio playback
- **platformdirs** - System-appropriate config directory handling

## Tips

- **Mix input styles**: Use flags for precise control, strings for quick timers
- **Organize with names**: Create descriptive timer names for different activities
- **Use the counter**: Track intervals, laps, or cycles during any timing session
- **Try the built-ins**: The included timers cover common use cases
- **Pause when needed**: Both timers and stopwatch can be paused and resumed

## Philosophy

sage is designed around the principle that tools should work the way you naturally think about them. Time is personal and contextual - sometimes you think "25 minutes," sometimes "25m," and sometimes "--minutes 25." sage accepts all of these because the tool should adapt to you, not the other way around.

The interface is intentionally minimal and distraction-free. When you're timing something, you want to focus on that activity, not on managing the timer. sage gets out of your way while providing exactly the functionality you need.

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Changelog

See CHANGELOG.md for version history and updates.
