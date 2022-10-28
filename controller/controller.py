import exec_command
import time
import utils
import resources_operator
import re
import config_file
import network_operator


class SinglePrimary(object):
    """
    Single Primary test
    """

    def __int__(self):
        self.yaml_file = config_file.ConfFile('../config.yaml')
        self.yaml_info_list = self.yaml_file.read_yaml()
        self.controller_node = exec_command.SSHconn(host=self.yaml_info_list['node'][0]['ip']
                                       ,username=self.yaml_info_list['node'][0]['username']
                                       ,password=self.yaml_info_list['node'][0]['password'])
        self.satellite_node01 = exec_command.SSHconn(host=self.yaml_info_list['node'][1]['ip']
                                       ,username=self.yaml_info_list['node'][1]['username']
                                       ,password=self.yaml_info_list['node'][1]['password'])
        self.satellite_node02 = exec_command.SSHconn(host=self.yaml_info_list['node'][2]['ip']
                                       ,username=self.yaml_info_list['node'][2]['username']
                                       ,password=self.yaml_info_list['node'][2]['password'])
        self.cmd_status = resources_operator.DRBD().drbdadm_status()
        self.cmd_primary = resources_operator.DRBD().drbdadm_secondary()
        self.cmd_secondary = resources_operator.DRBD().drbdadm_secondary()
        self.cmd_rl = resources_operator.Linstor().check_resource()
        self.exec_cmd = exec_command.SSHconn().exec_cmd()

    def diskful_primary(self):

        self.exec_cmd(self.cmd_primary, self.controller_node)

        node01_result = self.exec_cmd(self.cmd_primary, self.satellite_node01)
        nodeo1_command = re.findall('Command\s*(.*)', node01_result)
        if nodeo1_command:
            print(nodeo1_command)

        self.exec_cmd(self.cmd_primary, self.satellite_node02)
        node02_result = self.exec_cmd(self.cmd_primary, self.satellite_node02)
        nodeo2_command = re.findall('Command\s*(.*)', node02_result)
        if nodeo1_command:
            print(nodeo2_command)

        self.exec_cmd(self.cmd_status, self.controller_node)
        time.sleep(2)
        self.exec_cmd(self.cmd_rl, self.controller_node)

        self.exec_cmd(self.cmd_status, self.satellite_node01)
        time.sleep(2)
        self.exec_cmd(self.cmd_rl, self.satellite_node01)

        self.exec_cmd(self.cmd_status, self.satellite_node02)
        time.sleep(2)
        self.exec_cmd(self.cmd_rl, self.satellite_node02)


    def diskless_primary(self):
        self.exec_cmd(self.cmd_secondary, self.controller_node)
        self.exec_cmd(self.cmd_primary, self.satellite_node02)
        node01_result = self.exec_cmd(self.cmd_primary, self.satellite_node01)
        nodeo1_command = re.findall('Command\s*(.*)', node01_result)
        if nodeo1_command:
            print(nodeo1_command)

        self.exec_cmd(self.cmd_primary, self.controller_node)
        node_result = self.exec_cmd(self.cmd_primary, self.satellite_node02)
        node_command = re.findall('Command\s*(.*)', node_result)
        if nodeo1_command:
            print(node_command)

        self.exec_cmd(self.cmd_status, self.controller_node)
        time.sleep(2)
        self.exec_cmd(self.cmd_rl, self.controller_node)

        self.exec_cmd(self.cmd_status, self.satellite_node01)
        time.sleep(2)
        self.exec_cmd(self.cmd_rl, self.satellite_node01)

        self.exec_cmd(self.cmd_status, self.satellite_node02)
        time.sleep(2)
        self.exec_cmd(self.cmd_rl, self.satellite_node02)

    def main(self):
        SinglePrimary().diskful_primary()
        SinglePrimary().diskless_primary()


