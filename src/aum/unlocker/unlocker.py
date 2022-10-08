import logging
import pathlib
import shutil
import time
from typing import Iterable, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as expected_cond
from selenium.webdriver.support.wait import WebDriverWait

from aum.driver import SeleniumDriver
from aum.exceptions import PatchSizeError
from aum.helpers import iter_with_patch
from aum.helpers.dir_filter import filter_dir_by_stems, filter_dir_by_suffixes


class UnlockMusicBroker:
    """
    Unlock Music服务的代理人，根据调用操作web页面
    """

    driver: WebDriver
    wait: WebDriverWait
    download_dir: pathlib.Path  # 浏览器下载路径
    unlocked_suffixes: set[str]  # 已解锁的音频文件后缀

    locking_files: set[pathlib.Path] = set()

    __table_ele: Optional[WebElement] = None  # 页面下部的解锁预览表格的缓存

    def __init__(self, sel_driver: SeleniumDriver,
                 unlocked_suffixes: set[str],
                 wait_time: int = 10
                 ):
        """
        :param sel_driver: 已打开Unlock Music服务的SeleniumDriver
        :param unlocked_suffixes: 解锁的音频文件后缀组成的set
        :param wait_time: 寻找浏览器元素的超时时间
        """
        self.driver = sel_driver.driver
        self.wait = WebDriverWait(sel_driver.driver, timeout=wait_time)

        self.download_dir = sel_driver.download_dir
        self.unlocked_suffixes = unlocked_suffixes.copy()

    def upload(self, files: Iterable[pathlib.Path]):
        """上传待解锁的文件

        :param files: 待上传的文件路径迭代器
        """
        file_set = set(files)  # 待上传文件集合
        file_set -= self.locking_files  # 移除重复上传的音频文件

        input_field = self.wait.until(
            expected_cond.presence_of_element_located((By.CLASS_NAME, 'el-upload__input'))
        )
        filepath_str = (str(i) for i in file_set)  # 文件路径转字符串
        input_field.send_keys('\n'.join(filepath_str))
        logging.info('正在上传...')

        self.locking_files |= {i for i in file_set}

    def wait_until_unlocked(self, poll_interval: int = 1):
        """等待所有上传的文件解锁完成

        :param poll_interval: 检查解锁完成的频率，单位秒
        """
        expected_cnt = len(self.locking_files)

        finished_cnt = self._count_unlocked()
        while finished_cnt < expected_cnt:
            time.sleep(poll_interval)
            finished_cnt = self._count_unlocked()
        logging.info('上传完成。')

    def save_all(self, poll_interval: int = 1) -> set[str]:
        """保存全部解锁文件至浏览器下载目录

        :param poll_interval: 检查下载完成的频率，单位秒
        :return: 解锁后的音频文件名组成的list
        """
        # 开始下载
        download_all_btn = self.wait.until(
            expected_cond.presence_of_element_located((By.XPATH, '//span[text()="下载全部"]'))
        )
        download_all_btn.click()
        logging.info('开始下载...')

        # 选出所有下载文件预览行
        rows = self.driver.find_elements(By.CSS_SELECTOR, 'table.el-table__body .el-table__row')

        # 生成并返回所有的文件名stem
        downloading_stems = set()
        for r in rows:
            col2 = r.find_element(By.CLASS_NAME, 'el-table_1_column_2')
            col3 = r.find_element(By.CLASS_NAME, 'el-table_1_column_3')
            name = col3.text + ' - ' + col2.text
            downloading_stems.add(name)

        # 等待下载完成后返回
        unlocked_files = set()
        while len(downloading_stems) > 0:  # 当下载未完成全部时
            valid_stem_file_filter = filter_dir_by_stems(self.download_dir.iterdir(), downloading_stems)
            valid_file_filter = filter_dir_by_suffixes(valid_stem_file_filter, self.unlocked_suffixes)

            for new_unlocked_file in valid_file_filter:  # 如果本次解锁的文件出现
                unlocked_files.add(new_unlocked_file)
                downloading_stems.remove(new_unlocked_file.stem)

            file_left = len(downloading_stems)  # 剩余正在下载文件的总数
            if file_left > 0:  # 未全部下载完，等待后再检查
                logging.info(f'剩余{file_left}首...')
                time.sleep(poll_interval)
        logging.info(f'下载完成。')
        return {p.name for p in unlocked_files}

    def clear_all(self, poll_interval: int = 1):
        """清空页面中所有已解锁的文件

        :param poll_interval: 检查清理完成的频率，单位秒
        """
        clear_all_btn = self.wait.until(
            expected_cond.presence_of_element_located((By.XPATH, '//span[text()="清除全部"]'))
        )
        clear_all_btn.click()

        self.locking_files.clear()

        while self._count_unlocked() > 0:  # 等待解锁文件数归零
            time.sleep(poll_interval)

        self.__table_ele = None  # 清除缓存，以免其它模块改变页面后丢失元素

    def _count_unlocked(self) -> int:
        """计数网页中已解锁的文件格数

        :return: 网页中目前已解锁的文件个数
        """
        if self.__table_ele is None:
            self.__table_ele = self.driver.find_element(By.CSS_SELECTOR, 'table.el-table__body')  # 选中页面下部的解锁预览表格

        finished_cnt = len(self.__table_ele.find_elements(By.CLASS_NAME, 'el-icon-download'))  # 统计下载预览表格中下载按钮的个数
        return finished_cnt


