#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试浏览器提取功能

此脚本测试 content_fetcher 模块的内容抓取功能，特别是使用 browser-use 抓取复杂网页
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(".").resolve()
sys.path.insert(0, str(project_root))

from src.web_scraping_toolkit.content.content_fetcher import fetch_article_content

def test_content_extraction():
    """
    测试不同网站的内容提取能力
    """
    urls = [
        # 常规新闻网站
        "https://www.bbc.com/news/world-us-canada-65766362",  # BBC News
        "https://www.nytimes.com/2023/06/08/world/europe/ukraine-dam-collapse-russia.html",  # NYT
        
        # 使用JavaScript渲染内容的网站
        "https://medium.com/better-programming/10-extraordinary-github-repos-for-all-developers-939cdeb28ad0",  # Medium
        
        # 反爬虫较强的网站
        "https://www.bloomberg.com/news/articles/2023-06-09/uk-economy-rebounds-with-0-2-growth-in-april-after-march-drop",  # Bloomberg
    ]
    
    for url in urls:
        print(f"\n{'='*50}\n测试URL: {url}\n{'='*50}")
        
        # 测试1: 使用 browser-use
        print("\n[使用 browser-use]")
        start_time = time.time()
        content = fetch_article_content(url, use_browser_use=True)
        elapsed_time = time.time() - start_time
        if content:
            print(f"成功! 内容长度: {len(content)}字符")
            print(f"内容摘要: {content[:150]}...")
        else:
            print("失败! 无法提取内容")
        print(f"耗时: {elapsed_time:.2f}秒")
        
        # 测试2: 不使用 browser-use (仅 Playwright 和 requests+BS4)
        print("\n[不使用 browser-use]")
        start_time = time.time()
        content = fetch_article_content(url, use_browser_use=False)
        elapsed_time = time.time() - start_time
        if content:
            print(f"成功! 内容长度: {len(content)}字符")
            print(f"内容摘要: {content[:150]}...")
        else:
            print("失败! 无法提取内容")
        print(f"耗时: {elapsed_time:.2f}秒")

if __name__ == "__main__":
    test_content_extraction() 