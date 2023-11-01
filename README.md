# CNN Video Timer
CNN Video Timer is a tool designed for scheduling the checking and downloading of videos from CNN, with automated link extraction, video downloading, and timed task execution, complemented by email notifications upon download completion. 

## 功能介绍
CNN Video Timer 是一个用于定时检查和下载 CNN 视频的工具。它能自动提取CNN10的英语新闻Youtube视频链接，下载视频，并且可以配置为定时执行这些任务。下载完成后，它还可以通过电子邮件发送通知。

本项目维护将关闭，届时代码将重构后转入新项目，实现更多功能。新项目链接不日将发布。

## 文件结构（按拼音排序）
- `baidu_cloud_uploader.py`: 百度云上传模块，负责将下载的视频上传到百度云
- `CHANGELOG.md`: 各文件次要版本更新记录
- `config_loader.py`: 配置加载模块，负责加载和验证环境配置
- `configenv`: 参考配置文件，需要更名并设置相应的参数
- `deploy.sh`: linux ubuntu安装脚本，用于自动部署项目
- `downloader_checker.py`: 下载检查器模块，负责检查和管理视频下载
- `link_extractor.py`: 链接提取模块，负责从网页提取视频链接
- `metadata_manager.py`: 元数据管理模块，负责管理视频的元数据
- `notifier.py`: 通知模块，负责发送下载完成的电子邮件通知
- `README.md`: 本说明
- `requirements.txt`: 本项目依赖
- `scheduler.py`: 调度器模块，负责定时执行下载任务
- `utils.py`: 实用工具模块，包含多个实用函数
- `video_downloader.py`: 视频下载器模块，负责视频的下载
- `LICENSE.md`: 许可证
- `bin/`: 存放第三方工具，如 `ffmpeg`
- `log/`: 存放日志文件
- `metadata/`: 存放下载视频的元数据信息
- `videos/`: 存放下载的视频文件

## 更新日志
请查看 `CHANGELOG.md` 文件以获取详细的更新日志。

## 依赖
- Python 3
- FFmpeg，请下载后放在本项目的bin子目录中
- 其他 Python 库：apscheduler, python-dotenv, requests, yt_dlp，具体请参考 `requirements.txt` 文件

## 如何使用
### Windows
1. 确保已安装 Python。
2. 运行 `pip install -r requirements.txt` 安装必需的 Python 包。
3. 确保 `ffmpeg.exe` 在 `bin` 子目录中，本release中未包含bin目录和对应文件，请自行下载。
4. 将configenv文件更名为config.env，并设置其中的邮箱参数配置。

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
