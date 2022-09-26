
class DeviceService:

    def down_device(self,dev):
        cmd = f'nmcli device down {dev}'

    def up_device(self,dev):
        cmd = f'nmcli device up {dev}'