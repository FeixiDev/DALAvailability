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
