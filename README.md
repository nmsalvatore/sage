# sage

sage is a clean and easy-to-use CLI timer and stopwatch.

## Usage

sage provides a simple and intuitive command line interface.

### `sage timer`

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

#### Custom timers

To run a custom timer, simply provide the timer's name as the argument
following `sage timer`. To test this functionality yourself, sage
includes a 25 minute pomodoro timer by default which can be run with
the following command.

```bash
sage timer pomodoro
```

### `sage create`

As mentioned above, sage lets you create your own custom timers. You
can do so with `sage create <name> <duration>`. The name argument can
be any string and the duration follows the same rules as are used in
`sage timers`.

Here are some examples.

```bash
sage create potato 55m
sage create titanic "3 hours 14 minutes"
sage create rice --minutes 15 --seconds 30
```

### `sage update` - TODO

### `sage rename` - TODO

### `sage delete` - NEEDS DESCRIPTION

### `sage timers` - NEEDS DESCRIPTION

### `sage stopwatch` - TODO

sage also provides a stopwatch (or an ascending timer?), which can be
loaded using `sage stopwatch`.
