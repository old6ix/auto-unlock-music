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

## 部署

### 1. Clone仓库

### 2. 安装依赖

- docker

- docker compose插件

### 3. 设置环境变量

通过`AUM_MUSIC_DIR`环境变量设置音乐目录。

例如可以在项目根目录创建内容如下的`.env`文件：

```text
AUM_MUSIC_DIR=/path/to/music_dir
```

### 4. 运行

执行如下命令，运行程序。

```bash
./start.sh
```
