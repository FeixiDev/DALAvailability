import exec_command
import time
import utils
import resources_operator
import re


class SinglePrimary(object):
    """
    Single Primary test
    """

    def __int__(self):
        self.controller_node = exec_command.SSHconn(host='')
        self.satellite_node01 = exec_command.SSHconn(host='')
        self.satellite_node02 = exec_command.SSHconn(host='')
        self.cmd_status = resources_operator.DRBD().drbdadm_status()
        self.cmd_primary = resources_operator.DRBD().drbdadm_secondary()
        self.cmd_secondary = resources_operator.DRBD().drbdadm_secondary()
        self.cmd_rl = resources_operator.Linstor().check_resource()

    def diskful_primary(self):

        exec_command.SSHconn().exec_cmd(self.cmd_primary, self.controller_node)

        node01_result = exec_command.SSHconn().exec_cmd(self.cmd_primary, self.satellite_node01)
        nodeo1_command = re.findall('Command\s*(.*)', node01_result)
        if nodeo1_command:
            print(nodeo1_command)

        exec_command.SSHconn().exec_cmd(self.cmd_primary, self.satellite_node02)
        node02_result = exec_command.SSHconn().exec_cmd(self.cmd_primary, self.satellite_node02)
        nodeo2_command = re.findall('Command\s*(.*)', node02_result)
        if nodeo1_command:
            print(nodeo2_command)

        exec_command.SSHconn().exec_cmd(self.cmd_status, self.controller_node)
        time.sleep(2)
        exec_command.SSHconn().exec_cmd(self.cmd_rl, self.controller_node)

        exec_command.SSHconn().exec_cmd(self.cmd_status, self.satellite_node01)
        time.sleep(2)
        exec_command.SSHconn().exec_cmd(self.cmd_rl, self.satellite_node01)

        exec_command.SSHconn().exec_cmd(self.cmd_status, self.satellite_node02)
        time.sleep(2)
        exec_command.SSHconn().exec_cmd(self.cmd_rl, self.satellite_node02)

    def diskless_primary(self):
        exec_command.SSHconn().exec_cmd(self.cmd_secondary, self.controller_node)
        exec_command.SSHconn().exec_cmd(self.cmd_primary, self.satellite_node02)
        node01_result = exec_command.SSHconn().exec_cmd(self.cmd_primary, self.satellite_node01)
        nodeo1_command = re.findall('Command\s*(.*)', node01_result)
        if nodeo1_command:
            print(nodeo1_command)

        exec_command.SSHconn().exec_cmd(self.cmd_primary, self.controller_node)
        node_result = exec_command.SSHconn().exec_cmd(self.cmd_primary, self.satellite_node02)
        node_command = re.findall('Command\s*(.*)', node_result)
        if nodeo1_command:
            print(node_command)

        exec_command.SSHconn().exec_cmd(self.cmd_status, self.controller_node)
        time.sleep(2)
        exec_command.SSHconn().exec_cmd(self.cmd_rl, self.controller_node)

        exec_command.SSHconn().exec_cmd(self.cmd_status, self.satellite_node01)
        time.sleep(2)
        exec_command.SSHconn().exec_cmd(self.cmd_rl, self.satellite_node01)

        exec_command.SSHconn().exec_cmd(self.cmd_status, self.satellite_node02)
        time.sleep(2)
        exec_command.SSHconn().exec_cmd(self.cmd_rl, self.satellite_node02)


class AutomaticPromotion(object):
    """
     Automatic Promotion test
    """

    def __int__(self):
        self.controller_node = exec_command.SSHconn(host='')
        self.satellite_node01 = exec_command.SSHconn(host='')
        self.satellite_node02 = exec_command.SSHconn(host='')
        self.mkfs_cmd = f'mkfs.ext4 /dev/drbd1001'
        self.mount_cmd = f'mount /dev/drbd1001 /mnt'
        self.umount_cmd = 'umount -v /dev/drbd1001'
        self.cmd_status = resources_operator.DRBD().drbdadm_status()
        self.dd_cmd = utils.RWData().dd_write(device_name='')
        self.killdd_cmd = utils.RWData().kill_dd(dd_pid='')

    def diskful_mount(self):
        exec_command.SSHconn().exec_cmd(self.mount_cmd, self.controller_node)
        node_result = exec_command.SSHconn().exec_cmd(self.cmd_status, self.controller_node)

        exec_command.SSHconn().exec_cmd(self.umount_cmd, self.controller_node)

    def diskless_mount(self):
        exec_command.SSHconn().exec_cmd(self.mount_cmd, self.satellite_node02)
        node02_result = exec_command.SSHconn().exec_cmd(self.cmd_status, self.satellite_node02)

        exec_command.SSHconn().exec_cmd(self.umount_cmd, self.satellite_node02)

    def diskful_dd(self):
        exec_command.SSHconn().exec_cmd(self.dd_cmd, self.controller_node)
        node_result = exec_command.SSHconn().exec_cmd(self.cmd_status, self.controller_node)

        exec_command.SSHconn().exec_cmd(self.killdd_cmd, self.controller_node)

    def diskless_dd(self):
        exec_command.SSHconn().exec_cmd(self.dd_cmd, self.satellite_node02)
        node02_result = exec_command.SSHconn().exec_cmd(self.cmd_status, self.satellite_node02)

        exec_command.SSHconn().exec_cmd(self.killdd_cmd, self.satellite_node02)


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


