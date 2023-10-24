
# CNN Video Timer

## 功能介绍
CNN Video Timer 是一个用于定时检查和下载 CNN 视频的工具。

## 文件结构
- `CHANGELOG.md`: 各文件次要版本更新记录
- `config_loader.py`: 配置加载模块
- `configenv`: 参考配置文件，改名后设置自己邮箱设置
- `deploy.sh`: linux ubuntu安装脚本
- `downloader_checker.py`: 下载检查器模块
- `link_extractor.py`: 链接提取模块
- `metadata_manager.py`: 元数据管理模块
- `notifier.py`: 通知模块
- `README.md`: 本说明
- `requirements.txt`: 本项目依赖
- `scheduler.py`: 调度器模块
- `utils.py`: 实用工具模块
- `video_downloader.py`: 视频下载器模块

## 更新日志
请查看 `CHANGELOG.md` 文件以获取详细的更新日志。

## 依赖
- Python 3
- 其他 Python 库：请参考 `requirements.txt` 文件

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

## 贡献
如有任何问题或建议，或想要参与项目贡献，可以通过邮件方式联系我们，或在项目中提出 Issue 或 Pull Request。

## 许可证
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 风险提示
使用此工具时，请遵守相关法律法规，并尊重版权。

## 联系信息
如有任何问题或建议，请发邮件：admin@zhurong.link
