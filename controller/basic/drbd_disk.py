import yaml
import time
import re
import sys
from ... import utils
from ... import resources_operator
from ... import exec_command

class YamlRead:
    def __init__(self):
        self.yaml_info = self.yaml_read()

    def yaml_read(self):
        with open('../config.yaml') as f:
            config = yaml.safe_load(f)
        return config

class MainOperation:
    def __init__(self):
        self.obj_yaml = YamlRead()
        self.yaml_info_list = self.obj_yaml.yaml_info
        self.linstor_cmds = resources_operator.Linstor()
        self.drbd_cmds = resources_operator.DRBD()
        self.lvm_cmds = resources_operator.LVM()
        self.obj_controller = exec_command.SSHconn(host=self.yaml_info_list['node'][0]['ip']
                                       ,username=self.yaml_info_list['node'][0]['username']
                                       ,password=self.yaml_info_list['node'][0]['password'])
        self.obj_satellite01 = exec_command.SSHconn(host=self.yaml_info_list['node'][1]['ip']
                                       ,username=self.yaml_info_list['node'][1]['username']
                                       ,password=self.yaml_info_list['node'][1]['password'])
        self.obj_satellite02 = exec_command.SSHconn(host=self.yaml_info_list['node'][2]['ip']
                                       ,username=self.yaml_info_list['node'][2]['username']
                                       ,password=self.yaml_info_list['node'][2]['password'])

    def create_res(self, hostname, disk, ip):
        content = f"""
resource test {{
    on {hostname} {{
        device /dev/drbd1;
        disk {disk};
        address {ip}:7789;
        node-id 0;
        meta-disk internal;
    }}
}}
        """
        with open('./test.res', 'w') as f:
            f.write(content)
        try:
            self.obj_controller.upload('./test.res','/etc/drbd.d/')
        except Exception as r:
            print(f"res配置文件传输异常，错误：{r}")



    def create_resource(self):
        utils.exec_cmd("drbdadm create-md -y test.res",self.obj_controller)
        utils.exec_cmd("drbdadm up test",self.obj_controller)
        utils.exec_cmd("drbdadm primary --force test",self.obj_controller)
        resoult01 = utils.exec_cmd("drbdadm status test",self.obj_controller)
        re_resoult01 = re.findall(r'test role:primary',resoult01)
        if re_resoult01 != 'test role:primary':
            print("drbd资源状态异常")
            sys.exit()
        utils.exec_cmd("drbdadm down test",self.obj_controller)
        utils.exec_cmd("rm /root/test.res")