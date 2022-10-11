import paramiko
import subprocess
import yaml
import utils
import time
import re

class YamlRead:
    def __init__(self):
        self.yaml_info = self.yaml_read()

    def yaml_read(self):
        with open('config.yaml') as f:
            config = yaml.safe_load(f)
        return config

class MainOperation:
    def __init__(self):
        self.obj_yaml = YamlRead()
        self.yaml_info_list = self.obj_yaml.yaml_info


    def configuring_controller(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       ,username=self.yaml_info_list['node'][0]['username']
                                       ,password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd("systemctl start linstor-controller",obj_controller)
        time.sleep(2)
        utils.exec_cmd(f"linstor node create {self.yaml_info_list['node'][0]['name']} {self.yaml_info_list['node'][0]['bond_ip']} --node-type Combined",obj_controller)
        time.sleep(2)
        obj_controller.ssh_close()

    def configuring_satallite(self):
        obj_satallite01 = utils.SSHConn(host=self.yaml_info_list['node'][1]['ip']
                                       ,username=self.yaml_info_list['node'][1]['username']
                                       ,password=self.yaml_info_list['node'][1]['password'])

        utils.exec_cmd("systemctl start linstor-satallite",obj_satallite01)
        time.sleep(2)
        utils.exec_cmd(f"linstor node create {self.yaml_info_list['node'][1]['name']} {self.yaml_info_list['node'][1]['bond_ip']} --node-type Satellite",obj_satallite01)
        time.sleep(2)
        obj_satallite01.ssh_close()

        obj_satallite02 = utils.SSHConn(host=self.yaml_info_list['node'][2]['ip']
                                       ,username=self.yaml_info_list['node'][2]['username']
                                       ,password=self.yaml_info_list['node'][2]['password'])

        utils.exec_cmd("systemctl start linstor-satallite",obj_satallite02)
        time.sleep(2)
        utils.exec_cmd(f"linstor node create {self.yaml_info_list['node'][2]['name']} {self.yaml_info_list['node'][2]['bond_ip']} --node-type Satellite",obj_satallite02)
        time.sleep(2)
        obj_satallite02.ssh_close()

    def create_vg_lvm(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       ,username=self.yaml_info_list['node'][0]['username']
                                       ,password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd(f"pvcreate /dev/{self.yaml_info_list['node'][0]['disk']}",obj_controller)
        time.sleep(2)
        utils.exec_cmd(f"vgcreate vgtest /dev/{self.yaml_info_list['node'][0]['disk']}",obj_controller)
        time.sleep(2)
        utils.exec_cmd(f"lvcreate -l 50%VG -T vgtest/lvtest",obj_controller)
        time.sleep(2)
        utils.exec_cmd(f"linstor sp create lvm {self.yaml_info_list['node'][0]['name']} sptest vgtest",obj_controller)

        obj_satallite01 = utils.SSHConn(host=self.yaml_info_list['node'][1]['ip']
                                       ,username=self.yaml_info_list['node'][1]['username']
                                       ,password=self.yaml_info_list['node'][1]['password'])
        utils.exec_cmd(f"pvcreate /dev/{self.yaml_info_list['node'][1]['disk']}",obj_satallite01)
        time.sleep(2)
        utils.exec_cmd(f"vgcreate vgtest /dev/{self.yaml_info_list['node'][1]['disk']}",obj_satallite01)
        time.sleep(2)
        utils.exec_cmd(f"lvcreate -l 50%VG -T vgtest/lvtest",obj_satallite01)
        time.sleep(2)
        utils.exec_cmd(f"linstor sp create lvm {self.yaml_info_list['node'][1]['name']} sptest vgtest",obj_satallite01)

        obj_satallite02 = utils.SSHConn(host=self.yaml_info_list['node'][2]['ip']
                                       ,username=self.yaml_info_list['node'][2]['username']
                                       ,password=self.yaml_info_list['node'][2]['password'])
        utils.exec_cmd(f"pvcreate /dev/{self.yaml_info_list['node'][2]['disk']}",obj_satallite02)
        time.sleep(2)
        utils.exec_cmd(f"vgcreate vgtest /dev/{self.yaml_info_list['node'][2]['disk']}",obj_satallite02)
        time.sleep(2)
        utils.exec_cmd(f"lvcreate -l 50%VG -T vgtest/lvtest",obj_satallite02)
        time.sleep(2)
        utils.exec_cmd(f"linstor sp create lvm {self.yaml_info_list['node'][2]['name']} sptest vgtest",obj_satallite02)

    def delete_node_all(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       ,username=self.yaml_info_list['node'][0]['username']
                                       ,password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd(f"linstor n d {self.yaml_info_list['node'][0]['username']}",obj_controller)
        utils.exec_cmd(f"linstor n d {self.yaml_info_list['node'][1]['username']}",obj_controller)
        utils.exec_cmd(f"linstor n d {self.yaml_info_list['node'][2]['username']}",obj_controller)


    def delete_vg_all(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       ,username=self.yaml_info_list['node'][0]['username']
                                       ,password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd(f"vgremove vgtest",obj_controller)

        obj_satallite01 = utils.SSHConn(host=self.yaml_info_list['node'][1]['ip']
                                       ,username=self.yaml_info_list['node'][1]['username']
                                       ,password=self.yaml_info_list['node'][1]['password'])
        utils.exec_cmd(f"vgremove vgtest",obj_satallite01)

        obj_satallite02 = utils.SSHConn(host=self.yaml_info_list['node'][2]['ip']
                                       ,username=self.yaml_info_list['node'][2]['username']
                                       ,password=self.yaml_info_list['node'][2]['password'])
        utils.exec_cmd(f"vgremove vgtest",obj_satallite02)


    def create_sp(self):
        obj_satallite01 = utils.SSHConn(host=self.yaml_info_list['node'][1]['ip']
                                       ,username=self.yaml_info_list['node'][1]['username']
                                       ,password=self.yaml_info_list['node'][1]['password'])
        utils.exec_cmd(f"linstor sp create lvm {self.yaml_info_list['node'][1]['name']} sptest vgtest",obj_satallite01)
        obj_satallite02 = utils.SSHConn(host=self.yaml_info_list['node'][2]['ip']
                                       ,username=self.yaml_info_list['node'][2]['username']
                                       ,password=self.yaml_info_list['node'][2]['password'])
        utils.exec_cmd(f"linstor sp create lvm {self.yaml_info_list['node'][2]['name']} sptest vgtest",obj_satallite02)

    def delete_sp(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       , username=self.yaml_info_list['node'][0]['username']
                                       , password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd(f"linstor sp d sptest {self.yaml_info_list['node'][0]['username']}", obj_controller)
        utils.exec_cmd(f"linstor sp d sptest {self.yaml_info_list['node'][1]['username']}", obj_controller)
        utils.exec_cmd(f"linstor sp d sptest {self.yaml_info_list['node'][2]['username']}", obj_controller)

    def create_rd_vd_r_3diskful(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       , username=self.yaml_info_list['node'][0]['username']
                                       , password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd("linstor rd create resourcetest01", obj_controller)
        time.sleep(2)
        utils.exec_cmd("linstor vd create resourcetest01 5G", obj_controller)
        time.sleep(2)
        utils.exec_cmd("linstor resource c resourcetest01 --auto-place 3", obj_controller)
        time.sleep(2)

    def delete_rd(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       , username=self.yaml_info_list['node'][0]['username']
                                       , password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd("linstor rd d resourcetest01", obj_controller)

    def delete_r(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       , username=self.yaml_info_list['node'][0]['username']
                                       , password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd(f"linstor r d {self.yaml_info_list['node'][0]['username']} resourcetest01", obj_controller)
        utils.exec_cmd(f"linstor r d {self.yaml_info_list['node'][1]['username']} resourcetest01", obj_controller)
        utils.exec_cmd(f"linstor r d {self.yaml_info_list['node'][2]['username']} resourcetest01", obj_controller)


    def check_drbd(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       , username=self.yaml_info_list['node'][0]['username']
                                       , password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd("linstor r l", obj_controller)
        time.sleep(2)
        utils.exec_cmd("linstor r lv", obj_controller)
        time.sleep(2)
        utils.exec_cmd("drbdmon", obj_controller)
        time.sleep(2)
        utils.exec_cmd("drbdadm status", obj_controller)
        time.sleep(2)
        utils.exec_cmd("drbdsetup status -vs", obj_controller)
        time.sleep(2)
        utils.exec_cmd("drbdsetup events2", obj_controller)
        time.sleep(2)

    def check_error_reports(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       , username=self.yaml_info_list['node'][0]['username']
                                       , password=self.yaml_info_list['node'][0]['password'])
        error_list = utils.exec_cmd("linstor error-reports list", obj_controller)
        time.sleep(2)
        error_number = re.findall(r'\w{8}-\w{5}-\w{6}',error_list)
        utils.exec_cmd(f"linstor error-reports show {error_number[0]}", obj_controller)

    def configuring_resource(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       , username=self.yaml_info_list['node'][0]['username']
                                       , password=self.yaml_info_list['node'][0]['password'])
        info = utils.exec_cmd("linstor r lv | grep giresource", obj_controller)
        data = re.findall(f'\|([\w\s\/]+)', info)
        data1 = data[5]
        dev = data1.strip()
        pass

    def resource_operation_2diskful(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][1]['ip']
                                       , username=self.yaml_info_list['node'][1]['username']
                                       , password=self.yaml_info_list['node'][1]['password'])
        utils.exec_cmd(f"linstor r create {self.yaml_info_list['node'][1]['username']} resourcetest01 --storage-pool sptest", obj_controller)

        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][2]['ip']
                                       , username=self.yaml_info_list['node'][2]['username']
                                       , password=self.yaml_info_list['node'][2]['password'])
        utils.exec_cmd(
            f"linstor r create {self.yaml_info_list['node'][2]['username']} resourcetest01 --storage-pool sptest",obj_controller)

    def resource_operation_2diskful1diskless(self):
        """
        必须在2diskful基础上进行
        """
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       , username=self.yaml_info_list['node'][0]['username']
                                       , password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd(f"linstor r create {self.yaml_info_list['node'][0]['username']} resourcetest01 --diskles", obj_controller)

    def resource_operation_3diskful(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       , username=self.yaml_info_list['node'][0]['username']
                                       , password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd(f"linstor r create resourcetest01 --auto-place 3", obj_controller)

    def exchange_vd_size(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       , username=self.yaml_info_list['node'][0]['username']
                                       , password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd(f"linstor vd set-size resourcetest01 0 20G", obj_controller)

    def rg_operation(self,size):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       , username=self.yaml_info_list['node'][0]['username']
                                       , password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd(f"linstor rg create test01 --storage-pool sptest --place-count 1 ", obj_controller)
        utils.exec_cmd(f"linstor vg create test01", obj_controller)
        utils.exec_cmd(f"linstor rg spawn-resources test01 resourcetest04 {size}", obj_controller)

    def delete_rg(self):
        obj_controller = utils.SSHConn(host=self.yaml_info_list['node'][0]['ip']
                                       , username=self.yaml_info_list['node'][0]['username']
                                       , password=self.yaml_info_list['node'][0]['password'])
        utils.exec_cmd(f"linstor vg d test01 0", obj_controller)
        utils.exec_cmd(f"linstor rg d test01", obj_controller)

def main():
    obj_mainoperation = MainOperation()
    all_cmds = []
    all_cmds.extend('obj_mainoperation.configuring_controller')
    all_cmds.extend('obj_mainoperation.configuring_satallite')
    all_cmds.extend('obj_mainoperation.create_vg_lvm')
    all_cmds.extend('obj_mainoperation.create_rd_vd_r_3diskful')
    all_cmds.extend('obj_mainoperation.delete_r')
    all_cmds.extend('obj_mainoperation.resource_operation_2diskful')
    all_cmds.extend('obj_mainoperation.resource_operation_2diskful1diskless')
    all_cmds.extend('obj_mainoperation.check_drbd')
    all_cmds.extend('obj_mainoperation.check_error_reports')
    all_cmds.extend('obj_mainoperation.exchange_vd_size')
    all_cmds.extend('obj_mainoperation.rg_operation')
    all_cmds.extend('obj_mainoperation.delete_rg')
    all_cmds.extend('obj_mainoperation.delete_rd')

    for i in all_cmds:
        funct = eval(i)
        status = funct

if __name__ == "__main__":
    main()




