import config_file
import resources_operator
import exec_command
import utils
import re


class AutomaticPromotion(object):
    """
     Automatic Promotion test
    """

    def __int__(self):
        self.yaml_file = config_file.ConfFile('../config.yaml')
        self.yaml_info_list = self.yaml_file.read_yaml()
        self.controller_node = exec_command.SSHconn(host=self.yaml_info_list['node'][0]['ip']
                                                    , username=self.yaml_info_list['node'][0]['username']
                                                    , password=self.yaml_info_list['node'][0]['password'])
        self.satellite_node01 = exec_command.SSHconn(host=self.yaml_info_list['node'][1]['ip']
                                                     , username=self.yaml_info_list['node'][1]['username']
                                                     , password=self.yaml_info_list['node'][1]['password'])
        self.satellite_node02 = exec_command.SSHconn(host=self.yaml_info_list['node'][2]['ip']
                                                     , username=self.yaml_info_list['node'][2]['username']
                                                     , password=self.yaml_info_list['node'][2]['password'])
        self.disk_cmd = resources_operator.DISK()
        self.drbd_cmd = resources_operator.DRBD()
        self.rw_cmd = utils.RWData()

    def diskful_mount(self, drbd_route):
        self.disk_cmd.mount_disk(drbd_route, self.controller_node)
        node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
        node_role = re.findall('role:([\w]*)', str(node_result))
        if node_role[0] == 'role:Primary' and node_role[1] == 'role:Secondary' and node_role[2] == 'role:Secondary':
            self.disk_cmd.umount_disk(self.controller_node)
            node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
            node_role = re.findall('role:([\w]*)', str(node_result))
            if node_role[0] == 'role:Secondary':
                print(node_role[0])

    def diskless_mount(self, drbd_route):
        self.disk_cmd.mount_disk(drbd_route, self.satellite_node02)
        node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
        node_role = re.findall('role:([\w]*)', str(node_result))
        if node_role[0] == 'role:Secondary' and node_role[1] == 'role:Secondary' and node_role[2] == 'role:Primary':
            self.disk_cmd.umount_disk(self.satellite_node02)
            node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
            node_role = re.findall('role:([\w]*)', str(node_result))
            if node_role[2] == 'role:Secondary':
                print(node_role[2])

    def diskful_dd(self, device_name, dd_pid):
        self.rw_cmd.dd_write(device_name, self.controller_node)
        node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
        node_role = re.findall('role:([\w]*)', str(node_result))
        if node_role[0] == 'role:Primary' and node_role[1] == 'role:Secondary' and node_role[2] == 'role:Secondary':
            self.rw_cmd.kill_dd(dd_pid, self.controller_node)
            node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
            node_role = re.findall('role:([\w]*)', str(node_result))
            if node_role[0] == 'role:Secondary':
                print(node_role[0])

    def diskless_dd(self, device_name, dd_pid):
        self.rw_cmd.dd_write(device_name, self.satellite_node02)
        node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
        node_role = re.findall('role:([\w]*)', str(node_result))
        if node_role[0] == 'role:Secondary' and node_role[1] == 'role:Secondary' and node_role[2] == 'role:Primary':
            self.rw_cmd.kill_dd(dd_pid, self.satellite_node02)
            node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
            node_role = re.findall('role:([\w]*)', str(node_result))
            if node_role[2] == 'role:Secondary':
                print(node_role[2])
    def main(self):
        test_automatic_promotion = AutomaticPromotion()
        test_automatic_promotion.diskful_mount()
        test_automatic_promotion.diskless_mount()
        test_automatic_promotion.diskful_dd()
        test_automatic_promotion.diskless_dd()
