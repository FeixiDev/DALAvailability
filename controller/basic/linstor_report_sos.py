import sys
import re
from base import BaseClass
from utils import utils


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


    def sos_(self):
        utils.exec_cmd(f"linstor sos-report download --since 3days",self.obj_list[0])



def main():
    Test = MainOperation()
    Test.sos_()


if __name__ == "__main__":
    main()