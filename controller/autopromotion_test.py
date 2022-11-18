import config_file
import resources_operator
import exec_command
import utils
import re
import sys
import time
from threading import Thread




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
        self.dd_cmds = utils.RWData()
        check_cmd = resources_operator.Linstor.check_resource_detailed('resourcetest01',self.controller_node)
        result = re.findall(f'\|([\w\s\/]+)', check_cmd)
        self.device_name = result[5].strip()

    def use_dd_to_write_data(self, obj_ssh):
        try:
            print("................................线程1:开始执行dd写数据操作")
            dd_write = self.dd_cmds.dd_write(self.device_name, obj_ssh)
            time.sleep(5)
            print(".....................dd写数据操作执行完毕,dd进程已被关闭")
        except:
            print("dd写数据操作执行失败")
            sys.exit()


    def start_dd_write(self):
        state = Thread(target=self.use_dd_to_write_data)
        state.setDaemon(True)
        state.start()

    def kill_dd(self, obj_ssh):
        try:
            process_info = utils.exec_cmd('ps -A | grep dd', obj_ssh)
            result01 = re.findall(f'([\d]+) \?        \w\w:\w\w:\w\w dd',process_info)
            r_dd_pid = result01[0]
            kill_dd_cmd = self.dd_cmds.kill_dd(r_dd_pid)
            utils.exec_cmd(kill_dd_cmd, obj_ssh)
            print("dd进程已终止")
        except:
            print("停止dd写数据出现错误")
            sys.exit()



    def diskful_mount(self):
        print("diskful_mount测试开始")
        self.disk_cmd.mount_disk(self.device_name, self.controller_node)
        node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
        node_role = re.findall('role:([\w]*)', str(node_result))
        try:
            if node_role[0] == 'role:Primary' and node_role[1] == 'role:Secondary' and node_role[2] == 'role:Secondary':
                print('节点状态正常')
                time.sleep(2)
                self.disk_cmd.umount_disk(self.device_name,self.controller_node)
                node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
                node_role = re.findall('role:([\w]*)', str(node_result))
                if node_role[0] == 'role:Secondary':
                    print("diskful_mount测试通过")
        except:
            print("节点状态异常,测试退出")
            sys.exit()

    def diskless_mount(self):
        print("diskless_mount测试开始")
        self.disk_cmd.mount_disk(self.device_name, self.satellite_node02)
        node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
        node_role = re.findall('role:([\w]*)', str(node_result))
        try:
            if node_role[0] == 'role:Secondary' and node_role[1] == 'role:Secondary' and node_role[2] == 'role:Primary':
                print('节点状态正常')
                time.sleep(2)
                self.disk_cmd.umount_disk(self.device_name, self.satellite_node02)
                node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
                node_role = re.findall('role:([\w]*)', str(node_result))
                if node_role[2] == 'role:Secondary':
                    print("diskless_mount测试通过")
        except:
            print("节点状态异常，测试退出")
            sys.exit()

    def diskful_dd(self):
        print("diskful_dd测试开始")
        self.use_dd_to_write_data(self.controller_node)
        node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
        node_role = re.findall('role:([\w]*)', str(node_result))
        try:
            if node_role[0] == 'role:Primary' and node_role[1] == 'role:Secondary' and node_role[2] == 'role:Secondary':
                self.kill_dd(self.controller_node)
                node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
                node_role = re.findall('role:([\w]*)', str(node_result))
                if node_role[0] == 'role:Secondary':
                    print("节点状态正常，测试通过")
        except:
            print("节点状态异常，测试退出")
            sys.exit()

    def diskless_dd(self):
        print("diskless_dd测试开始")
        self.use_dd_to_write_data(self.satellite_node02)
        node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
        node_role = re.findall('role:([\w]*)', str(node_result))
        try:
            if node_role[0] == 'role:Secondary' and node_role[1] == 'role:Secondary' and node_role[2] == 'role:Primary':
                self.kill_dd(self.satellite_node02)
                node_result = self.drbd_cmd.drbdadm_status(self.controller_node)
                node_role = re.findall('role:([\w]*)', str(node_result))
                if node_role[2] == 'role:Secondary':
                    print("节点状态正常，测试通过")
        except:
            print("节点状态异常，测试退出")
            sys.exit()

def run():
    test_automatic_promotion = AutomaticPromotion()
    test_automatic_promotion.diskful_mount()
    test_automatic_promotion.diskless_mount()
    test_automatic_promotion.diskful_dd()
    test_automatic_promotion.diskless_dd()