class AutomaticPromotion(object):
    """
     Automatic Promotion test
    """

    def __int__(self,drbd_route):
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
        self.mkfs_cmd = resources_operator.DISK().mkfs_disk(drbd_route)
        self.mount_cmd = resources_operator.DISK().mount_disk(drbd_route)
        self.umount_cmd = resources_operator.DISK().umount_disk(drbd_route)
        self.cmd_status = resources_operator.DRBD().drbdadm_status()
        self.dd_cmd = utils.RWData().dd_write(device_name='')
        self.killdd_cmd = utils.RWData().kill_dd(dd_pid='')
        self.exec_cmd = exec_command.SSHconn().exec_cmd()

    def diskful_mount(self):
        self.exec_cmd(self.mount_cmd, self.controller_node)
        node_result = self.exec_cmd(self.cmd_status, self.controller_node)

        self.exec_cmd(self.umount_cmd, self.controller_node)

    def diskless_mount(self):
        self.exec_cmd(self.mount_cmd, self.satellite_node02)
        node02_result = self.exec_cmd(self.cmd_status, self.satellite_node02)

        self.exec_cmd(self.umount_cmd, self.satellite_node02)

    def diskful_dd(self):
        self.exec_cmd(self.dd_cmd, self.controller_node)
        node_result = self.exec_cmd(self.cmd_status, self.controller_node)

        self.exec_cmd(self.killdd_cmd, self.controller_node)

    def diskless_dd(self):
        self.exec_cmd(self.dd_cmd, self.satellite_node02)
        node02_result = exec_command.SSHconn().exec_cmd(self.cmd_status, self.satellite_node02)

        self.exec_cmd(self.killdd_cmd, self.satellite_node02)
    def main(self):
        test_automatic_promotion = AutomaticPromotion()
        test_automatic_promotion.diskful_mount()
        test_automatic_promotion.diskless_mount()
        test_automatic_promotion.diskful_dd()
        test_automatic_promotion.diskless_dd()

class LinstorCommandResponse(object):
    """
     LINSTOR响应测试
    """

    def response_test(self):
        cmd = f'time linstor n l'
        result = exec_command.SSHconn().exec_cmd(cmd)
        real = str(re.findall('real(.*?)user', result)).strip()
        user = str(re.findall('user(.*?)sys', result)).strip()
        sys = str(re.findall('sys(.*?)', result)).strip()

        list_data = [['real', real],
                     ['user', user],
                     ['sys', sys]
                     ]
        utils.Table().add_data(list_data)
        utils.Table().print_table()

    def main(self):
        LinstorCommandResponse().response_test()


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
        self.cat_cmd = f'cat /sys/block/drbd1000/queue/discard_max_bytes'
        self.exec_cmd = exec_command.SSHconn().exec_cmd()

    def discard_support(self):
        node_resutl = self.exec_cmd(self.cat_cmd, self.controller_node)
        node01_resutl = self.exec_cmd(self.cat_cmd, self.satellite_node01)
        node02_resutl = self.exec_cmd(self.cat_cmd, self.satellite_node02)

    def main(self):
        DiscardSupport().discard_support()


