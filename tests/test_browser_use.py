#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试browser-use内容提取功能

此脚本用于测试使用browser-use库进行网页内容提取
"""

import os
import sys
import time
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# 导入内容提取模块
from src.web_scraping_toolkit.content.content_fetcher import fetch_article_content


def test_browser_use():
    """
    测试使用browser-use提取网页内容
    注意：需要设置OPENAI_API_KEY环境变量
    """
    # 检查API密钥是否设置
    if not os.environ.get("OPENAI_API_KEY"):
        print("警告: 未设置OPENAI_API_KEY环境变量，browser-use将无法使用")
        print("可以通过以下方式临时设置环境变量:")
        print("export OPENAI_API_KEY=你的API密钥")
        print("本次将使用后备方法 (Playwright 和 BeautifulSoup) 进行测试")
    
    # 测试URL
    test_url = "https://en.wikipedia.org/wiki/Web_scraping"
    
    print(f"\n测试提取内容: {test_url}")
    print("-" * 80)
    
    # 使用browser-use提取内容
    print("\n1. 使用browser-use提取内容...")
    start = time.time()
    content_with_browser_use = fetch_article_content(test_url, use_browser_use=True)
    duration_with_browser_use = time.time() - start
    
    # 显示结果
    if content_with_browser_use:
        print(f"✅ 成功提取内容！耗时: {duration_with_browser_use:.2f}秒")
        print(f"内容长度: {len(content_with_browser_use)}字符")
        print("\n内容预览:")
        print("-" * 40)
        print(content_with_browser_use[:500] + "..." if len(content_with_browser_use) > 500 else content_with_browser_use)
    else:
        print(f"❌ 提取失败！耗时: {duration_with_browser_use:.2f}秒")
    
    print("-" * 80)
    
    # 不使用browser-use提取内容
    print("\n2. 使用传统方法提取内容 (Playwright/BeautifulSoup)...")
    start = time.time()
    content_without_browser_use = fetch_article_content(test_url, use_browser_use=False)
    duration_without_browser_use = time.time() - start
    
    # 显示结果
    if content_without_browser_use:
        print(f"✅ 成功提取内容！耗时: {duration_without_browser_use:.2f}秒")
        print(f"内容长度: {len(content_without_browser_use)}字符")
        print("\n内容预览:")
        print("-" * 40)
        print(content_without_browser_use[:500] + "..." if len(content_without_browser_use) > 500 else content_without_browser_use)
    else:
        print(f"❌ 提取失败！耗时: {duration_without_browser_use:.2f}秒")
    
    print("-" * 80)
    
    # 比较两种方法
    if content_with_browser_use and content_without_browser_use:
        print("\n比较两种方法:")
        print(f"- browser-use 方法: {len(content_with_browser_use)}字符, 耗时 {duration_with_browser_use:.2f}秒")
        print(f"- 传统方法: {len(content_without_browser_use)}字符, 耗时 {duration_without_browser_use:.2f}秒")
        
        quality_diff = len(content_with_browser_use) / len(content_without_browser_use) if len(content_without_browser_use) > 0 else float('inf')
        speed_diff = duration_without_browser_use / duration_with_browser_use if duration_with_browser_use > 0 else float('inf')
        
        print(f"内容量比例 (browser-use/传统): {quality_diff:.2f}x")
        print(f"速度比例 (传统/browser-use): {speed_diff:.2f}x")


if __name__ == "__main__":
    # 创建tests目录（如果不存在）
    tests_dir = Path(__file__).resolve().parent
    tests_dir.mkdir(exist_ok=True)
    
    # 运行测试
    test_browser_use() 