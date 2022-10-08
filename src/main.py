import logging
import shutil

from aum.config import ConfigFactory
from aum.driver import WebDriverFactory, SeleniumHub
from aum.helpers.dir_filter import filter_dir_by_suffixes
from aum.unlocker import PatchMusicUnlocker


def unlock_all_music(config):
    # 筛选出加密音乐
    locked_music_set = set(filter_dir_by_suffixes(
        config.music_dir.iterdir(),
        config.locked_suffixes
    ))
    if not locked_music_set:  # 无加密音乐，退出
        logging.info('未找到加密音乐。')
        return

    logging.info(f'找到如下{len(locked_music_set)}首加密音乐：')
    for index, p in enumerate(locked_music_set):
        logging.info(f'{index + 1}. {p.name}')

    # 创建WebDriver
    sel_hub = SeleniumHub(config.sel_hub_url, config.download_dir)
    logging.debug('正在创建WebDriver...')
    sel_driver = WebDriverFactory(sel_hub).create()
    logging.debug('创建完成。')

    # 解密
    music_unlocker = PatchMusicUnlocker(
        sel_driver,
        unlock_music_url=config.unlock_music_server,
        music_dir=config.music_dir,
        unlocked_suffixes=config.unlocked_suffixes,
        patch_size=config.unlock_patch_size
    )
    music_unlocker.unlock_files(locked_music_set)

    # 关闭WebDriver
    logging.debug('正在关闭WebDriver...')
    sel_driver.quit()
    logging.debug('关闭完成。')

    # 删除解密前的文件
    for p in locked_music_set:
        p.unlink(missing_ok=True)


def rename_all_music(config):
    logging.info(f'正在移除文件名内的无用子串...')

    music_dir = config.music_dir
    count = 0
    for child in music_dir.iterdir():
        for substr in config.removing_substr:
            if child.stem.find(substr) != -1:
                new_name = child.stem.replace(substr, '') + child.suffix  # 从stem中移除子串，得到新文件名
                shutil.move(child, music_dir / new_name)

                count += 1
                logging.info(f'{count}. "{child.name}" -> "{new_name}"')
                break

    if count > 0:
        logging.info('移除完成。')
    else:
        logging.info('没有文件需要移除。')


def main():
    config = ConfigFactory().create()

    unlock_all_music(config)
    rename_all_music(config)


if __name__ == '__main__':
    main()
