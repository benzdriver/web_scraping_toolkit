# Web Scraping Toolkit

一个功能强大的网页抓取工具包，集成了代理管理、验证码解决、缓存机制和数据提取功能。

## 功能特点

Web Scraping Toolkit 提供了以下主要功能：

### 核心功能

- **智能代理管理 (ProxyManager)**
  - 支持多种代理源（SmartProxy、自定义代理列表）
  - 自动代理轮换与健康检查
  - 问题代理的黑名单管理
  - 根据请求数量或时间间隔自动切换代理

- **验证码解决 (CaptchaSolver)**
  - 集成2Captcha等验证码解决服务
  - 自动检测和解决reCAPTCHA挑战
  - 灵活的回退策略

- **缓存机制 (CacheMechanism)**
  - 高效的请求缓存系统
  - 避免重复请求相同的URL
  - 缓存内容的过期管理

- **高级网页抓取 (WebScraper)**
  - HTTP请求与浏览器自动化无缝切换
  - 自动处理JavaScript渲染的页面
  - 智能用户代理管理，防止指纹识别
  - 多种故障恢复策略

### 趋势数据抓取 (trends 模块)

提供了多种方法获取 Google Trends 的热度数据：

- **SerpAPI 集成**: 通过第三方 API 服务获取 Google Trends 数据
- **PyTrends 集成**: 使用官方 Python 库获取 Google Trends 数据
- **批量处理**: 批量获取多个关键词的热度数据
- **智能后备**: 当 API 不可用时提供智能估算值
- **加权关键词**: 基于类别和优先级的关键词加权和排序

### 内容抓取 (content 模块)

提供了抓取和管理网页内容的工具：

- **智能内容抓取**: 使用 browser-use 自动识别和提取网页主体内容，有效应对反爬虫
- **动态内容渲染**: 使用 Playwright 抓取动态渲染的网页内容
- **内容解析**: 使用 BeautifulSoup 解析静态网页内容
- **新闻缓存**: 缓存网页内容，避免重复处理
- **状态管理**: 跟踪处理状态，记录已处理和未处理的内容

## 安装

```bash
# 从源代码安装
pip install -e .

# 或直接安装依赖
pip install -r requirements.txt
```

## 使用示例

### 基础用法

```python
from web_scraping_toolkit import ProxyManager, CacheMechanism, WebScraper

# 初始化代理管理器
proxy_manager = ProxyManager()

# 初始化缓存系统
cache = CacheMechanism("my_scraping_cache")

# 创建带有自动代理轮换和缓存功能的抓取器
scraper = WebScraper(
    proxy_manager=proxy_manager,
    cache_mechanism=cache
)

# 使用自动代理轮换和缓存获取网页
response = scraper.get("https://example.com")
```

### 代理轮换

```python
from web_scraping_toolkit import ProxyManager

# 使用自定义设置创建代理管理器
proxy_manager = ProxyManager(
    rotation_interval=300,  # 每5分钟轮换一次
    max_requests_per_ip=10  # 每个IP最多请求10次后轮换
)

# 获取用于requests的代理
proxy = proxy_manager.get_proxy()

# 将当前代理标记为问题代理（例如被封禁）
proxy_manager.blacklist_current_proxy(duration_minutes=30)

# 获取专门为Playwright格式化的代理
playwright_proxy = proxy_manager.get_playwright_proxy()
```

### 验证码解决

```python
from web_scraping_toolkit import CaptchaSolver

# 使用您的2Captcha API密钥初始化
solver = CaptchaSolver(api_key="your_2captcha_api_key")

# 解决reCAPTCHA
solution = solver.solve_recaptcha(
    site_key="6LcXXXXXXXXXXXXXXXXXXXXX",
    page_url="https://example.com"
)

# 与Playwright一起使用
def handle_page_with_captcha(page):
    if solver.detect_and_solve_recaptcha(page):
        print("验证码解决成功！")
```

### 缓存管理

```python
from web_scraping_toolkit import CacheMechanism

# 使用特定名称初始化缓存
cache = CacheMechanism("news_scraper_cache")

# 检查项目是否在缓存中
if cache.is_cached("https://example.com/article-1"):
    # 获取缓存数据
    data = cache.get_cached_data("https://example.com/article-1")
else:
    # 获取并缓存新数据
    data = fetch_new_data()
    cache.cache_data("https://example.com/article-1", data)

# 将项目标记为已处理
cache.mark_as_processed("https://example.com/article-1", stage="content_extraction")

# 获取未处理的项目
unprocessed = cache.get_unprocessed_items(stage="content_extraction")
```

### 趋势数据抓取

```python
from web_scraping_toolkit import get_trend_score_via_pytrends

# 获取单个关键词的热度分数
score = get_trend_score_via_pytrends("Express Entry")
print(f"热度分数: {score}")

# 批量获取多个关键词的热度分数
from web_scraping_toolkit import get_keyword_batch_scores

keywords = ["Express Entry", "Canada immigration", "Study permit"]
scores = get_keyword_batch_scores(keywords)

for kw, score in scores.items():
    print(f"{kw}: {score}")
```

