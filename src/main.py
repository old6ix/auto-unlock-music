import logging

from aum.config import ConfigFactory
from aum.driver import WebDriverFactory, SeleniumHub
from aum.unlocker import MusicUnlocker


def main():
    config = ConfigFactory().create()

    sel_hub = SeleniumHub(config.sel_hub_url, config.download_dir)
    sel_driver = WebDriverFactory(sel_hub, headless=False).create()

    # TODO 筛选出加密音乐

    music_unlocker = MusicUnlocker(
        sel_driver,
        unlock_music_url=config.unlock_music_server,
        music_dir=config.music_dir,
        unlocked_suffixes=config.unlocked_suffixes
    )
    # music_unlocker.unlock_files()

    # TODO 删除原加密音乐

    # TODO 删除无用文件名子串


if __name__ == '__main__':
    main()