class MusicUnlocker:
    _sel_driver: SeleniumDriver

    _service_url: str  # 音乐解锁服务的url
    _unlocked_suffixes: set[str]  # 解锁的音频文件后缀组成的set
    _music_dir: pathlib.Path

    def __init__(self, sel_driver: SeleniumDriver,
                 unlock_music_url: str,
                 music_dir: pathlib.Path,
                 unlocked_suffixes: set[str]
                 ):
        """
        :param sel_driver: SeleniumDriver
        :param unlock_music_url: 音乐解锁服务的url
        :param music_dir: 音乐目录
        :param unlocked_suffixes: 解锁的音频文件后缀组成的set
        """
        self._sel_driver = sel_driver
        self._service_url = unlock_music_url
        self._music_dir = music_dir
        self._unlocked_suffixes = unlocked_suffixes.copy()

    def unlock_files(self, files: Iterable[pathlib.Path]):
        self._sel_driver.driver.get(self._service_url)

        # 通过broker操作浏览器解锁音频文件
        broker = UnlockMusicBroker(self._sel_driver, self._unlocked_suffixes)
        broker.upload(files)
        broker.wait_until_unlocked()
        downloaded_filename_set = broker.save_all()
        broker.clear_all()

        # 将解锁后的音乐从浏览器下载目录移动至音乐目录
        logging.debug('将解锁后的音乐从下载目录移动至音乐目录...')
        self._move_down_to_music(downloaded_filename_set)
        logging.debug('移动完成。')

    def _move_down_to_music(self, filename_set: set[str]):
        """将浏览器下载路径的音乐移动到

        :param filename_set: 下载文件名组成的集合
        """
        for i in filename_set:
            shutil.move(self._sel_driver.download_dir / i, self._music_dir)


class PatchMusicUnlocker(MusicUnlocker):
    """
    可以分批解锁的unlocker
    """

    _patch_size: int

    def __init__(self, sel_driver: SeleniumDriver, unlock_music_url: str, music_dir: pathlib.Path,
                 unlocked_suffixes: set[str], patch_size: int = 0):
        """
        :param sel_driver: SeleniumDriver
        :param unlock_music_url: 音乐解锁服务的url
        :param music_dir: 音乐目录
        :param unlocked_suffixes: 解锁的音频文件后缀组成的set
        :param patch_size: 每批的音乐数量
        """
        super().__init__(sel_driver, unlock_music_url, music_dir, unlocked_suffixes)

        if patch_size < 0:
            logging.error(f'解锁批大小必须为非负整数（设置值：{patch_size}）！')
            raise PatchSizeError(patch_size)
        self._patch_size = patch_size

    def unlock_files(self, files: Iterable[pathlib.Path]):
        for path_patch in iter_with_patch(files, self._patch_size):
            super().unlock_files(files=path_patch)