class DiscardSupport(object):
    """
      LTrim/Discard support (diskless + diskful)
     """

    def __int__(self):
        self.controller_node = exec_command.SSHconn(host='')
        self.satellite_node01 = exec_command.SSHconn(host='')
        self.satellite_node02 = exec_command.SSHconn(host='')
        self.cat_cmd = f'cat /sys/block/drbd1000/queue/discard_max_bytes'

    def discard_support(self):
        node_resutl = exec_command.SSHconn().exec_cmd(self.cat_cmd, self.controller_node)
        node01_resutl = exec_command.SSHconn().exec_cmd(self.cat_cmd, self.satellite_node01)
        node02_resutl = exec_command.SSHconn().exec_cmd(self.cat_cmd, self.satellite_node02)


class LinstorEviction(object):
    """
    LINSTOR eviction test
    """

    def __int__(self, name):
        self.controller_node = exec_command.SSHconn(host='')
        self.satellite_node01 = exec_command.SSHconn(host='')
        self.satellite_node02 = exec_command.SSHconn(host='')
        self.rl_cmd = resources_operator.Linstor().check_resource()
        self.nl_cmd = resources_operator.Linstor().check_node()
        self.spl_cmd = resources_operator.Linstor().check_sp()
        self.recover_cmd = f'instor node restore {name}'
        self.restart_cmd = f'systemctl restart linstor-satellite'
        self.sp_cmd = 'linstor controller sp DrbdOptions/AutoEvictAllowEviction false'

    def open_eviction(self):
        exec_command.SSHconn().exec_cmd(self.nl_cmd, self.satellite_node01)
        exec_command.SSHconn().exec_cmd(self.spl_cmd, self.satellite_node01)
        exec_command.SSHconn().exec_cmd(self.rl_cmd, self.satellite_node01)

        if self.satellite_node02 is False:
            try:
                exec_command.SSHconn().exec_cmd(self.nl_cmd, self.satellite_node01)
                exec_command.SSHconn().exec_cmd(self.rl_cmd, self.satellite_node01)
                time.sleep(3600)
                exec_command.SSHconn().exec_cmd(self.nl_cmd, self.satellite_node01)
                exec_command.SSHconn().exec_cmd(self.rl_cmd, self.satellite_node01)
            except Exception as e:
                print('node2 is alive')
        if self.satellite_node02 is True:
            try:
                exec_command.SSHconn().exec_cmd(self.nl_cmd, self.satellite_node01)
                exec_command.SSHconn().exec_cmd(self.rl_cmd, self.satellite_node01)
            except Exception as e:
                print('node2 is closed')

        exec_command.SSHconn().exec_cmd(self.recover_cmd, self.satellite_node01)
        exec_command.SSHconn().exec_cmd(self.nl_cmd, self.satellite_node01)
        exec_command.SSHconn().exec_cmd(self.rl_cmd, self.satellite_node01)

        exec_command.SSHconn().exec_cmd(self.restart_cmd, self.satellite_node02)
        time.sleep(10)
        exec_command.SSHconn().exec_cmd(self.nl_cmd, self.satellite_node01)
        exec_command.SSHconn().exec_cmd(self.rl_cmd, self.satellite_node01)

    def shut_eviction(self):
        exec_command.SSHconn.exec_cmd(self.sp_cmd, self.satellite_node02)

        exec_command.SSHconn().exec_cmd(self.nl_cmd, self.satellite_node01)
        exec_command.SSHconn().exec_cmd(self.spl_cmd, self.satellite_node01)
        exec_command.SSHconn().exec_cmd(self.rl_cmd, self.satellite_node01)

        if self.satellite_node02 is False:
            try:
                exec_command.SSHconn().exec_cmd(self.nl_cmd, self.satellite_node01)
                exec_command.SSHconn().exec_cmd(self.rl_cmd, self.satellite_node01)
                time.sleep(3600)
                exec_command.SSHconn().exec_cmd(self.nl_cmd, self.satellite_node01)
                exec_command.SSHconn().exec_cmd(self.rl_cmd, self.satellite_node01)
            except Exception as e:
                print('node2 is alive')
        if self.satellite_node02 is True:
            try:
                exec_command.SSHconn().exec_cmd(self.nl_cmd, self.satellite_node01)
                exec_command.SSHconn().exec_cmd(self.rl_cmd, self.satellite_node01)
            except Exception as e:
                print('node2 is closed')

        exec_command.SSHconn().exec_cmd(self.recover_cmd, self.satellite_node01)
        exec_command.SSHconn().exec_cmd(self.nl_cmd, self.satellite_node01)
        exec_command.SSHconn().exec_cmd(self.rl_cmd, self.satellite_node01)

        exec_command.SSHconn().exec_cmd(self.restart_cmd, self.satellite_node02)
        time.sleep(10)
        exec_command.SSHconn().exec_cmd(self.nl_cmd, self.satellite_node01)
        exec_command.SSHconn().exec_cmd(self.rl_cmd, self.satellite_node01)
