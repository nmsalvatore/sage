# sage

sage is a clean and easy-to-use CLI timer and stopwatch.

## Usage

sage provides a simple and intuitive command line interface.

### `sage timer` - IN PROGRESS

The sage timer is built to be intuitive, the hope being that it works
how you expect it to work. Since we all intuit differently, timers can
loaded in multiple ways.

#### Time unit flags

Use option flags to set the timer. Flags can be applied in any order.

- `-h`, `--hours` - set timer hours
- `-m`, `--minutes` - set timer minutes
- `-s`, `--seconds` - set timer seconds

```bash
sage timer -m 15                        # 15 minute timer
sage timer --hours 1 --minutes 30       # 1 hour 30 minute timer
sage timer -s 45                        # 45 second timer
sage timer --seconds 30 -m 2            # 2 minute 30 second timer
```

#### Human-readable time strings

We're not all robots, so `sage timer` also accepts human-readable time
strings. You can even mix and match unit formats.

```bash
sage timer 25m                          # 25 minute timer
sage timer "10 minutes 30 sec"          # 10 minute 30 second timer
sage timer 3min25s                      # 3 minute 25 second timer
```

#### Custom timers - TODO

Timers can also be saved under custom names by using `sage create timer
<name> <duration>`. The timer name can be any valid string and the
timer duration must adhere to the same rules as above. Sage also
provides `update`, `rename` and `delete` commands for managing your
custom timers.

Examples of usage with custom timers can be seen below.

```bash
sage create timer potato 55m            # creates a 55 minute timer with the name "potato"
sage update timer potato "50 minutes"   # updates "potato" duration to 50 minutes
sage rename timer potato pomodoro       # renames timer "potato" to "pomodoro"
sage update pomodoro --minutes 25       # updates "pomodoro" duration to 25 minutes
sage delete timer pomodoro              # deletes timer "pomodoro"
```

To run a custom timer, simply provide the timer's name as the argument
following `sage timer` as you would would a normal timer. So instead of
`sage timer 15mins`, the syntax is `sage timer <name>`. To test this
functionality yourself, sage includes a 25 minute pomodoro timer by
default which can be run with the command below.

```bash
sage timer pomodoro
```

To view a list of all of your custom timers, use `sage list timers`.

### `sage stopwatch` - TODO

sage also provides a stopwatch (or an ascending timer?), which can be
loaded using `sage stopwatch`.
