import configparser
import csv
import os
import xlrd
from common.filepath import CONFIG_FILE, DATA_DIR
from common.logger import LogGen

logger = LogGen("FileReader").logger


class Config:
	# 读取配置文件
	"""
	[test]--->first
	name=zhangsna--->second
	age=18

	返回second的值
	"""

	def __init__(self):
		self.file = CONFIG_FILE
		if not os.path.exists(self.file):
			logger.error("{0}：文件未找到".format(self.file))
			raise FileNotFoundError("{0}：文件未找到".format(self.file))

	def get(self, first, second):
		cfg = configparser.ConfigParser()
		cfg.read(self.file)
		# logger.info("读取配置：{0}：{1}".format(second,cfg.get(first,second)))
		return cfg.get(first, second)


class CSVReader:
	def __init__(self, filename, title_flag=True):
		if not os.path.exists(filename):
			logger.error("{0}：文件未找到".format(filename))
			raise FileNotFoundError("{0}:文件不存在".format(filename))
		self.filename = filename
		self._data = list()
		self.csv = csv
		self.title_flag = title_flag

	"""
	return _data,一个嵌套列表,外层列表的每个元素为一行，如:
	[['selenium', 'selenium_百度搜索'], ['hello', 'hello_百度搜索']]
	"""

	@property
	def data(self):
		if not self._data:
			with open(self.filename, "r") as csvfile:
				c = self.csv.reader(csvfile)
				if self.title_flag:
					next(c)
				for irow in c:
					self._data.append(irow)
			return self._data
		logger.info("读取数据：{0}".format(self._data))
		return self._data


class ExcelReader:
	def __init__(self, filename, sheet=0, title_flag=True):
		if not os.path.exists(filename):
			logger.error("{0}：文件未找到".format(filename))
			raise FileNotFoundError("{0}文件不存在".format(filename))
		self.file = filename
		self._data = list()
		self.sheet = sheet
		self.title_flag = title_flag

	@property
	def data(self):
		if not self._data:
			workbook = xlrd.open_workbook(self.file)
			if type(self.sheet) not in [str, int]:
				logger.error("{0}:sheet的类型错误，只能传str和int".format(self.sheet))
				raise TypeError("{0}:sheet的类型错误，只能传str和int".format(self.sheet))
			elif type(self.sheet) == int:
				worksheet = workbook.sheet_by_index(self.sheet)
			else:
				worksheet = workbook.sheet_by_name(self.sheet)
			if self.title_flag:
				for irow in range(1, worksheet.nrows):
					self._data.append(worksheet.row_values(irow))
			else:
				for irow in range(worksheet.nrows):
					self._data.append(worksheet.row_values(irow))
		logger.info("读取数据：{0}".format(self._data))
		return self._data


if __name__ == '__main__':
	CReader = CSVReader(os.path.join(DATA_DIR, "register_info.csv"))
	data = CReader.data
	for list1 in data:
		print(list1)

	EReader = ExcelReader(os.path.join(DATA_DIR, "register_info.xlsx"))
	data = EReader.data
	print(data)
