import prettytable

class RWData:
    def dd_write(self,device_name):
        cmd = f'dd if=/dev/urandom of={device_name} oflag=direct status=progress'

    def kill_dd(self,dd_pid):
        cmd = f'kill {dd_pid}'

class Table(object):
    def __init__(self):
        self.header = None
        self.data = None
        self.table = prettytable.PrettyTable()

    def add_data(self, list_data):
        self.table.add_row(list_data)

    def add_column(self, fieldname, list_column):
        self.table.add_column(fieldname, list_column)

    def print_table(self):
        self.table.field_names = self.header
        print(self.table)