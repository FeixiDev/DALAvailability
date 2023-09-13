import sys
sys.path.append("..")
import yaml
import time
import re
from utils import exec_command, resources_operator


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
                                                   , username=self.yaml_info_list['node'][0]['username']
                                                   , password=self.yaml_info_list['node'][0]['password'])
        self.obj_satellite01 = exec_command.SSHconn(host=self.yaml_info_list['node'][1]['ip']
                                                    , username=self.yaml_info_list['node'][1]['username']
                                                    , password=self.yaml_info_list['node'][1]['password'])
        self.obj_satellite02 = exec_command.SSHconn(host=self.yaml_info_list['node'][2]['ip']
                                                    , username=self.yaml_info_list['node'][2]['username']
                                                    , password=self.yaml_info_list['node'][2]['password'])


    # def configuring_controller(self):
    #     """
    #     1、开启节点1的controller服务
    #     2、创建节点1的controller节点
    #     """
    #     print("开启节点1的controller服务和创建节点1的controller节点")
    #     start_controller_cmd = self.linstor_cmds.start_controller()
    #     create_node_cmd = self.linstor_cmds.create_node(self.yaml_info_list['node'][0]['name']
    #                                                     ,self.yaml_info_list['node'][0]['ip']
    #                                                     ,'Combined')
    #
    #     utils.exec_cmd(start_controller_cmd,self.obj_controller)
    #     time.sleep(2)
    #     utils.exec_cmd(create_node_cmd,self.obj_controller)
    #     time.sleep(2)
    #
    # def configuring_satallite(self):
    #     """
    #     1、开启节点2的satellite服务
    #     2、创建节点2的satellite节点
    #     3、开启节点3的satellite服务
    #     4、创建节点3的satellite节点
    #     """
    #     print("开启节点2和节点三的satellite服务和创建satellite节点")
    #     start_satellite_cmd = self.linstor_cmds.start_satellite()
    #     create_node_cmd01 = self.linstor_cmds.create_node(self.yaml_info_list['node'][1]['name']
    #                                                     ,self.yaml_info_list['node'][1]['ip']
    #                                                     ,'Satellite')
    #     create_node_cmd02 = self.linstor_cmds.create_node(self.yaml_info_list['node'][2]['name']
    #                                                     ,self.yaml_info_list['node'][2]['ip']
    #                                                     ,'Satellite')
    #
    #     utils.exec_cmd(start_satellite_cmd,self.obj_satellite01)
    #     time.sleep(2)
    #     utils.exec_cmd(create_node_cmd01,self.obj_satellite01)
    #     time.sleep(2)
    #     utils.exec_cmd(start_satellite_cmd,self.obj_satellite02)
    #     time.sleep(2)
    #     utils.exec_cmd(create_node_cmd02,self.obj_satellite02)
    #     time.sleep(2)


    def create_pv_vg_lvm(self):
        """
        分别在三个节点创建pv、vg
        """
        print("分别在三个节点创建pv和vg")
        pvcreate_node1 = self.lvm_cmds.create_pv(self.yaml_info_list['node'][0]['disk_path'],self.obj_controller)
        pvcreate_node2 = self.lvm_cmds.create_pv(self.yaml_info_list['node'][1]['disk_path'], self.obj_satellite01)
        pvcreate_node3 = self.lvm_cmds.create_pv(self.yaml_info_list['node'][2]['disk_path'], self.obj_satellite02)
        vgcreate_node1 = self.lvm_cmds.create_vg(self.yaml_info_list['node'][0]['disk_path'],'vgtest',self.obj_controller)
        vgcreate_node1 = self.lvm_cmds.create_vg(self.yaml_info_list['node'][1]['disk_path'], 'vgtest',self.obj_satellite01)
        vgcreate_node1 = self.lvm_cmds.create_vg(self.yaml_info_list['node'][2]['disk_path'], 'vgtest',self.obj_satellite02)


    def delete_node_all(self):
        """
        删除三个节点的node
        """
        print("删除三个节点的node")
        delete_node1 = self.linstor_cmds.delete_node(self.yaml_info_list['node'][0]['name'],self.obj_controller)
        delete_node2 = self.linstor_cmds.delete_node(self.yaml_info_list['node'][1]['name'],self.obj_satellite01)
        delete_node3 = self.linstor_cmds.delete_node(self.yaml_info_list['node'][2]['name'],self.obj_satellite02)

    def delete_vg_all(self):
        """
        删除三个节点的vg
        """
        print("删除三个节点的vg")
        delete_vg1 = self.lvm_cmds.delete_vg('vgtest',self.obj_controller)
        delete_vg2 = self.lvm_cmds.delete_vg('vgtest', self.obj_satellite01)
        delete_vg3 = self.lvm_cmds.delete_vg('vgtest', self.obj_satellite02)


    def create_sp(self):
        """
        分别在三个节点上创建sp
        """
        print("分别在三个节点上创建sp")
        create_sp1 = self.linstor_cmds.create_sp(self.yaml_info_list['node'][0]['name'],'lvm','sptest','vgtest',self.obj_controller)
        create_sp2 = self.linstor_cmds.create_sp(self.yaml_info_list['node'][1]['name'],'lvm','sptest','vgtest',self.obj_satellite01)
        create_sp3 = self.linstor_cmds.create_sp(self.yaml_info_list['node'][2]['name'],'lvm','sptest','vgtest',self.obj_satellite02)


    def delete_sp(self):
        """
        删除三个节点上的sp
        """
        print("删除三个节点上的sp")
        delete_sp1 = self.linstor_cmds.delete_sp(self.yaml_info_list['node'][0]['name'],'sptest',self.obj_controller)
        delete_sp2 = self.linstor_cmds.delete_sp(self.yaml_info_list['node'][1]['name'],'sptest',self.obj_satellite01)
        delete_sp3 = self.linstor_cmds.delete_sp(self.yaml_info_list['node'][2]['name'],'sptest',self.obj_satellite02)


    def create_rd_vd(self):
        """
        1、创建rd
        2、创建vd
        """
        print("创建rd和vd")
        create_rd = self.linstor_cmds.create_rd('resourcetest01',self.obj_controller)
        create_vd = self.linstor_cmds.create_vd('resourcetest01','5G',self.obj_controller)


    def delete_rd(self):
        """
        删除rd
        """
        print("删除rd")
        delete_rd = self.linstor_cmds.delete_rd('resourcetest01',self.obj_controller)


    def delete_r(self):
        """
        删除所有已创建的r,必须有三个r，不然会直接退出
        """
        print("删除所有已创建的r,必须有三个r，不然会直接退出")
        delete_r1 = self.linstor_cmds.delete_resource(self.yaml_info_list['node'][0]['name'],'resourcetest01',self.obj_controller)
        delete_r2 = self.linstor_cmds.delete_resource(self.yaml_info_list['node'][1]['name'],'resourcetest01',self.obj_controller)
        delete_r3 = self.linstor_cmds.delete_resource(self.yaml_info_list['node'][2]['name'],'resourcetest01',self.obj_controller)


    def check_drbd(self):
        """
        1、linstor r l
        2、linstor r lv
        3、drbdmon
        4、drbdadm status
        5、drbdsetup status -vs
        6、drbdsetup events2
        """
        print("执行linstor检查命令")
        print("linstor r l")
        check_cmd01 = self.linstor_cmds.check_resource(self.obj_controller)
        print("linstor r lv")
        check_cmd02 = self.linstor_cmds.check_resource_lv(self.obj_controller)
        # print("drbdmon")
        # check_cmd03 = self.drbd_cmds.drbdmon(self.obj_controller)
        print("drbdadm status")
        check_cmd04 = self.drbd_cmds.drbdadm_status(self.obj_controller)
        print("drbdsetup status -vs")
        check_cmd05 = self.drbd_cmds.drbdsetup_status(self.obj_controller)
        # print("drbdsetup events2")
        # check_cmd06 = self.drbd_cmds.check_events(self.obj_controller)


    def check_error_reports(self):
        """
        检查error reports
        """
        print("检查error reports")
        check_error_list = self.linstor_cmds.check_error_reports_list(self.obj_controller)
        time.sleep(2)
        error_number = re.findall(r'\w{8}-\w{5}-\w{6}',check_error_list)
        print(error_number)
        error_number01 = error_number[0]

        check_error_cmd = self.linstor_cmds.check_error_reports_specific(error_number01,self.obj_controller)

    def configuring_resource(self):
        """
        配置auto-promote
        """
        print("配置auto-promote")
        adjust_config = self.linstor_cmds.adjust_linstor_resource_settings('auto-promote','no','resourcetest01',self.obj_controller)
        unset_config = self.linstor_cmds.unset_linstor_resource_settings('auto-promote','no','resourcetest01',self.obj_controller)

    def resource_operation_3diskful(self):
        """
        自动放置3diskful
        """
        print("自动放置3diskful")
        create_r = self.linstor_cmds.create_diskful_resource_auto('resourcetest01','3',self.obj_controller)


    def resource_operation_2diskful(self):
        """
        以第二和第三节点创建两个diskful
        """
        print("以第二和第三节点创建两个diskful")
        create_diskful_cmd01 = self.linstor_cmds.create_diskful_resource(self.yaml_info_list['node'][1]['name'],'resourcetest01','sptest',self.obj_satellite01)
        create_diskful_cmd02 = self.linstor_cmds.create_diskful_resource(self.yaml_info_list['node'][2]['name'],'resourcetest01','sptest',self.obj_satellite02)

    def resource_operation_2diskful1diskless(self):
        """
        必须在2diskful基础上进行,新增一个diskless
        """
        print("必须在2diskful基础上进行,新增一个diskless")
        create_diskless_cmd = self.linstor_cmds.create_diskless_resource(self.yaml_info_list['node'][0]['name'],'resourcetest01',self.obj_controller)

    def exchange_vd_size(self):
        """
        改变vd的容量，达成扩容的目的
        """
        print("改变vd的容量，达成扩容的目的")
        change_vdsize_cmd = self.linstor_cmds.adjust_resource_size('resourcetest01','0','10G',self.obj_controller)

    def rg_operation(self):
        """
        1、创建资源组
        2、创建卷组
        3、放置资源
        """
        print("资源组的操作")
        create_rg_cmd = self.linstor_cmds.create_resource_group('rgtest01','sptest','1',self.obj_controller)
        create_vg_cmd = self.linstor_cmds.create_volume_group('rgtest01',self.obj_controller)
        create_r_by_rg_cmd = self.linstor_cmds.create_resource_by_rg('rgtest01','resourcetest03','2G',self.obj_controller)

    def delete_rg(self):
        """
        删除rg
        """
        print("删除rg")
        delete_vg_cmd = self.linstor_cmds.delete_resource_group('rgtest01',self.obj_controller)
        delete_rg_cmd = self.linstor_cmds.delete_volume_group('rgtest01','0',self.obj_controller)


