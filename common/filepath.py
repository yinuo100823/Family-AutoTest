import os

"""
该类负责各文件位置的配置
"""
BASE_DIR=os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE=os.path.join(BASE_DIR,"config","config.ini")
COMMON_DIR=os.path.join(BASE_DIR,"common")
DATA_DIR=os.path.join(BASE_DIR,"data")
SCREENSHOT_DIR=os.path.join(BASE_DIR,"screenshots")
PO_DIR=os.path.join(BASE_DIR,"po")
REPORT_DIR=os.path.join(BASE_DIR,"report")
LOG_DIR=os.path.join(BASE_DIR,"log")
ELEMENT_DIR=os.path.join(BASE_DIR,"elements")