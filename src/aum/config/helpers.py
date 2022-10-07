import logging
import os
import pathlib


def log_depends_bool(info: str, value, level=logging.INFO) -> None:
    """根据bool(value)是否为True来在日志输出其值

    如果为True则输出"info：value"，否则输出"info：无"。

    :param info: 值前的提示
    :param value: 值
    :param level: 日志级别
    """
    if value:
        logging.log(level, f'{info}：{value}')
    else:
        logging.log(level, f'{info}：无')


class EnvValue:
    def __init__(self, env_var: str, default=None):
        self._env_var = env_var  # 环境变量名
        self._env_value = os.environ.get(env_var, default)  # 环境变量值

    def __str__(self):
        return self._env_value

    def raw(self):
        """环境变量的原始值，不做任何处理"""
        return self._env_value

    def to_str(self) -> str:
        """将环境变量解析为字符串

        :return: 字符串
        :raise ValueError: 当环境变量值为None时
        """
        self._check_none('字符串')
        return self._env_value

    def to_path(self, warn_if_not_exists: bool = True) -> pathlib.Path:
        """将环境变量解析为路径

        :param warn_if_not_exists: 如果检查路径不存在则发出警告
        :return: 对象化的路径
        :raise ValueError: 当环境变量值为None时
        """
        self._check_none('路径')

        p = pathlib.Path(self._env_value)
        if warn_if_not_exists and not p.exists():
            logging.warning(f'路径"{p}"不存在，可能引发异常！')
        return p

    def to_str_set(self, sep: str = ';', discard_empty: bool = True) -> set[str]:
        """解析字符串表示的集合

        :param sep: 分隔符
        :param discard_empty: 是否忽略集合内的空字符串
        :return: 解析后的字符串set
        :raise ValueError: 当环境变量值为None时
        """
        self._check_none('字符串集合')

        str_list = self._env_value.split(sep)
        str_set = set(str_list)
        if discard_empty:
            str_set.discard('')
        return str_set

    def _check_none(self, target_name: str) -> None:
        """检查该环境变量是否为None，若是则报错

        :param target_name: 日志中对改环境变量的称呼
        :raise ValueError: 当环境变量值为None时
        """
        if self._env_value is None:
            logging.error(f'环境变量"{self._env_var}"未设置，无法解析为{target_name}！')
            raise ValueError(f'Value of env "{self._env_var}" is None.')
