# utils.py v1.0.2

import os
import re
import logging
from config_loader import load_config

config = load_config()

logger = logging.getLogger('utils')  # 新增 logger 对象

def sanitize_filename(filename: str) -> str:
    """处理文件名中的特殊字符"""
    filename = re.sub(r'[<>:"/\\|?*]+', '_', filename)  # 将在文件名中禁止的特殊字符替换为一个下划线
    filename = re.sub(r'[^a-zA-Z0-9_.-]+', '_', filename)  
    filename = re.sub(r'_+', '_', filename)  
    return filename

def setup_logging():
    """设置日志系统，包括文件处理器和控制台处理器"""
    # 检查并创建 log 子目录
    if not os.path.exists("log"):
        os.makedirs("log")
        logger.debug(f'Created directory: log')

    # 设置日志
    root_logger = logging.getLogger()  # 获取根记录器
    root_logger.setLevel(logging.INFO)

    # Disable the default log handlers to avoid duplication
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 定义日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # 文件处理器
    log_file_path = os.path.join("log", config["LOG_FILENAME"])
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)
    logger.addHandler(console_handler)

    logger.info("Script started.")

def create_directories():
    """检查并创建指定的子目录"""
    # 检查并创建 videos 子目录
    if not os.path.exists(config["DOWNLOAD_PATH"]):
        os.makedirs(config["DOWNLOAD_PATH"])
        logger.debug(f'Created directory: {config["DOWNLOAD_PATH"]}')