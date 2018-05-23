from api import Api

class Action():
    def __init__ (self, *, config=None):
        self.api = Api(config=config)
        self.states = {
                'at work': {
                    'name': 'at work',
                    'exec': self.clock_out
                },
                'off work': {
                    'name': 'off work',
                    'exec': self.clock_in
                }
            }

        self.state = self.states[self.get_initial_state()]

    def get_initial_state(self):
        initial_state = self.api.get_state()
        return initial_state

    def get_state(self):
        return self.state

    def set_state(self, *, state_name):
        self.state = self.states[state_name]
        self.api.set_state(state_name=state_name)

    def clock_in(self, *, day=None, time=None):
        self.set_state(state_name='at work')
        self.api.clock_in(day=day, time=time)

    def clock_out(self, *, day=None, time=None):
        self.set_state(state_name='off work')
        self.api.clock_out(day=day, time=time)

