import prettytable
import subprocess
import sys
import paramiko
import log
import exec_command

def exec_cmd(cmd, conn=None):
    local_obj = exec_command.LocalProcess()
    if conn:
        result = conn.exec_cmd(cmd)
    else:
        result = local_obj.exec_cmd(cmd)
    log.Log().write_to_log(cmd, result['rt'], 30)
    if result['st']:
        pass
        # f_result = result['rt'].rstrip('\n')
    if result['st'] is False:
        sys.exit()
    return result['rt']


class RWData(object):
    def __int__(self, ssh_conn=None):
        self.ssh_conn = ssh_conn
        self.obj_conn = exec_command.SSHconn()
    def dd_write(self,device_name):
        cmd = f'dd if=/dev/urandom of={device_name} oflag=direct status=progress'
        result = self.obj_conn.exec_cmd(cmd, self.ssh_conn)
        return result


    def dd_read(self,device_name,read_test_path):
        cmd = f"dd if={device_name} of={read_test_path} oflag=direct status=progress"
        result = self.obj_conn.exec_cmd(cmd, self.ssh_conn)
        return result


    def kill_dd(self,dd_pid):
        cmd = f'kill {dd_pid}'
        result = self.obj_conn.exec_cmd(cmd, self.ssh_conn)
        return result

        

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
