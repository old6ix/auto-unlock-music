from typing import Iterable, Generator

from aum.exceptions import PatchSizeError


def iter_with_patch(iterator: Iterable, patch_size: int = 0) -> Generator[list, None, None]:
    """分批

    :param iterator: 被分批的迭代器
    :param patch_size: 每批元素个数，0表示不分批
    :return: 每次返回一批数据组成的list的生成器
    """
    if patch_size < 0:
        raise PatchSizeError(patch_size)
    elif patch_size == 0:
        yield list(iterator)
        return

    curr_cnt = 0  # 当前批内元素个数
    curr_patch = []  # 当前批
    for i in iterator:
        curr_patch.append(i)
        curr_cnt += 1

        if curr_cnt == patch_size:
            ret = curr_patch.copy()  # 本次将生成的对象

            # 清空当前批
            curr_cnt = 0
            curr_patch.clear()

            yield ret  # 生成

    if curr_cnt > 0:  # 如果有剩余，说明最后一批不满，生成该批次
        yield curr_patch
