import pathlib
from typing import Iterable


def filter_dir_by_suffixes(dir_generator: Iterable[pathlib.Path],
                           suffixes: set[str]
                           ) -> Iterable[pathlib.Path]:
    """根据文件名后缀过滤路径Iterable

    :param dir_generator: 被过滤的Iterable
    :param suffixes: 滤出的后缀集合
    :return: 过滤出相同后缀文件的filter
    """
    _suffixes = suffixes.copy()
    return filter(lambda p: p.suffix in _suffixes, dir_generator)


def filter_dir_by_stems(dir_generator: Iterable[pathlib.Path],
                        stems: set[str]
                        ) -> Iterable[pathlib.Path]:
    """根据文件名stem过滤路径Iterable

    :param dir_generator: 被过滤的Iterable
    :param stems: 滤出的stem集合
    :return: 过滤出相同stem文件的filter
    """
    _stems = stems.copy()
    return filter(lambda p: p.stem in _stems, dir_generator)
