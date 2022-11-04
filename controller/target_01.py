import re
import config_file
import exec_command
import utils
import resources_operator
import network_operator

class QuorumTest(object):
    """
    quorum(q) target01(t01)
    """
    def __int__(self,dev):
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
        self.drbd_cmd = resources_operator.DRBD()
        self.device_cmd = network_operator.DeviceService()


    def quorum_a_loss(self,dev):
        self.device_cmd.down_device(self.controller_node,dev=dev)
        node_resutl = self.drbd_cmd.drbdadm_status(self.controller_node)
        node01_resutl = self.drbd_cmd.drbdadm_status(self.satellite_node01)
        node02_resutl = self.drbd_cmd.drbdadm_status(self.satellite_node02)
        quorum_node = re.findall('quorum:([\W]*)',str(node_resutl))
        quorum_node01 = re.findall('quorum:([\W]*)', str(node01_resutl))
        quorum_node02 = re.findall('quorum:([\W]*)', str(node02_resutl))
        if quorum_node == 'quorum:no' and quorum_node01 != 'quorum:no' and quorum_node02 != 'quorum:no':
            print('test pass')
            self.device_cmd.up_device(self.controller_node,dev=dev)

    def quorum_c_loss(self,dev):
        self.device_cmd.down_device(self.satellite_node02, dev=dev)
        node_resutl = self.drbd_cmd.drbdadm_status(self.controller_node)
        node01_resutl = self.drbd_cmd.drbdadm_status(self.satellite_node01)
        node02_resutl = self.drbd_cmd.drbdadm_status(self.satellite_node02)
        quorum_node = re.findall('quorum:([\W]*)', str(node_resutl))
        quorum_node01 = re.findall('quorum:([\W]*)', str(node01_resutl))
        quorum_node02 = re.findall('quorum:([\W]*)', str(node02_resutl))
        if quorum_node02 == 'quorum:no' and quorum_node01 != 'quorum:no' and quorum_node != 'quorum:no':
            print('test pass')
            self.device_cmd.up_device(self.satellite_node02,dev=dev)
    def quorum_ab_loss(self,dev):
        self.device_cmd.down_device(self.controller_node, dev=dev)
        self.device_cmd.down_device(self.satellite_node01, dev=dev)
        node_resutl = self.drbd_cmd.drbdadm_status(self.controller_node)
        node01_resutl = self.drbd_cmd.drbdadm_status(self.satellite_node01)
        node02_resutl = self.drbd_cmd.drbdadm_status(self.satellite_node02)
        quorum_node = re.findall('quorum:([\W]*)', str(node_resutl))
        quorum_node01 = re.findall('quorum:([\W]*)', str(node01_resutl))
        quorum_node02 = re.findall('quorum:([\W]*)', str(node02_resutl))
        if quorum_node02 == 'quorum:no' and quorum_node01 == 'quorum:no' and quorum_node == 'quorum:no':
            self.device_cmd.up_device(self.satellite_node01, dev=dev)
            node_resutl = self.drbd_cmd.drbdadm_status(self.controller_node)
            node01_resutl = self.drbd_cmd.drbdadm_status(self.satellite_node01)
            node02_resutl = self.drbd_cmd.drbdadm_status(self.satellite_node02)
            quorum_node = re.findall('quorum:([\W]*)', str(node_resutl))
            quorum_node01 = re.findall('quorum:([\W]*)', str(node01_resutl))
            quorum_node02 = re.findall('quorum:([\W]*)', str(node02_resutl))
            if quorum_node02 == 'quorum:no' and quorum_node01 == 'quorum:no' and quorum_node == 'quorum:no':
                self.device_cmd.up_device(self.controller_node, dev=dev)
                node_resutl = self.drbd_cmd.drbdadm_status(self.controller_node)
                node01_resutl = self.drbd_cmd.drbdadm_status(self.satellite_node01)
                node02_resutl = self.drbd_cmd.drbdadm_status(self.satellite_node02)
                quorum_node = re.findall('quorum:([\W]*)', str(node_resutl))
                quorum_node01 = re.findall('quorum:([\W]*)', str(node01_resutl))
                quorum_node02 = re.findall('quorum:([\W]*)', str(node02_resutl))
                if quorum_node02 != 'quorum:no' and quorum_node01 != 'quorum:no' and quorum_node != 'quorum:no':
                    print('test pass')
    def main(self):
        quorumtest = QuorumTest()
        quorumtest.quorum_a_loss()
        quorumtest.quorum_c_loss()
        quorumtest.quorum_ab_loss()