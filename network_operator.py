import utils
class DeviceService(object):

    def down_device(self,dev, ssh_conn=None):
        cmd = f'ifconfig {dev} down'
        result = utils.exec_cmd(cmd,ssh_conn)
        return result


    def up_device(self,dev, ssh_conn=None):
        cmd = f'nmcli device connect {dev}'
        result = utils.exec_cmd(cmd,ssh_conn)
        return result

class Scp:

    def local_to_remote_file(self,local_file,remote_username,remote_ip,remote_folder,ssh_conn=None):
        cmd = f'scp {local_file} {remote_username}@{remote_ip}:{remote_folder}'
        result = utils.exec_cmd(cmd,ssh_conn)
        return result