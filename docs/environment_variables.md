# 环境变量配置

Web Scraping Toolkit 支持通过环境变量或 `.env` 文件进行配置。本文档列出了所有支持的环境变量及其用途。

## 创建 .env 文件

将以下内容复制到项目根目录的 `.env` 文件中，并根据需要修改各项设置：

```bash
# Web Scraping Toolkit 环境变量示例文件

# ===== OpenAI 配置 =====
# 用于 browser-use 内容提取的OpenAI API密钥
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_ORGANIZATION=your_openai_organization_id_here

# ===== browser-use 配置 =====
# browser-use 日志级别 (debug, info, warning, error, critical)
BROWSER_USE_LOGGING_LEVEL=info

# ===== 代理配置 =====
USE_PROXY=false
PROXY_ROTATION_INTERVAL=300  # 代理轮换间隔（秒）
PROXY_MAX_REQUESTS=10  # 每个代理最大请求数

# ===== SmartProxy 配置 =====
SMARTPROXY_USERNAME=user
SMARTPROXY_PASSWORD=pass
SMARTPROXY_ENDPOINT=gate.smartproxy.com
SMARTPROXY_PORT=7000
SMARTPROXY_PROTOCOL=http  # 协议类型: http或socks5
SMARTPROXY_ADDITIONAL_PORTS=7001,7002,7003  # 额外端口列表

# ===== 验证码相关 =====
TWOCAPTCHA_API_KEY=your_key

# ===== Google Trends API =====
SERPAPI_KEY=your_serpapi_key  # 用于Google Trends数据获取

# ===== 日志配置 =====
LOG_LEVEL=INFO  # 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_DIR=logs    # 日志文件存储目录
LOG_CAPTURE_WARNINGS=true  # 是否捕获Python警告
```

## 环境变量详解

### browser-use 配置

browser-use 是一个强大的浏览器自动化工具，用于从复杂网页提取内容。它需要以下环境变量：

* **OPENAI_API_KEY**: OpenAI API密钥，用于browser-use的AI模型。必须提供才能使用browser-use功能。
* **OPENAI_ORGANIZATION**: OpenAI组织ID，用于API调用的组织归属。
* **BROWSER_USE_LOGGING_LEVEL**: browser-use的日志级别，可以是debug、info、warning、error或critical。

### 代理配置

这些设置控制代理轮换和使用行为：

* **USE_PROXY**: 是否启用代理功能(true/false)
* **PROXY_ROTATION_INTERVAL**: 代理轮换的时间间隔（秒）
* **PROXY_MAX_REQUESTS**: 每个代理最大请求数，超过后自动轮换

### SmartProxy 配置

如果你使用SmartProxy服务，需要以下设置：

* **SMARTPROXY_USERNAME/PASSWORD**: SmartProxy服务的用户凭证
* **SMARTPROXY_ENDPOINT**: SmartProxy服务的入口地址
* **SMARTPROXY_PORT**: SmartProxy服务的主端口
* **SMARTPROXY_PROTOCOL**: 代理协议类型，支持http或socks5
* **SMARTPROXY_ADDITIONAL_PORTS**: 逗号分隔的额外端口列表，用于提高并发性能

### API密钥

各种外部服务的API密钥：

* **TWOCAPTCHA_API_KEY**: 用于解决验证码挑战，可从[2Captcha官网](https://2captcha.com/)获取
* **SERPAPI_KEY**: 用于通过SerpAPI获取Google Trends数据，可从[SerpAPI官网](https://serpapi.com/)获取

### 日志配置

控制日志记录行为：

* **LOG_LEVEL**: 日志记录级别，控制记录哪些类型的消息(DEBUG/INFO/WARNING/ERROR/CRITICAL)
* **LOG_DIR**: 日志文件存储目录
* **LOG_CAPTURE_WARNINGS**: 是否捕获Python内置的warnings并转为日志 