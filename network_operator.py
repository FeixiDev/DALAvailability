import exec_command
class DeviceService(object):
    def __int__(self, ssh_conn=None):
        self.ssh_conn = ssh_conn
        self.obj_conn = exec_command.SSHconn()
    def down_device(self,dev):
        cmd = f'ifconfig {dev} down'
        result = self.obj_conn.exec_cmd(cmd, self.ssh_conn)
        return result


    def up_device(self,dev):
        cmd = f'nmcli device connect {dev}'
        result = self.obj_conn.exec_cmd(cmd, self.ssh_conn)
        return result
