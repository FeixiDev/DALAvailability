from .base import BaseClass
from utils import utils


class MainOperation(BaseClass):
    def __init__(self):
        super().__init__()


    def delete_node(self):
        print(f"删除节点:{self.nodename_list[0]}")
        utils.exec_cmd(f"linstor node delete {self.yaml_info_list['node'][0]['name']}",self.obj_controller)
        print(f"删除节点:{self.nodename_list[1]}")
        utils.exec_cmd(f"linstor node delete {self.yaml_info_list['node'][1]['name']}",self.obj_satellite01)
        print(f"删除节点:{self.nodename_list[2]}")
        utils.exec_cmd(f"linstor node delete {self.yaml_info_list['node'][2]['name']}",self.obj_satellite02)


def main():
    Test = MainOperation()
    print("------------测试开始：linstor节点删除------------")
    Test.delete_node()
    print("------------测试结束：linstor节点删除------------")


if __name__ == "__main__":
    main()