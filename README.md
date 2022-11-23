<div align="center">

![logo](https://user-images.githubusercontent.com/23132866/194682997-7728ac58-3dc0-4ad3-a2ae-9a316ed38be5.png)

# Auto Unlock Music

<div>
    <img alt="Python 3.9" src="https://img.shields.io/badge/Python-3.9-blue?logo=python">
    <img alt="Docker" src="https://img.shields.io/badge/-Docker-5c5c5c?logo=docker">
</div>

</div>
<br/>

基于[Unlock Music 音乐解锁](https://git.unlock-music.dev/um/web)和[Selenium](https://www.selenium.dev/)实现自动解锁音乐。

## 功能

对给定的音乐文件夹（暂不包括其中的子文件夹），进行如下操作：

### 1. 解锁音乐

自动在其中找到加密音乐文件（如.qmc0格式），将其解密并替换为常见的音频文件（如.mp3格式）。

### 2. 修改文件名

在QQ音乐中，音乐文件名通常以`歌手 - 歌曲 [mqms2].mp3`的类似形式保存。本程序可以自动地移除其中的多余字符串，转换为`歌手 - 歌曲.mp3`，保持文件名干净整洁。

## 部署

### 1. Clone仓库

### 2. 安装依赖

- docker

- docker compose插件

### 3. 配置音乐文件所有者

解锁后音乐文件所有者默认为`root:root`。可通过设置如下两个变量来指定其它用户：

| 环境变量名         | 说明        | 示例   |
|---------------|-----------|------|
| AUM_MUSIC_UID | 所有者的用户ID  | 1000 |
| AUM_MUSIC_GID | 所有者的用户组ID | 1000 |

### 4. 配置音乐目录

| 环境变量名         | 说明   | 示例                 |
|---------------|------|--------------------|
| AUM_MUSIC_DIR | 音乐目录 | /path/to/music_dir |

### 5. 设置分批解锁（可选）

如果设备性能不佳，则可能在同时解锁过多加密音乐时卡顿，分批次解锁可以大幅改善这一问题。

通过`AUM_UNLOCK_PATCH_SIZE`环境变量设置单批次的音乐个数。容器内默认为6个，可自行调整；设置为0则表示不分批。程序内默认不分批，单独运行时需要注意。

### 6. 运行

执行如下命令，运行程序。

```bash
./start.sh
```

通过Crontab等外部触发程序触发此命令，即可实现自动解锁音乐。
