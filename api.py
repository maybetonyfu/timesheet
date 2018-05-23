from airtable import Airtable

class Api ():
    def __init__(self, *, config=None):
        api_key = config['airtable_api_key']
        base_key = config['airtable_base_key']
        table_name_state = config['table_name_state']
        table_name_timesheet = config['table_name_timesheet']
        self.pricipal = config['principal']
        self.lunch_break = config['lunch_break']
        self.state = Airtable(base_key, table_name_state, api_key)
        self.timesheet = Airtable(base_key, table_name_timesheet, api_key)

    def get_state(self):
        record = self.state.match('state_principal', self.pricipal)
        return record['fields']['state_name']

    def set_state(self, * , state_name=None):
        record = {'state_name': state_name }
        self.state.update_by_field('state_principal', self.pricipal, record)

    def clock_in(self, *, day=None, time=None):
        record = {
            'record_day': day,
            'clock_in_time': time,
            'lunch_break': self.lunch_break
        }
        self.timesheet.insert(record)

    def clock_out(self, *, day=None, time=None):
        record = {
            'clock_out_time': time
        }
        self.timesheet.update_by_field('record_day', day, record)
