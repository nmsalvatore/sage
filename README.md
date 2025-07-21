# sage

A clean and intuitive CLI timer and stopwatch that works the way you think about time.

## Installation

```bash
pip install sage
```

## Quick Start

```bash
sage timer 25m                  # Start a 25-minute timer
sage timer pomodoro             # Use the built-in pomodoro timer
sage stopwatch                  # Start a stopwatch
sage list                       # See all your custom timers
```

## Features

- **Intuitive time input** - Use natural language like "25m", "1 hour 30 minutes", or "45s"
- **Custom timer management** - Create, update, and organize your own named timers
- **Clean interface** - Distraction-free curses display with pause/resume functionality
- **Sound notifications** - Audio alerts when timers complete
- **Stopwatch with lap counter** - Track intervals and repetitions
- **Cross-platform** - Works on Linux, macOS, and Windows

## Usage

### Timer

sage timer accepts flexible, human-readable time formats that work however you naturally think about time:

```bash
sage timer 25m                              # 25 minutes
sage timer "10 minutes 30 seconds"          # 10 minutes 30 seconds
sage timer 3min25s                          # 3 minutes 25 seconds
sage timer "1 hour 15m"                     # 1 hour 15 minutes
sage timer 2h30m45s                         # 2 hours 30 minutes 45 seconds
```

#### Timer Controls

Once running, control your timer with simple keystrokes:

- **Space** - Pause and resume
- **Enter** - Increment counter
- **Q** - Quit

#### Custom Timers

Save frequently used timers with memorable names:

```bash
sage timer pomodoro                         # Built-in 25-minute timer
sage timer workout                          # Your custom workout timer
sage timer meditation                       # Your custom meditation timer
```

### Managing Custom Timers

Create and organize your personal library of timers:

```bash
sage list                                   # List all available timers
sage create <name> <duration>               # Create a new timer
sage update <name> <duration>               # Update existing timer
sage rename <name> <new_name>               # Rename a timer
sage delete <name>                          # Delete a timer
```

#### Examples

```bash
# Create timers for different activities
sage create workout 45m
sage create meditation "10 minutes"
sage create presentation "1 hour 15 minutes"

# Update and organize
sage update workout 50m
sage rename workout morning-routine
sage delete old-timer
```

All timer commands accept the same flexible time formats as the main timer.

### Stopwatch

For timing activities with unknown duration:

```bash
sage stopwatch                      # Start a stopwatch
sage stopwatch --paused             # Start paused (begin when ready)
```

#### Stopwatch Controls

- **Space** - Pause and resume
- **Enter** - Increment counter
- **Q** - Quit

The stopwatch displays elapsed time with centisecond precision and includes a lap counter for tracking intervals or repetitions.

### Advanced Options

#### Starting Paused

Both timers and stopwatch can start in a paused state:

```bash
sage timer 25m --paused             # Load timer but don't start immediately
sage stopwatch --paused             # Load stopwatch but don't start immediately
```

Perfect for setting up your timer, then starting it at the precise moment you're ready.

## Configuration

Custom timers are automatically saved to your system's standard configuration directory:

- **Linux/macOS**: `~/.config/sage/presets.json`
- **Windows**: `%APPDATA%\sage\presets.json`

The configuration file is created automatically when you save your first custom timer.

## Time Format Examples

sage understands time the way you naturally express it:

| Input | Meaning |
|-------|---------|
| `25m` | 25 minutes |
| `1h30m` | 1 hour 30 minutes |
| `45s` | 45 seconds |
| `"2 hours"` | 2 hours |
| `"10 min 30 sec"` | 10 minutes 30 seconds |
| `1h15m30s` | 1 hour 15 minutes 30 seconds |

## Error Handling

sage provides clear, helpful error messages:

- Invalid time formats suggest correct alternatives
- Missing arguments show proper usage
- Duration limits are clearly explained (1 second to 24 hours)
- Sound file warnings alert if audio notifications unavailable

## Requirements

- Python 3.10+
- Terminal with curses support
- Cross-platform support (Linux, macOS, Windows)

## Dependencies

sage uses minimal, well-maintained dependencies:

- **click** - Modern command-line interface framework
- **nava** - Cross-platform audio playback for notifications
- **platformdirs** - Cross-platform config directory handling

## Philosophy

sage is built on the principle that tools should adapt to how you naturally think, not force you to learn arbitrary syntax. Time is personal and contextual - sometimes you think "25 minutes," sometimes "25m," sometimes you want a named timer for your routine.

The interface is intentionally minimal and distraction-free. When timing something, you want to focus on that activity, not on managing the timer. sage gets out of your way while providing exactly the functionality you need.

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

---

*sage - because timing shouldn't be complicated.*
