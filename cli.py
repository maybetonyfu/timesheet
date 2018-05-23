"""Timesheet.

Usage:
  cli.py punch
  cli.py clockin [(--date=DATE --time=TIME)]
  cli.py clockout [(--date=DATE --time=TIME)]
  cli.py status
  cli.py leave
  cli.py enter
  cli.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from action import Action
from datetime import datetime
import toml
import pytz

def punch(action):
    print('punch')

def clock_in(action, day, time):
    action.clock_in(day=day, time=time)
    print('clock in')

def clock_out(action, day, time):
    action.clock_out(day=day, time=time)
    print('clock out')

def check_status(action):
    state = action.get_state()
    print(state['name'])

def leave(action):
    action.set_state(state_name='off work')

def enter(action):
    action.set_state(state_name='at work')

def local_time_to_utc_time(*, day=None, time=None):
    melbourne = pytz.timezone("Australia/Melbourne")
    time_string = f'{day} {time}'
    time = datetime.strptime(time_string, '%Y-%m-%d %H:%M')
    utc_time = melbourne.localize(time, is_dst=None).astimezone(pytz.utc)
    return utc_time.strftime ("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    arguments = docopt(__doc__)
    config = toml.load('config.toml')
    action = Action(config=config)

    if arguments['clockin']:
        if arguments['--date'] and arguments['--time']:
            day = arguments['--date']
            time = local_time_to_utc_time(day=arguments['--date'], time=arguments['--time'])
            clock_in(action, day, time)
        else:
            day = datetime.now().strftime("%Y-%m-%d")
            time = datetime.utcnow().isoformat()
            clock_in(action, day, time)

    elif arguments['clockout']:
        if arguments['--date'] and arguments['--time']:
            day = arguments['--date']
            time = local_time_to_utc_time(day=arguments['--date'], time=arguments['--time'])
            clock_out(action, day, time)
        else:
            day = datetime.now().strftime("%Y-%m-%d")
            time = datetime.utcnow().isoformat()
            clock_out(action, day, time)

    elif arguments['status']:
        check_status(action)

    elif arguments['leave']:
        leave(action)

    elif arguments['enter']:
        enter(action)

    elif arguments['punch']:
        enter(action)