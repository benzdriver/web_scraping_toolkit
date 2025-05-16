"""
日志系统模块

提供了统一的日志配置和获取功能。
"""

import os
import logging
from datetime import datetime

# 导入配置管理
from .config import get_logger_config

# 定义日志级别映射
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

# 默认日志目录
DEFAULT_LOG_DIR = "logs"
# 统一日志文件名
UNIFIED_LOG_FILE = "web_scraping_toolkit.log"

# 统一文件处理程序字典，用于共享
_file_handlers = {}

def setup_logger(
    name: str = None,
    log_dir: str = None,
    console_level: str = None,
    file_level: str = None,
    capture_warnings: bool = None,
    include_timestamp: bool = True,
    unified_log: bool = True
):
    """
    设置并配置一个日志记录器
    
    Args:
        name: 日志记录器名称，如果为None则使用根日志记录器
        log_dir: 日志文件存储目录
        console_level: 控制台日志级别
        file_level: 文件日志级别
        capture_warnings: 是否捕获Python警告并将其转换为日志
        include_timestamp: 是否在日志文件名中包含时间戳（仅当unified_log=False时有效）
        unified_log: 是否将所有日志统一输出到一个文件
        
    Returns:
        logger: 配置好的日志记录器
    """
    # 获取日志配置
    config = get_logger_config()
    
    # 使用传入的参数或配置值
    log_dir = log_dir or config.get("directory", DEFAULT_LOG_DIR)
    console_level = console_level or config.get("level", "info")
    file_level = file_level or config.get("level", "debug")
    
    if capture_warnings is None:
        capture_warnings = config.get("capture_warnings", True)
    
    # 从环境变量读取统一日志设置
    if unified_log is None:
        unified_log = config.get("unified_log", True)
    
    # 创建日志目录
    os.makedirs(log_dir, exist_ok=True)
    
    # 获取日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置最低级别，处理程序可以过滤
    
    # 清除现有处理程序（避免重复）
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # 配置控制台处理程序
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVELS.get(console_level.lower(), logging.INFO))
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 配置文件处理程序
    if unified_log:
        # 使用统一日志文件
        global _file_handlers
        
        # 检查是否已经有统一的文件处理程序
        handler_key = f"{log_dir}:{file_level}"
        
        if handler_key not in _file_handlers:
            # 创建新的统一文件处理程序
            log_file = os.path.join(log_dir, UNIFIED_LOG_FILE)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(LOG_LEVELS.get(file_level.lower(), logging.DEBUG))
            
            # 详细的格式化程序，包含模块位置信息
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            
            # 缓存处理程序以供重用
            _file_handlers[handler_key] = file_handler
        
        # 添加统一文件处理程序
        logger.addHandler(_file_handlers[handler_key])
    else:
        # 使用模块特定的日志文件
        if include_timestamp:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_name = f"{name if name else 'root'}_{timestamp}.log"
        else:
            log_name = f"{name if name else 'root'}.log"
        
        log_file = os.path.join(log_dir, log_name)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(LOG_LEVELS.get(file_level.lower(), logging.DEBUG))
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # 设置是否捕获警告
    if capture_warnings:
        logging.captureWarnings(True)
    
    return logger

def get_logger(name: str, **kwargs):
    """
    获取一个命名的日志记录器
    
    如果日志记录器已存在且有处理程序，则直接返回；
    否则使用setup_logger创建一个新的。
    
    Args:
        name: 日志记录器名称
        **kwargs: 传递给setup_logger的关键字参数
        
    Returns:
        logger: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger
    
    return setup_logger(name, **kwargs) 