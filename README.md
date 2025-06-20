# Fizz

Fizz is a clean and easy-to-use CLI timer and stopwatch.

## Usage

Fizz provides a simple and intuitive command line interface. The following examples provide a comprehensive view of Fizz usage.

```bash
# Timer commands
fizz timer -m 15        # 15 minute timer
fizz timer -h 1 -m 30   # 1 hour 30 minute timer
fizz timer -s 45        # 45 second timer
fizz timer -s 30 -m 2   # 2 minute 30 second timer, argument order doesn't matter

# Stopwatch command
fizz stopwatch

# Custom timers
fizz timer pomodoro                 # runs 25 minute timer, included by default
fizz timer -h 1 --name potato       # creates a 1 hour timer called `potato`
fizz timer potato                   # runs 1 hour timer
fizz timer -m 55 --name potato      # updates `potato` to 55 minute timer
fizz timer potato                   # runs 55 minute timer
fizz timer list                     # shows list of custom timers
fizz timer delete potato            # deletes custom timer `potato`
```
