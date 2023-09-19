from .base import BaseClass
from utils import utils
import drbd_status
import linstor_node_create
import linstor_node_delete
import linstor_sp_thinlvm_create
import linstor_sp_thinlvm_increase
import linstor_sp_thinlvm_delete
import linstor_sp_lvm_create
import linstor_sp_lvm_delete
import linstor_r_create
import linstor_r_increase
import linstor_r_decrease
import linstor_r_promotion
import linstor_r_eviction
import linstor_report_error
import linstor_report_sos
import linstor_responsetime
import trim




class MainOperation(BaseClass):
    """
    前提条件：

    """
    def __init__(self):
        super().__init__()
        self.data_list = []
        self._init_datalist()


    def _init_datalist(self):
        pass

    def linstor_node_create_s(self):
        print(f"创建Combined节点{self.nodename_list[0]}")
        utils.exec_cmd(f"linstor node create {self.yaml_info_list['node'][0]['name']} {self.yaml_info_list['node'][0]['ip']} --node-type Combined",self.obj_controller)
        print(f"创建Combined节点{self.nodename_list[1]}")
        utils.exec_cmd(f"linstor node create {self.yaml_info_list['node'][1]['name']} {self.yaml_info_list['node'][1]['ip']} --node-type Combined",self.obj_satellite01)
        print(f"创建Combined节点{self.nodename_list[2]}")
        utils.exec_cmd(f"linstor node create {self.yaml_info_list['node'][2]['name']} {self.yaml_info_list['node'][2]['ip']} --node-type Combined",self.obj_satellite02)

    def linstor_r_2diskful_1diskless(self):
        print(f"在节点{self.nodename_list[0]}创建diskful资源")
        utils.exec_cmd(f"linstor r c {self.nodename_list[0]} {self.resource_name} --storage-pool {self.thick_lvm_storagepool_name}",self.obj_controller)
        print(f"在节点{self.nodename_list[1]}创建diskful资源")
        utils.exec_cmd(f"linstor r c {self.nodename_list[1]} {self.resource_name} --storage-pool {self.thick_lvm_storagepool_name}",self.obj_satellite01)
        print(f"在节点{self.nodename_list[2]}创建diskless资源")
        utils.exec_cmd(f"linstor r c {self.nodename_list[-1]} {self.resource_name} --diskless",self.obj_satellite02)


def main():
    print("------------测试开始：基础测试测试------------")
    Test = MainOperation()
    drbd_status.main()
    linstor_node_create.main()
    linstor_node_delete.main()
    Test.linstor_node_create_t()
    linstor_sp_thinlvm_create.main()
    linstor_sp_thinlvm_increase.main()
    linstor_sp_thinlvm_delete.main()
    linstor_sp_lvm_create.main()
    linstor_sp_lvm_delete.main()
    linstor_sp_lvm_create.main()
    linstor_r_create.main()
    Test.linstor_r_2diskful_1diskless()
    linstor_r_increase.main()
    linstor_r_decrease.main()
    linstor_r_promotion.main()
    linstor_r_eviction.main()
    linstor_report_error.main()
    linstor_report_sos.main()
    linstor_responsetime.main()
    trim.main()


    print("------------测试结束：基础测试测试------------")

if __name__ == "__main__":
    main()
