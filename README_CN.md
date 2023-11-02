# CNN Video Timer
CNN Video Timer is a tool designed for scheduling the checking and downloading of videos from CNN, with automated link extraction, video downloading, and timed task execution, complemented by email notifications upon download completion. 

## 功能介绍
CNN Video Timer 是一个用于定时检查和下载 CNN 视频的工具。它能自动提取CNN10的英语新闻Youtube视频链接，下载视频，并且可以配置为定时执行这些任务。下载完成后，它还可以通过电子邮件发送通知。

本项目在计划重构，添加实现更多功能，新项目链接不日将发布。

## 文件结构（按拼音排序）
- `.gitignore`：排除文件包括，日志，元数据，下载视频，本地配置，密钥，临时文件等
- `baidu_cloud_uploader.py`: 百度云上传模块，负责将下载的视频上传到百度云(需设置百度API并获取授权用户的access token)
- `build.bat`：给管理员使用的打包模块，将工作目录下配置文件先移出，再使用pyinstaller打包创建2个release包，其中一个含ffmpeg.exe
- `CHANGELOG.md`: 各模块版本更新记录
- `config_loader.py`: 配置加载模块，负责加载和验证环境配置
- `configenv`: 参考配置文件，需要更名为config.env，并设置相应的参数
- `deploy.sh`: linux ubuntu一键安装脚本，用于自动部署项目
- `downloader_checker.py`: 下载检查器模块，负责检查和管理视频下载
- `install.bat`:给windows用户使用的安装脚本，下载完整版本后在windows窗口执行，会创建bin目录，并将ffmege移动到bin目录，添加系统路径
- `LICENSE.md`: MIT许可证
- `link_extractor.py`: 链接提取模块，负责从网页提取视频链接
- `metadata_manager.py`: 元数据管理模块，负责管理视频的元数据
- `notifier.py`: 通知模块，负责发送下载完成的电子邮件通知（请先在配置文件中设置用户邮箱参数）
- `README.md`: 本说明
- `requirements.txt`: 本项目依赖，apscheduler，python-dotenv，requests，yt_dlp，另外ffmpeg.exe需要提前下载在bin目录
- `scheduler.py`: 调度器模块，负责定时执行下载任务，可在配置文件中设置下载时间，单独执行时使用--test参数为立即执行
- `utils.py`: 实用工具模块，包含日志设置，目录检查创建和文件名清洗
- `video_downloader.py`: 视频下载器模块，负责视频的下载
- `bin/`: 存放第三方工具，目前为`ffmpeg.exe`，`ffprobe.exe``ffplay.exe`
- `log/`: 存放日志文件，日志文件名为video_downloader.log
- `metadata/`: 存放下载视频的元数据信息，元数据名为metadata.json
- `videos/`: 存放下载的视频文件，各日期的视频文件

## 更新日志
请查看 `CHANGELOG.md` 文件以获取详细的更新日志。

## 依赖
- Python 3
- FFmpeg，请下载ffmpeg.exe后放在本项目的bin子目录中，下载网址：https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
- 其他 Python 库：apscheduler, python-dotenv, requests, yt_dlp，具体版本号请参考 `requirements.txt` 文件

## 如何使用
### Windows
#### 方法一（推荐）
1. 直接下载：https://github.com/znhskzj/cnnvideo-timer/releases/download/v0.9.1/releaseffmpeg.zip
2. 在本地新建一个目录，将上述文件解压缩。
3. 执行install.bat脚本（windows10以上用户，如果windows10以下，需要自行安装解压缩软件并参照以下方法二）。

#### 方法二
1. 在https://github.com/znhskzj/cnnvideo-timer的仓库中，release页面下载最新版本。
2. 没有下载过ffmpeg.exe的，请下载releaseffmpeg.zip。
3. 解压至单独的工作目录，创建bin子目录，将ffmpeg.exe放入该子目录，将该目录添加到系统环境的path中。
4. 将configenv改名为config.env。
5. 执行cnn10vd.exe文件，视频文件会下载到当前目录的video子目录中。

#### 程序员同学
1. 请至https://github.com/znhskzj/cnnvideo-timer下载源码。
2. 将configenv改名为config.env后进行参数配置。
3. 各种花式使用，可以实现实时下载，计划下载，下载多个视频，更换其它新闻频道下载，更换下载文件规格，查看youtube视频元数据，上传百度云盘等功能。
4. 欢迎star、fork和pr。

### Mac 和 Linux
1. 确保已安装 Python。
2. 运行以下命令来一键自动部署项目(Ubuntu和Debian)：

   ```bash
   curl -sSL https://raw.githubusercontent.com/znhskzj/cnnvideo-timer/main/deploy.sh | bash

如果需要手工部署，请确保 deploy.sh 脚本有执行权限。可以使用如下命令进行检查和设置：
chmod +x deploy.sh

## 常见问题
- linux下的安装问题请查看FAQ.md文档。

## 贡献
如有任何问题或建议，或想要参与项目贡献，可以通过邮件方式联系我们，或在项目中提出 Issue 或 Pull Request。

## 许可证
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 风险提示
使用此工具和下载使用视频时，请遵守相关法律法规，以及视频原创者的使用条款和条件，并尊重版权。

## 联系信息
如有任何问题或建议，请发邮件：admin@zhurong.link