def main():
    obj_mainoperation = MainOperation()
    obj_mainoperation.create_pv_vg_lvm()
    obj_mainoperation.create_sp()
    obj_mainoperation.create_rd_vd()
    obj_mainoperation.resource_operation_3diskful()
    obj_mainoperation.delete_r()
    obj_mainoperation.resource_operation_2diskful()
    obj_mainoperation.resource_operation_2diskful1diskless()
    obj_mainoperation.delete_r()
    #此处有rd、vd，无r
    obj_mainoperation.check_drbd()
    obj_mainoperation.check_error_reports()
    obj_mainoperation.configuring_resource()
    obj_mainoperation.exchange_vd_size()
    obj_mainoperation.rg_operation()
    obj_mainoperation.delete_rd()
    # all_cmds = []
    # all_cmds.extend('obj_mainoperation.configuring_controller')
    # all_cmds.extend('obj_mainoperation.configuring_satallite')
    # all_cmds.extend('obj_mainoperation.create_vg_lvm')
    # all_cmds.extend('obj_mainoperation.create_rd_vd_r_3diskful')
    # all_cmds.extend('obj_mainoperation.delete_r')
    # all_cmds.extend('obj_mainoperation.resource_operation_2diskful')
    # all_cmds.extend('obj_mainoperation.resource_operation_2diskful1diskless')
    # all_cmds.extend('obj_mainoperation.check_drbd')
    # all_cmds.extend('obj_mainoperation.check_error_reports')
    # all_cmds.extend('obj_mainoperation.exchange_vd_size')
    # all_cmds.extend('obj_mainoperation.rg_operation')
    # all_cmds.extend('obj_mainoperation.delete_rg')
    # all_cmds.extend('obj_mainoperation.delete_rd')
    #
    # for i in all_cmds:
    #     funct = eval(i)

if __name__ == "__main__":
    main()




