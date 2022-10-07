from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.file_detector import LocalFileDetector


class WebDriverFactory:
    hub_url: str
    headless: bool

    def __init__(self, hub_url: str, headless: bool = True):
        """
        :param hub_url: Selenium Hub地址
        :param headless: 是否以无头模式启动
        """
        self.hub_url = hub_url
        self.headless = headless

    def _generate_opts(self) -> webdriver.FirefoxOptions:
        """根据成员变量生成Firefox配置

        :return: Firefox配置
        """
        opts = webdriver.FirefoxOptions()
        opts.headless = self.headless
        return opts

    def create(self) -> WebDriver:
        """创建Firefox WebDriver"""
        _driver = webdriver.Remote(
            command_executor=self.hub_url,
            options=self._generate_opts()
        )

        # 允许向Web App上传文件
        _driver.file_detector = LocalFileDetector()

        return _driver
