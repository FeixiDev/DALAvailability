from prettytable import PrettyTable
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

    def dd_write(self,device_name, ssh_conn=None):
        cmd = f'dd if=/dev/urandom of={device_name} oflag=direct status=progress'
        result = exec_cmd(cmd,ssh_conn)
        return result


    def dd_read(self,device_name,read_test_path, ssh_conn=None):
        cmd = f"dd if={device_name} of={read_test_path} oflag=direct status=progress"
        result = exec_cmd(cmd,ssh_conn)
        return result


    def kill_dd(self,dd_pid, ssh_conn=None):
        cmd = f'kill {dd_pid}'
        result = exec_cmd(cmd,ssh_conn)
        return result

        

class Table(object):
    def __init__(self,field_name):
        self.table = PrettyTable(field_name)

    def add_row(self, list_data):
        self.table.add_row(list_data)

    def print_table(self):
        print(self.table)