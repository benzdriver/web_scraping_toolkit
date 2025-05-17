#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试传统内容提取功能（不使用browser-use）

此脚本用于测试使用Playwright和BeautifulSoup进行网页内容提取
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
    parser = argparse.ArgumentParser(description="测试传统内容提取")
    parser.add_argument("--url", help="要测试的URL", default="https://en.wikipedia.org/wiki/Web_scraping")
    return parser.parse_args()


def test_content_extraction(test_url=None):
    """
    测试使用Playwright和BeautifulSoup提取网页内容
    """
    # 默认测试URL
    if not test_url:
        test_url = "https://en.wikipedia.org/wiki/Web_scraping"
    
    print(f"\n测试提取内容: {test_url}")
    print("-" * 80)
    
    # 使用Playwright提取内容
    print("\n1. 使用Playwright提取内容...")
    start = time.time()
    
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(test_url, timeout=20000)
            time.sleep(2)  # 等待页面渲染和跳转
            
            # 首先尝试使用常见选择器
            selectors = [
                'div.entry-content', 'article', 'div.article-content', 'div#content', 
                'div.post-content', 'div.main-content', 'main', '.article-body'
            ]
            
            content = None
            for sel in selectors:
                try:
                    node = page.query_selector(sel)
                    if node:
                        text = node.inner_text().strip()
                        if len(text) > 200:
                            content = text
                            break
                except Exception:
                    continue
            
            # 如果没有找到内容，尝试获取所有段落
            if not content:
                ps = page.query_selector_all('p')
                content = '\n'.join(p.inner_text().strip() for p in ps if p.inner_text())
            
            browser.close()
    except Exception as e:
        print(f"❌ Playwright提取失败！错误: {e}")
        content = None
    
    duration = time.time() - start
    
    # 显示结果
    if content and len(content) > 200:
        print(f"✅ 成功提取内容！耗时: {duration:.2f}秒")
        print(f"内容长度: {len(content)}字符")
        print("\n内容预览:")
        print("-" * 40)
        print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"❌ 提取失败！耗时: {duration:.2f}秒")
    
    print("-" * 80)
    
    # 使用BeautifulSoup提取内容
    print("\n2. 使用BeautifulSoup提取内容...")
    start = time.time()
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        resp = requests.get(test_url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 首先尝试使用常见选择器
        selectors = [
            'div.entry-content', 'article', 'div.article-content', 'div#content', 
            'div.post-content', 'div.main-content', 'main', '.article-body'
        ]
        
        content = None
        for sel in selectors:
            node = soup.select_one(sel)
            if node and len(node.get_text(strip=True)) > 200:
                content = node.get_text(separator='\n', strip=True)
                break
        
        # 如果没有找到内容，尝试获取所有段落
        if not content:
            paragraphs = soup.find_all('p')
            content = '\n'.join(p.get_text(strip=True) for p in paragraphs)
            
    except Exception as e:
        print(f"❌ BeautifulSoup提取失败！错误: {e}")
        content = None
    
    duration = time.time() - start
    
    # 显示结果
    if content and len(content) > 200:
        print(f"✅ 成功提取内容！耗时: {duration:.2f}秒")
        print(f"内容长度: {len(content)}字符")
        print("\n内容预览:")
        print("-" * 40)
        print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"❌ 提取失败！耗时: {duration:.2f}秒")
    
    print("-" * 80)
    

if __name__ == "__main__":
    # 解析命令行参数
    args = parse_args()
    
    # 运行测试
    test_content_extraction(test_url=args.url) 