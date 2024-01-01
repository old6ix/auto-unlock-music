from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.file_detector import LocalFileDetector

from .hub import SeleniumHub


@dataclass(frozen=True)
class SeleniumDriver:
    driver: WebDriver
    hub: SeleniumHub  # 该WebDriver对应的Hub

    @property
    def download_dir(self):
        """下载目录"""
        return self.hub.download_dir

    @property
    def hub_url(self):
        """对应Hub的地址"""
        return self.hub.url

    def quit(self):
        return self.driver.quit()


class WebDriverFactory:
    sel_hub: SeleniumHub
    headless: bool

    def __init__(self, sel_hub: SeleniumHub, headless: bool = True):
        """
        :param sel_hub: Selenium Hub
        :param headless: 是否以无头模式启动
        """
        self.sel_hub = sel_hub
        self.headless = headless

    def _generate_opts(self) -> webdriver.FirefoxOptions:
        """根据成员变量生成Firefox配置

        :return: Firefox配置
        """
        opts = webdriver.FirefoxOptions()
        if self.headless:
            opts.add_argument('--headless')
        return opts

    def create(self) -> SeleniumDriver:
        """创建Firefox WebDriver"""
        opts = self._generate_opts()

        _driver = webdriver.Remote(
            command_executor=self.sel_hub.url,
            options=opts
        )

        # 允许向Web App上传文件
        _driver.file_detector = LocalFileDetector()

        return SeleniumDriver(
            driver=_driver,
            hub=self.sel_hub
        )
