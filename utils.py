

class RWData:
    def dd_write(self,device_name):
        cmd = f'dd if=/dev/urandom of={device_name} oflag=direct status=progress'

    def kill_dd(self,dd_pid):
        cmd = f'kill {dd_pid}'