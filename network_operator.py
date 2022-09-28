
class DeviceService:

    def down_device(self,dev):
        cmd = f'ifconfig {dev} down'

    def up_device(self,dev):
        cmd = f'nmcli device connect {dev}'