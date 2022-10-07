import pathlib
from dataclasses import dataclass


@dataclass(frozen=True)
class SeleniumHub:
    """
    Selenium Hub节点配置
    """
    url: str  # hub url
    download_dir: pathlib.Path  # 该hub的下载目录
