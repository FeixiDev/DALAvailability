import subprocess
import sys
import paramiko
import log

def exec_cmd(cmd, conn=None):
    if conn:
        result = conn.exec_cmd(cmd)
    else:
        result = subprocess.getoutput(cmd)
    log.Log().write_to_log(cmd,result,30)
    if result:
        result = result.rstrip('\n')
    if result is False:
        sys.exit()
    return result

class SSHConn(object):

    def __init__(self, host, port=22, username=None, password=None, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._username = username
        self._password = password
        self.SSHConnection = None
        self.ssh_connect()

    def _connect(self):
        try:
            objSSHClient = paramiko.SSHClient()
            objSSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            objSSHClient.connect(self._host, port=self._port,
                                 username=self._username,
                                 password=self._password,
                                 timeout=self._timeout)
            self.SSHConnection = objSSHClient
            print(f" Success to connect {self._host}")
        except:
            print(f" Failed to connect {self._host}")

    def ssh_connect(self):
        self._connect()
        if not self.SSHConnection:
            print(f'Connect retry for {self._host}')
            self._connect()
            if not self.SSHConnection:
                sys.exit()

    def exec_cmd(self, command):
        if self.SSHConnection:
            stdin, stdout, stderr = self.SSHConnection.exec_command(command)
            data = stdout.read()
            if bool(data) is True:
                data = data.decode() if isinstance(data, bytes) else data
                return data
            err = stderr.read()
            if bool(err) is True:
                err = err.decode() if isinstance(err, bytes) else err
                return False

    def ssh_close(self):
        self.SSHConnection.close()


class RWData:
    def dd_write(self,device_name):
        cmd = f'dd if=/dev/urandom of={device_name} oflag=direct status=progress'

    def kill_dd(self,dd_pid):
        cmd = f'kill {dd_pid}'