# CNN10 Video Downloader

这是一个自动下载CNN10视频的脚本，它使用`yt-dlp`来实现下载功能，并确保视频的标题得到适当的清洗以保存到指定的目录。此外，我们也增加了对错误的详细日志记录和错误通知功能。

## 文件结构

- `video_downloader.py`: 主下载脚本，版本1.6.1
- `config.env`: 环境参数，版本1.3.0
- `config_loader.py`: 配置加载器，版本 v1.2.2
- `notifier.py`: 通知器，用于在出现错误时发送电子邮件，版本 v1.1.1
- `downloader_checker.py`: 下载检查器，用于检查视频是否应该被下载，版本 v2.1.3
- `link_extractor.py`: 用于从指定页面提取视频链接的脚本，版本 v1.0.1
- `metadata_manager.py`: 管理视频元数据的类，版本 v1.0.1
- `utils.py`: 包含多个实用函数的模块，版本 v1.1.0

## 更新日志

### video_downloader.py
- **v1.6.1**
  - 引入了`LinkExtractor`类来专门处理链接的提取工作。
  - 新增了`schedule_runner`函数，支持根据设定的时间自动运行下载任务。
  - 日志记录逻辑得到了进一步优化，以更方便地捕获和查看关键信息。
  - 整体代码结构进行了优化，提高了代码的可读性和可维护性。

- **v1.6.0**
  - 重新组织了错误处理逻辑，使其更具有针对性，可以捕获网络超时、连接失败等具体错误。
  - 加入了`logger`对象，对于关键的信息和错误进行了日志记录。
  - 在`extract_video_links_from_page`中添加了更细致的错误处理。
  - `DownloaderManager`类被引入，用于管理视频的下载和检查。

- **v1.5.3**
  - 重构了`sanitize_filename`函数，确保对所有特殊字符进行了处理。
  - `MetadataManager`类被引入，提供了更方便的方式来存储和管理视频元数据。
  - 对视频信息进行的检查被加强，确保只下载那些还没有被下载的视频。
  - 在下载每一个视频后，都会存储该视频的元数据。

- **v1.5.2**
  - 重构了代码，将`create_directories`, `setup_logging`, `sanitize_filename`, `extract_video_links_from_page`等函数剥离到`utils.py`。
  - 其他一些小的改进和优化。

### config.env
- **v1.3.0**
  - 在所有环境变量参数中添加了对应的中文解释。

### config_loader.py
- **v1.2.2**
  - 添加了日志配置，确保与其他日志文件保持一致。
  - 修正了配置键名的大小写不一致问题。

### notifier.py
- **v1.1.1**
  - 修复了电子邮件格式问题。
  - 添加了更多的日志记录。

### downloader_checker.py
- **v2.1.3**
  - 引入了DownloaderManager类，用于管理视频的下载和检查。

### link_extractor.py
- **v1.0.1**
  - 添加了logger对象和对`extract_video_links_from_page`函数的错误处理。

### metadata_manager.py
- **v1.0.1**
  - 初始版本，用于管理视频的元数据。

### utils.py
- **v1.1.0**
  - 添加了多个实用函数，如`create_directories`, `setup_logging`, `sanitize_filename`。

## 如何使用

1. 在同一目录下放置所有的`.py`文件和`config.env`文件。
2. 在`config.env`中设置相关配置。
3. 运行`video_downloader.py`以开始下载。

请确保已经安装了所有必需的Python包，可以使用`pip install -r requirements.txt`来安装。