### 加权关键词排序

```python
from web_scraping_toolkit import fetch_weighted_trending_keywords

# 定义关键词类别
keyword_categories = {
    "签证类别": ["Express Entry", "PR card", "Study permit"],
    "移民路径": ["PNP", "Atlantic Immigration", "Startup visa"]
}

# 定义高优先级关键词
priority_keywords = ["Express Entry draw", "CRS cutoff"]

# 获取加权排序后的关键词
weighted_keywords = fetch_weighted_trending_keywords(
    keywords_by_category=keyword_categories,
    priority_keywords=priority_keywords,
    max_keywords=5
)
```

### 内容抓取

```python
from web_scraping_toolkit import fetch_article_content

# 智能内容抓取（使用 browser-use）
url = "https://example.com/article"
content = fetch_article_content(url)
print(content[:200] + "...")  # 预览前200个字符

# 禁用 browser-use，仅使用 Playwright 和 BeautifulSoup
content = fetch_article_content(url, use_browser_use=False)

# 指定自定义 CSS 选择器
selectors = ['div.article-content', '.main-article', '#content']
content = fetch_article_content(url, selectors=selectors)
```

### 新闻缓存

```python
from web_scraping_toolkit import (
    check_cached_news,
    update_news_cache,
    mark_news_processed
)

# 更新新闻缓存
news_items = [
    {"title": "标题1", "url": "https://example.com/1", "keyword": "关键词1"},
    {"title": "标题2", "url": "https://example.com/2", "keyword": "关键词2"}
]
update_news_cache(news_items)

# 标记新闻已处理
mark_news_processed("https://example.com/1", "content_generation")

# 获取未处理的新闻
from web_scraping_toolkit import get_unprocessed_news
unprocessed = get_unprocessed_news("content_generation")
```

## 配置

工具包支持通过环境变量或`.env`文件进行配置：

```
# .env 文件示例
USE_PROXY=true
PROXY_ROTATION_INTERVAL=300  # 代理轮换间隔（秒）
PROXY_MAX_REQUESTS=10  # 每个代理最大请求数
SMARTPROXY_USERNAME=user
SMARTPROXY_PASSWORD=pass
SMARTPROXY_ENDPOINT=gate.smartproxy.com
SMARTPROXY_PORT=7000
SMARTPROXY_PROTOCOL=http  # 协议类型: http或socks5
SMARTPROXY_ADDITIONAL_PORTS=7001,7002,7003  # 额外端口列表
TWOCAPTCHA_API_KEY=your_key
SERPAPI_KEY=your_serpapi_key  # 用于Google Trends数据获取

# browser-use 配置
BROWSER_USE_LOGGING_LEVEL=info  # browser-use 日志级别

# 日志配置
LOG_LEVEL=INFO  # 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_DIR=logs    # 日志文件存储目录
LOG_CAPTURE_WARNINGS=true  # 是否捕获Python警告
```

## 详细文档

查看 `examples` 目录中的示例代码了解更多用法。完整的API文档将在项目稳定后提供。

### API密钥说明

- **SERPAPI_KEY**: 用于通过SerpAPI获取Google Trends数据，可从[SerpAPI官网](https://serpapi.com/)获取
- **TWOCAPTCHA_API_KEY**: 用于解决验证码挑战，可从[2Captcha官网](https://2captcha.com/)获取

### 代理配置详解

- **USE_PROXY**: 是否启用代理功能 (true/false)
- **PROXY_ROTATION_INTERVAL**: 代理轮换的时间间隔（秒）
- **PROXY_MAX_REQUESTS**: 每个代理最大请求数，超过后自动轮换
- **SMARTPROXY_USERNAME/PASSWORD**: SmartProxy服务的用户凭证
- **SMARTPROXY_ENDPOINT**: SmartProxy服务的入口地址
- **SMARTPROXY_PORT**: SmartProxy服务的主端口
- **SMARTPROXY_PROTOCOL**: 代理协议类型，支持http或socks5
- **SMARTPROXY_ADDITIONAL_PORTS**: 逗号分隔的额外端口列表，用于提高并发性能

### 日志配置详解

- **LOG_LEVEL**: 日志记录级别，控制记录哪些类型的消息
  - DEBUG: 所有调试信息（最详细）
  - INFO: 一般信息和重要事件
  - WARNING: 警告消息（可能有问题）
  - ERROR: 错误消息（功能受影响）
  - CRITICAL: 严重错误（程序可能崩溃）
- **LOG_DIR**: 日志文件存储目录
- **LOG_CAPTURE_WARNINGS**: 是否捕获Python内置的warnings并转为日志

更多日志系统使用详情，请参阅 [日志系统文档](docs/logging.md)。

## 系统要求

- Python 3.7+
- 依赖包：
  - requests>=2.25.0
  - beautifulsoup4>=4.9.0
  - python-dotenv>=0.15.0
  - 2captcha-python>=1.5.1
  - playwright>=1.20.0
  - pytrends>=4.9.0

## 许可证

MIT 