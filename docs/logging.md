# Web Scraping Toolkit 日志系统指南

Web Scraping Toolkit 提供了一个集中式日志系统，用于统一管理项目中的日志记录。本文档将指导您如何在项目中正确使用日志系统。

## 日志系统概述

日志系统提供以下功能：

- 统一的日志格式和级别
- 同时输出到控制台和文件
- 可配置的日志级别
- 支持统一日志文件或按模块分散日志文件
- 日志文件自动按时间戳命名（在非统一模式下）
- 支持捕获 Python 警告

## 在模块中使用日志

### 基本用法

在您的模块中使用日志系统的基本步骤：

```python
# 1. 导入日志系统
from web_scraping_toolkit.utils.logger import get_logger

# 2. 创建模块专用的日志记录器
logger = get_logger("模块名称")

# 3. 使用不同级别记录日志
logger.debug("调试信息，仅在调试时显示")
logger.info("一般信息，正常操作时显示")
logger.warning("警告信息，表示可能有问题")
logger.error("错误信息，表示出现了错误")
logger.critical("严重错误，表示程序可能无法继续")

# 4. 记录异常
try:
    # 执行可能会抛出异常的代码
    result = some_risky_operation()
except Exception as e:
    # 使用 exc_info=True 记录异常堆栈
    logger.error(f"操作失败: {e}", exc_info=True)
```

### 日志命名约定

为了保持日志名称的一致性和层次结构，我们采用以下命名约定：

- 顶级模块使用简单名称：`get_logger("proxy_manager")`
- 子模块使用点分隔的层次结构：`get_logger("web_scraping_toolkit.trends")`
- 测试模块添加 "test" 前缀：`get_logger("test.proxy_manager")`

## 日志配置

### 在应用程序中配置日志

如果您想更精细地控制日志系统，可以使用 `setup_logger` 函数：

```python
from web_scraping_toolkit.utils.logger import setup_logger

# 创建一个自定义配置的日志记录器
logger = setup_logger(
    name="my_module",              # 日志记录器名称
    log_dir="custom_logs",         # 日志文件目录
    console_level="info",          # 控制台日志级别 (debug, info, warning, error, critical)
    file_level="debug",            # 文件日志级别
    capture_warnings=True,         # 是否捕获 Python 警告
    include_timestamp=True,        # 是否在日志文件名中包含时间戳（仅当unified_log=False时有效）
    unified_log=True               # 是否将所有日志写入同一个文件
)
```

### 环境变量配置

日志系统可以通过环境变量或 `.env` 文件进行配置：

```
# .env 文件示例
LOG_LEVEL=DEBUG             # 全局日志级别
LOG_DIR=logs                # 日志文件目录
LOG_CAPTURE_WARNINGS=true   # 是否捕获警告
LOG_UNIFIED=true            # 是否使用统一日志文件
```

## 统一日志模式与分散日志模式

### 统一日志模式（默认）

在统一日志模式下，所有模块的日志都会写入同一个名为`web_scraping_toolkit.log`的文件中。这样可以更方便地查看整个应用程序的运行流程，尤其是在调试复杂问题时。每条日志记录都包含模块名称和源代码位置信息，便于定位问题。

启用统一日志模式（默认已启用）：
```python
# 通过环境变量启用
os.environ["LOG_UNIFIED"] = "true"

# 或在setup_logger中启用
logger = setup_logger(name="my_module", unified_log=True)
```

### 分散日志模式

在分散日志模式下，每个模块有自己的日志文件，文件名格式为`{模块名}_{时间戳}.log`。当您需要隔离不同模块的日志时，这种模式很有用。

启用分散日志模式：
```python
# 通过环境变量启用
os.environ["LOG_UNIFIED"] = "false"

# 或在setup_logger中启用
logger = setup_logger(name="my_module", unified_log=False)
```

## 最佳实践

1. **使用适当的日志级别**
   - DEBUG: 详细的调试信息
   - INFO: 常规操作信息
   - WARNING: 警告但不影响主要功能
   - ERROR: 错误导致功能无法正常工作
   - CRITICAL: 严重错误导致程序可能崩溃

2. **提供足够的上下文**
   - 包含相关参数和返回值
   - 记录操作的目标和结果
   - 对于错误，说明原因和影响

3. **避免敏感信息**
   - 不要记录密码、API密钥等敏感信息
   - 对长文本使用截断或摘要

4. **异常处理**
   - 使用 `exc_info=True` 记录完整异常堆栈
   - 在捕获异常的地方记录日志，而不是重新抛出

## 日志文件管理

日志文件存储在 `logs` 目录下（除非另行配置）：

- **统一日志模式**：所有日志写入单个文件 `web_scraping_toolkit.log`
- **分散日志模式**：每个模块有自己的日志文件，格式为 `{模块名}_{时间戳}.log`

在生产环境中，应定期清理旧的日志文件，以防止磁盘空间占用过大。对于统一日志文件，可以考虑使用日志滚动（log rotation）策略，当文件达到一定大小时自动创建新的日志文件。 