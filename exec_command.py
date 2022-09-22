import paramiko
import subprocess


class SSHconn(object):
    def __init__(self, host, port=22, username="root", password=None, timeout=8):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self.timeout = timeout
        self.SSHConnection = None
        self.ssh_conn()

    def ssh_conn(self):
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(host=self._host,
                         username=self._username,
                         port=self._port,
                         password=self._password,
                         timeout=self.timeout,
                         look_for_keys=False,
                         allow_agent=False)
            self.SSHConnection = conn
        except paramiko.AuthenticationException:
            print(f" Error SSH connection message of {self._host}")
        except Exception as e:
            print(f" Failed to connect {self._host}")

    def exec_cmd(self, command):
        if self.SSHConnection:
            stdin, stdout, stderr = self.SSHConnection.exec_command(command)
            result = stdout.read()
            if result is not None:
                return result

            err = stderr.read()
            if err is not None:
                return err

    def download(self, local, remote):
        try:
            sftp_file = paramiko.SFTPClient.from_transport(self.transport)
            download_file = sftp_file.get(remotepath=remote, localpath=local)
            return download_file
        except Exception as e:
            return False

    def upload(self, local, remote):
        try:
            sftp_file = paramiko.SFTPClient.from_transport(self.transport)
            upload_file = sftp_file.put(remotepath=remote, localpath=local)
            return upload_file
        except Exception as e:
            return False


class LocalProcess(object):
    def exec_cmd(command):
        sub_conn = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if sub_conn.returcode == 0:
            result = sub_conn.stdout
            return result
        else:
            print(f"Can't to execute command: {command}")
            err = sub_conn.stderr
            print(f"Error message:{err}")
            return False
