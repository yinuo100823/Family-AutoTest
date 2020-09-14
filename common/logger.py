import logging
import time
import os
from common.filepath import LOG_DIR


class LogGen:
    __object = None

    def __new__(cls, *args, **kwargs):
        if cls.__object == None:
            cls.__object = object.__new__(cls)
        return cls.__object

    def __init__(self, logger, level=logging.INFO, is_consol=False):
        self.__logger = logging.getLogger(logger)
        self.__level = level
        self.__is_consol = is_consol

    def __set_log_path_name_format(self):
        filepath = os.path.join(LOG_DIR, time.strftime("%Y-%m-%d", time.localtime()))
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filename = os.path.join(filepath, "test-info.log")
        fileh = logging.FileHandler(filename, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s -- %(levelname)s -- %(name)s -- %(message)s")  # 设置日志输出格式
        self.__logger.setLevel(self.__level)
        if self.__is_consol:
            consoleh = logging.StreamHandler()
            consoleh.setFormatter(formatter)
            self.__logger.addHandler(consoleh)
        fileh.setFormatter(formatter)
        self.__logger.addHandler(fileh)

    @property
    def logger(self):
        self.__set_log_path_name_format()
        return self.__logger


if __name__ == '__main__':
    logger1 = LogGen("登录模块1", is_consol=True)
    logger1.logger.info("hello1")
    logger2 = LogGen("登录模块2", is_consol=True)
    logger2.logger.info("hello2")
