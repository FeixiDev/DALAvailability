import exec_command
import config_file
import utils

class DiscardSupport(object):
    """
      LTrim/Discard support (diskless + diskful)
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


    def discard_support(self, drbd_route):
        cat_cmd = f'cat /sys/block/{drbd_route}/queue/discard_max_bytes'
        node_resutl = utils.exec_cmd(cat_cmd, self.controller_node)
        node01_resutl = utils.exec_cmd(cat_cmd, self.satellite_node01)
        node02_resutl = utils.exec_cmd(cat_cmd, self.satellite_node02)
        if str(node_resutl) == '0' and str(node01_resutl) == '0' and str(node02_resutl) == '0' :
            print('Tset,passed')

        elif str(node_resutl) =='0' or str(node01_resutl) == '0' and str(node02_resutl) == '0':
            print('Test,passed')

        else:
            print('Test,failed')