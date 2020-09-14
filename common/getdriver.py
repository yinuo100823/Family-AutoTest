from selenium import webdriver

from common.logger import LogGen
logger=LogGen("getdriver").get()
class GetDriver:
    def __init__(self,browser_name="chrome"):
        if browser_name=="chrome":
            self.__driver=webdriver.Chrome()

        elif browser_name=="firefox":
            self.__driver=webdriver.Firefox()
        elif browser_name=="ie":
            self.__driver = webdriver.Ie()
        else:
            logger.error("the error type of browser")
    def get(self):
        return self.__driver