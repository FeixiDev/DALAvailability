import paramiko
import subprocess


class SSHconn(object):
    def __init__(self, host, port=22, username="root", password=None, timeout=8):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self.timeout = timeout
        self.sshconnection = None
        self.ssh_conn()


    def ssh_conn(self):
        """
        SSH连接
        """
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname=self._host,
                         username=self._username,
                         port=self._port,
                         password=self._password,
                         timeout=self.timeout,
                         look_for_keys=False,
                         allow_agent=False)
            self.sshconnection = conn
        except paramiko.AuthenticationException:
            print(f" Error SSH connection message of {self._host}")
        except Exception as e:
            print(f" Failed to connect {self._host}")

    def exec_cmd(self, command):
        """
        命令执行
        """
        if self.sshconnection:
            stdin, stdout, stderr = self.sshconnection.exec_command(command)
            result = stdout.read()
            result = result.decode() if isinstance(result, bytes) else result
            if result is not None:
                return {"st": True, "rt": result}

            err = stderr.read()
            if err is not None:
                return {"st": False, "rt": err}


    def download(self, local, remote):
        """
        sftp下载文件
        """
        try:
            sftp_file = paramiko.SFTPClient.from_transport(self.transport)
            download_file = sftp_file.get(remotepath=remote, localpath=local)
            return {"st": True, "rt": "File downloaded successfully"}
        except Exception as e:
            return {"st": False, "rt": e}

    def upload(self, local, remote):
        """
        sftp上传文件
        """
        try:
            sftp_file = paramiko.SFTPClient.from_transport(self.transport)
            upload_file = sftp_file.put(remotepath=remote, localpath=local)
            return {"st": True, "rt": "File uploaded successfully"}
        except Exception as e:
            return {"st": False, "rt": e}


class LocalProcess(object):
    def exec_cmd(self,command):
        """
        命令执行
        """
        sub_conn = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if sub_conn.returcode == 0:
            result = sub_conn.stdout
            return {"st": True, "rt": result}
        else:
            print(f"Can't to execute command: {command}")
            err = sub_conn.stderr
            print(f"Error message:{err}")
            return {"st": False, "rt": err}
