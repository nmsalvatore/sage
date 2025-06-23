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
sage timer -m 15                    # 15 minute timer
sage timer -h 1 -m 30               # 1 hour 30 minute timer
sage timer -s 45                    # 45 second timer
sage timer -s 30 -m 2               # 2 minute 30 second timer
```

#### Human-readable time strings

We're not all robots, so `sage timer` also accepts human-readable time
strings. You can even mix and match unit formats.

```bash
sage timer 25m                      # 25 minute timer
sage timer "10m 30s"                # 10 minute 30 second timer
sage timer 3min25s                  # 3 minute 25 second timer
```

#### Custom names - TODO

Timers can also be saved with custom names by using the `--name` flag,
followed by a name. To load a custom timer, pass the timer name after
`sage timer`. For example, sage includes a 25 minute pomodoro timer by
default with the name `pomodoro`, which can be loaded with `sage timer
pomodoro`.

Here are some other examples.

```bash
sage timer -h 1 --name potato       # creates a 1 hour timer called `potato`
sage timer potato                   # runs 1 hour timer
sage timer -m 55 --name potato      # updates `potato` to 55 minute timer
sage timer potato                   # runs 55 minute timer because it was updated above
```

To view all of your custom timers, use `sage timer list`.

To delete a custom timer, use `sage timer delete <custom_name>`. If I
wanted to delete `potato` for instance, I'd use `sage timer delete
potato`.

### `sage stopwatch` - TODO

sage also provides a stopwatch (or an ascending timer?), which can be
loaded using `sage stopwatch`.
