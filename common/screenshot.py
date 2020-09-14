import os
import time
from common.filepath import SCREENSHOT_DIR
from common.logger import LogGen
logger=LogGen("GetScreenShot").logger
class GetScreenShot:
    def __init__(self,driver):
        self.driver=driver
        self.type=".png"
    def save_name(self,name):
        day = time.strftime("%Y-%m-%d", time.localtime())
        timer = time.strftime("%H-%M-%S", time.localtime())
        filepath=os.path.join(SCREENSHOT_DIR,day)
        if not os.path.exists(filepath):
            try:
                os.makedirs(filepath)
            except Exception as e:
                logger.error("文件夹创建失败：{0}".format(e))
        filename=os.path.join(filepath,str(timer)+"-"+str(name)+str(self.type))
        return filename
    def save_screenshot(self,name):
        filename=self.save_name(name)
        try:
            self.driver.save_screenshot(filename)
            logger.info("截图成功：{0}".format(filename))
        except Exception as e:
            logger.error("截图失败：{0}".format(e))
        return filename
