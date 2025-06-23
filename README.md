# fizz

fizz is a clean and easy-to-use CLI timer and stopwatch.

## Usage

fizz provides a simple and intuitive command line interface.

### `fizz timer` - IN PROGRESS

The fizz timer is built to be intuitive, the hope being that it works
how you expect it to work. Since we all intuit differently, timers can
loaded in multiple ways.

#### Time unit flags

Use option flags to set the timer. Flags can be applied in any order.

- `-h`, `--hours` - set timer hours
- `-m`, `--minutes` - set timer minutes
- `-s`, `--seconds` - set timer seconds

```bash
fizz timer -m 15                    # 15 minute timer
fizz timer -h 1 -m 30               # 1 hour 30 minute timer
fizz timer -s 45                    # 45 second timer
fizz timer -s 30 -m 2               # 2 minute 30 second timer
```

#### Human-readable time strings

We're not all robots, so `fizz timer` also accepts human-readable time
strings. You can even mix and match unit formats.

```bash
fizz timer "25 minutes"             # 25 minute timer
fizz timer "10m 30s"                # 10 minute 30 second timer
fizz timer "2 minute 60 s"          # 3 minute timer
```

#### Custom names - TODO

Timers can also be saved with custom names by using the `--name` flag,
followed by a name. To load a custom timer, pass the timer name after
`fizz timer`. For example, fizz includes a 25 minute pomodoro timer by
default with the name `pomodoro`, which can be loaded with `fizz timer
pomodoro`.

Here are some other examples.

```bash
fizz timer -h 1 --name potato       # creates a 1 hour timer called `potato`
fizz timer potato                   # runs 1 hour timer
fizz timer -m 55 --name potato      # updates `potato` to 55 minute timer
fizz timer potato                   # runs 55 minute timer because it was updated above
```

To view all of your custom timers, use `fizz timer list`.

To delete a custom timer, use `fizz timer delete <custom_name>`. If I
wanted to delete `potato` for instance, I'd use `fizz timer delete
potato`.

### `fizz stopwatch` - TODO

fizz also provides a stopwatch (or an ascending timer?), which can be
loaded using `fizz stopwatch`.
