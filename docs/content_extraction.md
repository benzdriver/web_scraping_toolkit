# 内容提取模块

内容提取模块提供了从网页中提取正文内容的功能，支持多种提取策略和方法。

## 功能特点

内容提取模块支持以下三种提取策略，按照优先级使用：

1. **browser-use 智能提取**：利用浏览器自动化库和 AI 模型进行智能内容提取，有效应对复杂的网页结构和反爬虫措施。
2. **Playwright 动态渲染**：使用 Playwright 自动化浏览器动态渲染网页，可以处理动态加载的 JavaScript 内容。
3. **Requests + BeautifulSoup**：作为后备方案，使用 requests 获取静态网页内容，使用 BeautifulSoup 解析提取。

## 安装依赖

要完整支持全部功能，需要安装以下依赖：

```bash
pip install requests beautifulsoup4 playwright browser-use

# 安装 Playwright 浏览器
python -m playwright install chromium
```

## 使用方法

### 基本用法

```python
from web_scraping_toolkit.content.content_fetcher import fetch_article_content

# 测试 URL
url = "https://www.example.com/article/123"

# 默认使用所有方法（优先使用 browser-use）
content = fetch_article_content(url)

# 禁用 browser-use，只使用 Playwright 和 BeautifulSoup
content = fetch_article_content(url, use_browser_use=False)

# 指定自定义选择器
selectors = ['div.article-content', '.main-article', '#content']
content = fetch_article_content(url, selectors=selectors)
```

### browser-use 特性

browser-use 是一个强大的浏览器自动化库，主要特性包括：

1. **智能内容提取**：使用 AI 模型自动判断网页主要内容并提取
2. **反爬虫能力**：可以处理复杂的反爬虫网站
3. **定制提取**：通过描述性任务操作浏览器并提取特定内容

## 实现原理

### browser-use 流程

1. 创建 Agent 实例并描述任务
2. 并行运行并捕获页面结果
3. 返回提取的文本内容

### Playwright 流程

1. 打开无头浏览器并访问 URL
2. 等待页面加载完成
3. 通过 CSS 选择器定位和提取内容
4. 如果不成功，尝试提取所有段落

### 性能比较

| 方法 | 优点 | 缺点 |
| --- | --- | --- |
| browser-use | 智能处理复杂网页，可应对反爬虫 | 处理时间长，有 API 调用限制 |
| Playwright | 支持 JavaScript，可进行交互 | 配置复杂，内存消耗高 |
| Requests+BS4 | 简单快速，资源消耗小 | 不支持 JavaScript，无法处理动态内容 |

## 常见问题

### browser-use 未安装

如果没有安装 browser-use，系统会自动降级到 Playwright。要安装 browser-use：

```bash
pip install browser-use
```

### 内容提取失败

如果全部方法均无法提取内容，可介入以下步骤：

1. 检查网站是否有反爬虫措施或访问限制
2. 尝试自定义选择器列表
3. 增加等待时间或使用代理服务

## 示例项目

在项目根目录下有一个 `test_content_fetcher.py` 示例，可以运行测试不同提取方法的效果：

```bash
python test_content_fetcher.py
``` 