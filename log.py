import logging
import logging.handlers
import datetime
import sys
import socket


def get_host_ip():
    """
    查询本机ip地址
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


class Log(object):
    def __init__(self):

        now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.file_name = str(now_time) + '.log'
        self.ip = get_host_ip()


    def write_to_log(self,data1,data2,level=10):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger_format = (f"%(asctime)s - %(levelname)s - {self.ip} - {data1} - {data2}")
        fmt = logging.Formatter(logger_format)
        file_handler = logging.FileHandler(self.file_name)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
        if level == 10:
            logger.debug("this is debug")
        elif level == 20:
            logger.info("this is info")
        elif level == 30:
            logger.error("this is error")
        elif level == 40:
            logger.warning("this is warning")
        elif level == 50:
            logger.critical("this is critical")
        else:
            print('The level must be 10,20,30,40,50')
