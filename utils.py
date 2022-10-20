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

class RWData:
    def dd_write(self,device_name):
        cmd = f'dd if=/dev/urandom of={device_name} oflag=direct status=progress'
        return cmd

    def dd_read(self,device_name,read_test_path):
        cmd = f"dd if={device_name} of={read_test_path} oflag=direct status=progress"

    def kill_dd(self,dd_pid):
        cmd = f'kill {dd_pid}'
        return cmd