class LinstorEviction(object):
    """
    LINSTOR eviction test
    """

    def __int__(self, name):
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
        self.rl_cmd = resources_operator.Linstor().check_resource()
        self.nl_cmd = resources_operator.Linstor().check_node()
        self.spl_cmd = resources_operator.Linstor().check_sp()
        self.recover_cmd = f'instor node restore {name}'
        self.restart_cmd = f'systemctl restart linstor-satellite'
        self.sp_cmd = 'linstor controller sp DrbdOptions/AutoEvictAllowEviction false'
        self.exec_cmd = exec_command.SSHconn().exec_cmd()

    def open_eviction(self):
        self.exec_cmd(self.nl_cmd, self.satellite_node01)
        self.exec_cmd(self.spl_cmd, self.satellite_node01)
        self.exec_cmd(self.rl_cmd, self.satellite_node01)

        if self.satellite_node02 is False:
            try:
                self.exec_cmd(self.nl_cmd, self.satellite_node01)
                self.exec_cmd(self.rl_cmd, self.satellite_node01)
                time.sleep(3600)
                self.exec_cmd(self.nl_cmd, self.satellite_node01)
                self.exec_cmd(self.rl_cmd, self.satellite_node01)
            except Exception as e:
                print('node2 is alive')
        if self.satellite_node02 is True:
            try:
                self.exec_cmd(self.nl_cmd, self.satellite_node01)
                self.exec_cmd(self.rl_cmd, self.satellite_node01)
            except Exception as e:
                print('node2 is closed')

        self.exec_cmd(self.recover_cmd, self.satellite_node01)
        self.exec_cmd(self.nl_cmd, self.satellite_node01)
        self.exec_cmd(self.rl_cmd, self.satellite_node01)

        self.exec_cmd(self.restart_cmd, self.satellite_node02)
        time.sleep(10)
        self.exec_cmd(self.nl_cmd, self.satellite_node01)
        self.exec_cmd(self.rl_cmd, self.satellite_node01)

    def shut_eviction(self):
        self.exec_cmd(self.sp_cmd, self.satellite_node02)

        self.exec_cmd(self.nl_cmd, self.satellite_node01)
        self.exec_cmd(self.spl_cmd, self.satellite_node01)
        self.exec_cmd(self.rl_cmd, self.satellite_node01)

        if self.satellite_node02 is False:
            try:
                self.exec_cmd(self.nl_cmd, self.satellite_node01)
                self.exec_cmd(self.rl_cmd, self.satellite_node01)
                time.sleep(3600)
                self.exec_cmd(self.nl_cmd, self.satellite_node01)
                self.exec_cmd(self.rl_cmd, self.satellite_node01)
            except Exception as e:
                print('node2 is alive')
        if self.satellite_node02 is True:
            try:
                self.exec_cmd(self.nl_cmd, self.satellite_node01)
                self.exec_cmd(self.rl_cmd, self.satellite_node01)
            except Exception as e:
                print('node2 is closed')

        self.exec_cmd(self.recover_cmd, self.satellite_node01)
        self.exec_cmd(self.nl_cmd, self.satellite_node01)
        self.exec_cmd(self.rl_cmd, self.satellite_node01)

        self.exec_cmd(self.restart_cmd, self.satellite_node02)
        time.sleep(10)
        self.exec_cmd(self.nl_cmd, self.satellite_node01)
        self.exec_cmd(self.rl_cmd, self.satellite_node01)

    def main(self):
        LinstorEviction().open_eviction()
        LinstorEviction().shut_eviction()

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
        self.status_cmd = resources_operator.DRBD().drbdadm_status()
        self.down_cmd = network_operator.DeviceService().down_device(dev)
        self.up_cmd = network_operator.DeviceService().up_device(dev)
        self.exec_cmd = exec_command.SSHconn().exec_cmd()


    def quorum_a_loss(self):
        self.exec_cmd(self.down_cmd,self.controller_node)
        node_resutl = self.exec_cmd(self.status_cmd, self.controller_node)
        node01_resutl = self.exec_cmd(self.status_cmd, self.satellite_node01)
        node02_resutl = self.exec_cmd(self.status_cmd, self.satellite_node02)
        quorum_node = re.findall('quorum:([\W]*)',str(node_resutl))
        quorum_node01 = re.findall('quorum:([\W]*)', str(node01_resutl))
        quorum_node02 = re.findall('quorum:([\W]*)', str(node02_resutl))
        if quorum_node == 'quorum:no' and quorum_node01 != 'quorum:no' and quorum_node02 != 'quorum:no':
            print('test pass')
            self.exec_cmd(self.up_cmd, self.controller_node)

    def quorum_c_loss(self):
        self.exec_cmd(self.down_cmd, self.satellite_node02)
        node_resutl = self.exec_cmd(self.status_cmd, self.controller_node)
        node01_resutl = self.exec_cmd(self.status_cmd, self.satellite_node01)
        node02_resutl = self.exec_cmd(self.status_cmd, self.satellite_node02)
        quorum_node = re.findall('quorum:([\W]*)', str(node_resutl))
        quorum_node01 = re.findall('quorum:([\W]*)', str(node01_resutl))
        quorum_node02 = re.findall('quorum:([\W]*)', str(node02_resutl))
        if quorum_node02 == 'quorum:no' and quorum_node01 != 'quorum:no' and quorum_node != 'quorum:no':
            print('test pass')
            self.exec_cmd(self.up_cmd, self.satellite_node02)
    def quorum_ab_loss(self):
        self.exec_cmd(self.down_cmd, self.controller_node)
        self.exec_cmd(self.down_cmd, self.satellite_node01)
        node_resutl = self.exec_cmd(self.status_cmd, self.controller_node)
        node01_resutl = self.exec_cmd(self.status_cmd, self.satellite_node01)
        node02_resutl = self.exec_cmd(self.status_cmd, self.satellite_node02)
        quorum_node = re.findall('quorum:([\W]*)', str(node_resutl))
        quorum_node01 = re.findall('quorum:([\W]*)', str(node01_resutl))
        quorum_node02 = re.findall('quorum:([\W]*)', str(node02_resutl))
        if quorum_node02 == 'quorum:no' and quorum_node01 == 'quorum:no' and quorum_node == 'quorum:no':
            self.exec_cmd(self.up_cmd, self.satellite_node01)
            node_resutl = self.exec_cmd(self.status_cmd, self.controller_node)
            node01_resutl = self.exec_cmd(self.status_cmd, self.satellite_node01)
            node02_resutl = self.exec_cmd(self.status_cmd, self.satellite_node02)
            quorum_node = re.findall('quorum:([\W]*)', str(node_resutl))
            quorum_node01 = re.findall('quorum:([\W]*)', str(node01_resutl))
            quorum_node02 = re.findall('quorum:([\W]*)', str(node02_resutl))
            if quorum_node02 == 'quorum:no' and quorum_node01 == 'quorum:no' and quorum_node == 'quorum:no':
                self.exec_cmd(self.up_cmd, self.controller_node)
                node_resutl = self.exec_cmd(self.status_cmd, self.controller_node)
                node01_resutl = self.exec_cmd(self.status_cmd, self.satellite_node01)
                node02_resutl = self.exec_cmd(self.status_cmd, self.satellite_node02)
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







