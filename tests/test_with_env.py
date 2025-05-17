#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试browser-use内容提取功能（使用命令行环境变量）

此脚本用于测试使用browser-use库进行网页内容提取，支持通过命令行参数传入环境变量
"""

import os
import sys
import time
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# 导入内容提取模块
from src.web_scraping_toolkit.content.content_fetcher import fetch_article_content


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="测试browser-use内容提取")
    parser.add_argument("--api-key", help="OpenAI API密钥")
    parser.add_argument("--org", help="OpenAI组织ID", default="org-CSbk0H5wWnHQugObHUEypy0M")
    parser.add_argument("--url", help="要测试的URL", default="https://en.wikipedia.org/wiki/Web_scraping")
    return parser.parse_args()


def test_browser_use(api_key=None, org_id=None, test_url=None):
    """
    测试使用browser-use提取网页内容
    """
    # 设置环境变量
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    if org_id:
        os.environ["OPENAI_ORGANIZATION"] = org_id
    
    # 检查API密钥是否设置
    if not os.environ.get("OPENAI_API_KEY"):
        print("警告: 未设置OPENAI_API_KEY环境变量，browser-use将无法使用")
        print("请通过--api-key参数提供API密钥")
        print("例如: python tests/test_with_env.py --api-key=你的API密钥")
        return
    
    # 输出环境变量状态
    print("\n环境变量设置:")
    print(f"OPENAI_API_KEY: {'已设置' if os.environ.get('OPENAI_API_KEY') else '未设置'}")
    print(f"OPENAI_ORGANIZATION: {os.environ.get('OPENAI_ORGANIZATION') or '未设置'}")
    
    # 默认测试URL
    if not test_url:
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
    # 解析命令行参数
    args = parse_args()
    
    # 运行测试
    test_browser_use(
        api_key=args.api_key,
        org_id=args.org,
        test_url=args.url
    ) 