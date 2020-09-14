import os
import time
from common.filepath import  REPORT_DIR
from common.logger import LogGen

logger=LogGen("GetReportPath").logger
class GetReportPath:
    def __init__(self):
        self._report_path=None
        self.day=time.strftime("%Y-%m-%d",time.localtime())
    def get_report_path(self):
        self._report_path=os.path.join(REPORT_DIR,self.day)
        if not os.path.exists(self._report_path):
            try:
                os.makedirs(self._report_path)
            except Exception as e:
                logger.error("文件夹创建失败：{0}".format(e))
    @property
    def data(self):
        self.get_report_path()
        logger.info("测试报告地址：{0}".format(self._report_path))
        return self._report_path

if __name__ == '__main__':
    grp=GetReportPath()
    print(grp.data)