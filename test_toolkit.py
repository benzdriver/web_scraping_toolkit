#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 web_scraping_toolkit 功能的独立脚本

此脚本测试 web_scraping_toolkit 的核心功能：
1. 代理管理和轮换
2. Google Trends 数据获取
3. 文章内容抓取
4. 关键词加权和排序
5. 关键词新闻获取
6. 完整数据获取流程
"""

import os
import sys
import json
import time
from dotenv import load_dotenv
from datetime import datetime

# 导入我们的工具包
from web_scraping_toolkit import (
    ProxyManager, CaptchaSolver, CacheMechanism, WebScraper,
    get_trend_score_via_serpapi, get_trend_score_via_pytrends,
    get_keyword_batch_scores, fetch_weighted_trending_keywords,
    fetch_article_content
)

# 导入日志系统
from web_scraping_toolkit.utils.logger import setup_logger

# 创建测试结果目录
TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results")
os.makedirs(TEST_DIR, exist_ok=True)

# 加载环境变量
load_dotenv()

def setup_toolkit_components(logger):
    """设置 web_scraping_toolkit 组件"""
    logger.info("=== 设置 Web Scraping Toolkit ===")
    
    # 初始化代理管理器
    proxy_manager = ProxyManager()
    logger.info(f"代理管理器已初始化，共有 {proxy_manager.proxy_count} 个代理")
    
    # 初始化验证码解析器
    captcha_solver = CaptchaSolver()
    logger.info(f"验证码解析器可用: {captcha_solver.is_available()}")
    
    # 初始化缓存
    cache = CacheMechanism("toolkit_test")
    logger.info(f"缓存机制已初始化")
    
    # 创建网页抓取器
    scraper = WebScraper(
        proxy_manager=proxy_manager,
        captcha_solver=captcha_solver,
        cache_mechanism=cache,
        browser_headless=True
    )
    
    return proxy_manager, captcha_solver, cache, scraper

def test_google_trends_fetch(logger):
    """测试从 Google Trends 获取热度分数"""
    logger.info("=== 测试 Google Trends 数据获取 ===")
    
    # 测试关键词
    test_keywords = [
        "Canadian immigration",
        "Express Entry Canada",
        "Canada PNP",
        "Study permit Canada"
    ]
    
    results = {}
    
    # 首先检查 SerpAPI 是否可用
    serpapi_key = os.environ.get("SERPAPI_KEY")
    if serpapi_key:
        logger.info("找到 SerpAPI 密钥，测试 SerpAPI 方法...")
        for keyword in test_keywords[:2]:  # 只用 SerpAPI 测试两个关键词
            logger.info(f"获取关键词热度: {keyword} (使用 SerpAPI)")
            try:
                score = get_trend_score_via_serpapi(keyword)
                logger.info(f"热度分数: {score}")
                results[keyword] = score
                time.sleep(2)
            except Exception as e:
                logger.error(f"使用 SerpAPI 获取 '{keyword}' 的热度分数时出错: {e}", exc_info=True)
    else:
        logger.warning("未找到 SerpAPI 密钥，跳过 SerpAPI 测试")
    
    # 然后使用 PyTrends 测试
    logger.info("使用 PyTrends 测试...")
    for keyword in test_keywords:
        if keyword in results and results[keyword] is not None:
            continue  # 如果已经通过 SerpAPI 成功获取，则跳过
            
        logger.info(f"获取关键词热度: {keyword} (使用 PyTrends)")
        try:
            score = get_trend_score_via_pytrends(keyword)
            logger.info(f"热度分数: {score}")
            results[keyword] = score
            time.sleep(2)
        except Exception as e:
            logger.error(f"使用 PyTrends 获取 '{keyword}' 的热度分数时出错: {e}", exc_info=True)
            results[keyword] = None
    
    # 保存结果
    output_file = os.path.join(TEST_DIR, "trends_test_results.json")
    with open(output_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)
    
    logger.info(f"热度测试结果已保存到 {output_file}")
    return results

def test_article_extraction(logger):
    """测试文章内容抓取"""
    logger.info("=== 测试文章内容抓取 ===")
    
    # 测试 URL
    test_urls = [
        "https://www.cicnews.com/2023/05/canada-welcomes-over-26000-new-immigrants-in-march-0526544.html",
        "https://www.canada.ca/en/immigration-refugees-citizenship/news/2023/04/canada-launches-new-international-health-care-worker-immigration-pathway.html",
        "https://www.ctvnews.ca/canada/canada-unveils-new-pathways-for-foreign-healthcare-workers-to-get-permanent-residency-1.6364977"
    ]
    
    results = {}
    
    for url in test_urls:
        logger.info(f"从以下网址抓取文章内容: {url}")
        try:
            # 使用我们的函数抓取文章
            content = fetch_article_content(url)
            if content:
                logger.info(f"已抓取 {len(content)} 个字符")
                
                # 存储内容预览
                preview = content[:200] + "..." if len(content) > 200 else content
                results[url] = {
                    "success": True,
                    "length": len(content),
                    "preview": preview
                }
                logger.debug(f"内容预览: {preview}")
            else:
                logger.warning("抓取内容失败")
                results[url] = {
                    "success": False,
                    "reason": "未返回内容"
                }
                
            # 请求之间添加小延迟
            time.sleep(2)
        except Exception as e:
            logger.error(f"从 '{url}' 抓取内容时出错: {e}", exc_info=True)
            results[url] = {
                "success": False,
                "reason": str(e)
            }
    
    # 保存结果
    output_file = os.path.join(TEST_DIR, "article_extraction_test_results.json")
    with open(output_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)
    
    logger.info(f"文章抓取结果已保存到 {output_file}")
    return results

def test_trending_keywords(logger):
    """测试热门关键词生成"""
    logger.info("=== 测试热门关键词生成 ===")
    
    try:
        # 定义关键词类别
        keyword_categories = {
            "签证类别": ["Express Entry", "PR card", "Study permit"],
            "移民路径": ["PNP", "Atlantic Immigration", "Startup visa"]
        }
        
        # 定义优先级关键词
        priority_keywords = ["Express Entry draw", "CRS cutoff"]
        
        # 获取加权关键词
        logger.info("获取加权热门关键词...")
        weighted_keywords = fetch_weighted_trending_keywords(
            keywords_by_category=keyword_categories,
            priority_keywords=priority_keywords,
            max_keywords=5
        )
        
        # 显示结果
        logger.info("热门关键词结果:")
        for i, kw_data in enumerate(weighted_keywords, 1):
            logger.info(f"{i}. {kw_data['keyword']} (分数: {kw_data['base_score']}, 加权分数: {kw_data['weighted_score']})")
        
        # 保存结果
        output_file = os.path.join(TEST_DIR, "trending_keywords_test_results.json")
        with open(output_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": weighted_keywords
            }, f, indent=2)
        
        logger.info(f"热门关键词结果已保存到 {output_file}")
        return weighted_keywords
    except Exception as e:
        logger.error(f"测试热门关键词生成时出错: {e}", exc_info=True)
        return None

def test_news_cache(logger):
    """测试新闻缓存功能"""
    from web_scraping_toolkit import (
        check_cached_news, update_news_cache,
        mark_news_processed, get_unprocessed_news
    )
    
    logger.info("=== 测试新闻缓存功能 ===")
    
    # 测试新闻项
    test_news = [
        {"title": "加拿大欢迎26,000名新移民", "url": "https://example.com/news1", "keyword": "移民"},
        {"title": "Express Entry最新一轮邀请", "url": "https://example.com/news2", "keyword": "Express Entry"},
        {"title": "安大略省提名计划更新", "url": "https://example.com/news3", "keyword": "PNP"}
    ]
    
    try:
        # 更新缓存
        logger.info("更新新闻缓存...")
        update_news_cache(test_news)
        
        # 检查缓存
        logger.info("检查缓存的新闻...")
        cached_news = check_cached_news()
        logger.info(f"缓存中有 {len(cached_news)} 条新闻")
        
        # 标记一条新闻为已处理
        logger.info("标记一条新闻为已处理...")
        mark_news_processed("https://example.com/news1", "content_generation")
        
        # 获取未处理的新闻
        logger.info("获取未处理的新闻...")
        unprocessed = get_unprocessed_news("content_generation")
        logger.info(f"有 {len(unprocessed)} 条未处理的新闻")
        for i, news in enumerate(unprocessed, 1):
            logger.debug(f"未处理新闻 {i}: {news['title']} ({news['url']})")
        
        # 保存结果
        output_file = os.path.join(TEST_DIR, "news_cache_test_results.json")
        with open(output_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "cached_count": len(cached_news),
                "unprocessed_count": len(unprocessed),
                "unprocessed": unprocessed
            }, f, indent=2)
        
        logger.info(f"新闻缓存测试结果已保存到 {output_file}")
        return True
    except Exception as e:
        logger.error(f"测试新闻缓存时出错: {e}", exc_info=True)
        return False

def test_news_fetch(logger):
    """测试为特定关键词获取新闻项目"""
    # 从正确的模块导入函数
    from web_scraping_toolkit.content import fetch_article_content
    
    logger.info("=== 测试关键词新闻获取 ===")
    
    # 创建一个关键词数据条目
    keyword_data = {
        "keyword": "Express Entry Canada",
        "category": "移民路径",
        "base_score": 80,
        "weighted_score": 96,
        "type": "news_article"
    }
    
    try:
        # 搜索该关键词的新闻 (简化版)
        news_urls = [
            "https://www.cicnews.com/2023/05/canada-welcomes-over-26000-new-immigrants-in-march-0526544.html",
            "https://www.ctvnews.ca/canada/canada-unveils-new-pathways-for-foreign-healthcare-workers-to-get-permanent-residency-1.6364977"
        ]
        
        logger.info(f"获取关键词 '{keyword_data['keyword']}' 的新闻...")
        news_items = []
        
        for i, url in enumerate(news_urls):
            logger.info(f"抓取URL: {url}")
            content = fetch_article_content(url)
            
            if content:
                item = {
                    "title": f"{keyword_data['keyword']} 相关新闻 #{i+1}",
                    "url": url,
                    "source": "测试来源",
                    "full_content": content,
                    "keyword": keyword_data["keyword"]
                }
                news_items.append(item)
                logger.info(f"已获取文章，内容长度: {len(content)} 字符")
            else:
                logger.warning(f"无法获取内容，跳过")
        
        logger.info(f"获取到 {len(news_items)} 条新闻项目:")
        for i, item in enumerate(news_items, 1):
            logger.info(f"{i}. {item['title']} | 来源: {item.get('source', '未知')}")
            logger.info(f"   URL: {item['url']}")
            logger.info(f"   内容长度: {len(item.get('full_content', '')) if item.get('full_content') else 0} 字符")
        
        # 保存结果
        output_file = os.path.join(TEST_DIR, "news_fetch_test_results.json")
        with open(output_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "keyword_data": keyword_data,
                "news_items": news_items
            }, f, indent=2)
        
        logger.info(f"新闻获取测试结果已保存到 {output_file}")
        return news_items
    except Exception as e:
        logger.error(f"获取关键词新闻时出错: {e}", exc_info=True)
        return None

def test_full_pipeline(logger):
    """测试完整的数据获取流程"""
    logger.info("=== 测试完整数据获取流程 ===")
    
    try:
        # 1. 获取热门关键词
        logger.info("第1步: 获取热门关键词...")
        keywords = fetch_weighted_trending_keywords(
            keywords_by_category={
                "移民类别": ["Express Entry", "PNP", "Study permit"],
                "热门省份": ["Ontario immigration", "British Columbia immigration"]
            },
            max_keywords=3
        )
        
        logger.info(f"获取到 {len(keywords)} 个关键词:")
        for i, kw in enumerate(keywords, 1):
            logger.info(f"{i}. {kw['keyword']} (分数: {kw['base_score']})")
        
        # 2. 为每个关键词获取新闻内容
        logger.info("第2步: 获取关键词相关新闻...")
        all_news = []
        
        # 每个关键词只处理最多2个新闻，加速测试
        max_news_per_keyword = 2
        
        # 测试用的新闻URL
        test_urls = [
            "https://www.cicnews.com/2023/05/canada-welcomes-over-26000-new-immigrants-in-march-0526544.html",
            "https://www.ctvnews.ca/canada/canada-unveils-new-pathways-for-foreign-healthcare-workers-to-get-permanent-residency-1.6364977"
        ]
        
        for kw_data in keywords[:2]:  # 只处理前两个关键词
            logger.info(f"处理关键词: {kw_data['keyword']}")
            
            # 为了测试，我们使用固定的URL
            keyword_news = []
            
            for i, url in enumerate(test_urls[:max_news_per_keyword]):
                logger.info(f"  抓取URL: {url}")
                content = fetch_article_content(url)
                
                if content:
                    news_item = {
                        "title": f"{kw_data['keyword']} 相关新闻 #{i+1}",
                        "url": url,
                        "source": "测试来源",
                        "keyword": kw_data["keyword"],
                        "full_content": content[:500] + "..." if len(content) > 500 else content,
                        "category": kw_data.get("category", "未分类")
                    }
                    keyword_news.append(news_item)
                    logger.info(f"  成功获取内容，长度: {len(content)} 字符")
                else:
                    logger.warning(f"  无法获取内容，跳过")
            
            all_news.extend(keyword_news)
            logger.info(f"关键词 '{kw_data['keyword']}' 获取到 {len(keyword_news)} 条新闻")
        
        # 3. 更新缓存
        logger.info("第3步: 更新新闻缓存...")
        from web_scraping_toolkit import update_news_cache
        update_news_cache(all_news)
        logger.info(f"已将 {len(all_news)} 条新闻添加到缓存")
        
        # 汇总结果
        pipeline_results = {
            "keywords": keywords,
            "news_items": all_news
        }
        
        # 保存结果
        output_file = os.path.join(TEST_DIR, "pipeline_test_results.json")
        with open(output_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "keywords_count": len(keywords),
                "news_count": len(all_news),
                "results": pipeline_results
            }, f, indent=2)
        
        logger.info(f"完整流程测试结果已保存到 {output_file}")
        return pipeline_results
    except Exception as e:
        logger.error(f"运行完整数据获取流程时出错: {e}", exc_info=True)
        return None

def main():
    """主函数，运行所有测试"""
    # 设置日志记录器
    logger = setup_logger(
        name="web_scraping_test",
        log_dir="logs",
        console_level="info",
        file_level="debug",
        include_timestamp=True,
        unified_log=True  # 使用统一日志文件
    )
    
    start_time = time.time()
    logger.info("开始测试 web_scraping_toolkit")
    
    # 设置组件
    proxy_manager, captcha_solver, cache, scraper = setup_toolkit_components(logger)
    
    # 显示可用测试
    logger.info("可用测试:")
    logger.info("1. Google Trends 数据获取")
    logger.info("2. 文章内容抓取")
    logger.info("3. 热门关键词生成")
    logger.info("4. 新闻缓存")
    logger.info("5. 关键词新闻获取")
    logger.info("6. 完整数据获取流程")
    logger.info("all. 运行所有测试")
    
    # 获取用户选择
    choice = input("\n选择要运行的测试 (1-6 或 'all'): ")
    
    try:
        if choice == '1' or choice.lower() == 'all':
            test_google_trends_fetch(logger)
            
        if choice == '2' or choice.lower() == 'all':
            test_article_extraction(logger)
            
        if choice == '3' or choice.lower() == 'all':
            test_trending_keywords(logger)
            
        if choice == '4' or choice.lower() == 'all':
            test_news_cache(logger)
            
        if choice == '5' or choice.lower() == 'all':
            test_news_fetch(logger)
            
        if choice == '6' or choice.lower() == 'all':
            test_full_pipeline(logger)
    except Exception as e:
        logger.error(f"测试执行失败: {e}", exc_info=True)
    
    end_time = time.time()
    logger.info(f"所有测试在 {end_time - start_time:.2f} 秒内完成")

if __name__ == "__main__":
    main() 