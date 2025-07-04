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
sage timer -m 15                            # 15 minute timer
sage timer --hours 1 --minutes 30           # 1 hour 30 minute timer
sage timer -s 45                            # 45 second timer
sage timer --seconds 30 -m 2                # 2 minute 30 second timer
```

#### Human-readable time strings

We're not all robots, so `sage timer` also accepts human-readable time
strings. You can even mix and match unit formats.

```bash
sage timer 25m                              # 25 minute timer
sage timer "10 minutes 30 sec"              # 10 minute 30 second timer
sage timer 3min25s                          # 3 minute 25 second timer
```

#### Custom timers

To run a custom timer, simply provide the timer's name as the argument
following `sage timer`. To test this functionality yourself, sage
includes a 25 minute pomodoro timer by default which can be run with
the following command:

```bash
sage timer pomodoro
```

### `sage timers` - IN PROGRESS

As mentioned above, sage lets you create custom timers, which are
managed under `sage timers`. Here you can create, update, rename, and
delete timers. The commands available under `sage timers` are as
follows:

- `sage timers list`
- `sage timers create <timer_name> <timer_duration>`
- `sage timers update <timer_name> <timer_duration>`
- `sage timers rename <timer_name> <new_timer_name>`
- `sage timers delete <timer_name>`

Here are some more practical examples of usage.

```bash
sage timers list                            # list all custom timers
sage timers create potato 55m               # create a 55 minute timer named 'potato'
sage timers update potato -m 15 -s 30       # change duration of 'potato' to 15 minutes 30 seconds
sage timers rename potato rice              # change name of 'potato' to 'rice'
sage timers delete rice                     # delete rice
```

### `sage stopwatch` - TODO

sage also provides a stopwatch (or an ascending timer?), which can be
loaded using `sage stopwatch`.
