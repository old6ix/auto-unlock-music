from aum.config import ConfigFactory
from aum.driver import WebDriverFactory


def main():
    config = ConfigFactory().create()

    driver = WebDriverFactory(hub_url=config.sel_hub, headless=False).create()
    driver.get(config.unlock_music_server)


if __name__ == '__main__':
    main()
