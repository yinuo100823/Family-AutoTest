import unittest
from common.filereader import Config
from common.getdriver import GetDriver
from common.screenshot import GetScreenShot
class MyUnitTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.url = Config().get("baseinfo", "url")
		cls.driver = GetDriver().get()
		cls.driver.implicitly_wait(15)
		cls.driver.maximize_window()
		cls.driver.get(cls.url)
		cls.shot = GetScreenShot(cls.driver)

	@classmethod
	def tearDownClass(cls):

		cls.driver.quit()
