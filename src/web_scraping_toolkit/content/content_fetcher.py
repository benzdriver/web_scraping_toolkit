"""
网页内容抓取工具

提供了用于抓取网页文章正文内容的工具，支持：
1. 使用 browser-use 进行智能网页内容提取（支持复杂反爬虫网站）
2. 使用 Playwright 进行动态网页内容提取
3. 使用 requests + BeautifulSoup 作为后备方案
"""

import time
import json
import requests
from typing import Optional, List, Any, Dict
from bs4 import BeautifulSoup

# 导入集中式日志系统
from ..utils.logger import get_logger

# 配置日志
logger = get_logger("web_scraping_toolkit.content")

def fetch_article_content(
    url: str, 
    min_length: int = 200, 
    selectors: Optional[List[str]] = None,
    use_browser_use: bool = True
) -> Optional[str]:
    """
    抓取网页文章的正文内容
    
    使用三种方法尝试抓取内容：
    1. 首先使用 browser-use（如果启用）进行智能内容提取
    2. 然后使用 Playwright（支持JavaScript渲染和动态内容）
    3. 如果失败，则使用 requests + BeautifulSoup 作为后备
    
    Args:
        url: 要抓取的网页URL
        min_length: 有效内容的最小长度
        selectors: 用于定位正文内容的CSS选择器列表
        use_browser_use: 是否启用 browser-use 进行智能内容提取
        
    Returns:
        抓取到的文章正文，如果抓取失败则返回None
    """
    # 默认选择器
    if selectors is None:
        selectors = [
            'div.entry-content', 'article', 'div.article-content', 'div#content', 
            'div.post-content', 'div.main-content', 'main', '.article-body'
        ]

    # 1. 先用 browser-use 智能提取（如果启用）
    if use_browser_use:
        try:
            from browser_use import Agent
            
            async def extract_content():
                # 初始化一个默认LLM
                try:
                    from langchain_openai import ChatOpenAI
                    
                    # 尝试从环境变量读取API密钥
                    import os
                    api_key = os.environ.get("OPENAI_API_KEY")
                    org_id = os.environ.get("OPENAI_ORGANIZATION")
                    
                    if not api_key:
                        logger.warning("[browser-use] 未设置OPENAI_API_KEY环境变量，无法使用browser-use")
                        return None
                    
                    # 构建LLM参数
                    llm_params = {
                        "api_key": api_key,
                        "model": "gpt-4o",  # 使用支持视觉的模型
                        "temperature": 0
                    }
                    
                    # 如果有组织ID，添加到参数中
                    if org_id:
                        llm_params["organization"] = org_id
                        
                    # 创建支持视觉能力的LLM实例
                    llm = ChatOpenAI(**llm_params)
                    
                    # 初始化Agent
                    agent = Agent(
                        task=f"Extract the main article content from this webpage: {url}. Return the content in plain text format only, without any explanations or structure.",
                        llm=llm,
                        use_vision=True,  # 启用视觉理解能力
                    )
                    
                    # 运行Agent
                    try:
                        result = await agent.run(max_steps=5)  # 限制步骤数以避免过长运行
                        
                        # 尝试从结果中提取内容
                        content = None
                        
                        # 尝试获取output属性
                        if hasattr(result, 'output'):
                            content = result.output
                            logger.info("[browser-use] 成功从output属性获取内容")
                        
                        # 如果没有output属性，尝试获取text属性
                        elif hasattr(result, 'text'):
                            content = result.text
                            logger.info("[browser-use] 成功从text属性获取内容")
                        
                        # 如果result是字典类型，尝试从常见键获取内容
                        elif isinstance(result, dict):
                            for key in ['output', 'text', 'content', 'result', 'main_content']:
                                if key in result:
                                    content_part = result[key]
                                    if isinstance(content_part, str):
                                        content = content_part
                                        logger.info(f"[browser-use] 成功从字典键 '{key}' 获取内容")
                                        break
                                    elif isinstance(content_part, dict) and "text" in content_part:
                                        content = content_part["text"]
                                        logger.info(f"[browser-use] 成功从字典键 '{key}.text' 获取内容")
                                        break
                        
                        # 如果还是没找到，尝试将整个result转为字符串
                        if not content:
                            try:
                                # 如果是JSON格式，先尝试解析
                                if hasattr(result, '__dict__'):
                                    result_dict = result.__dict__
                                    json_str = json.dumps(result_dict, default=str)
                                    result_obj = json.loads(json_str)
                                    
                                    # 从JSON对象中提取内容字段
                                    extracted_text = []
                                    def extract_text_fields(obj, depth=0):
                                        if depth > 5:  # 限制递归深度
                                            return
                                        
                                        if isinstance(obj, dict):
                                            for k, v in obj.items():
                                                if k in ['text', 'content', 'main_content', 'introduction', 'body']:
                                                    if isinstance(v, str) and len(v) > min_length:
                                                        extracted_text.append(v)
                                                else:
                                                    extract_text_fields(v, depth+1)
                                        elif isinstance(obj, list):
                                            for item in obj:
                                                extract_text_fields(item, depth+1)
                                    
                                    extract_text_fields(result_obj)
                                    if extracted_text:
                                        content = "\n\n".join(extracted_text)
                                        logger.info("[browser-use] 成功从JSON结构提取文本内容")
                            except Exception as e:
                                logger.warning(f"[browser-use] 尝试解析JSON失败: {e}")
                        
                        # 如果还是没找到，使用字符串表示
                        if not content:
                            try:
                                content = str(result)
                                logger.info("[browser-use] 使用结果的字符串表示")
                            except Exception as e:
                                logger.warning(f"[browser-use] 尝试字符串转换失败: {e}")
                                return None
                        
                        return content
                    except Exception as e:
                        logger.warning(f"[browser-use] 运行失败: {e}")
                        return None
                    
                except ImportError as e:
                    logger.warning(f"[browser-use] 未安装必要的依赖: {e}")
                    return None
                except Exception as e:
                    logger.warning(f"[browser-use] 初始化LLM失败: {e}")
                    return None
                
            # 运行异步函数
            import asyncio
            try:
                content = asyncio.run(extract_content())
                if content and len(content) > min_length:
                    logger.info(f"[browser-use] 成功提取内容: {url}")
                    return content
            except Exception as e:
                logger.warning(f"[browser-use] 内容提取失败: {e}")
        except ImportError:
            logger.warning("[browser-use] 未安装，跳过智能内容提取")

    # 2. 用 Playwright headless browser，自动跳转
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=20000)
            time.sleep(2)  # 等待页面渲染和跳转
            for sel in selectors:
                try:
                    node = page.query_selector(sel)
                    if node:
                        text = node.inner_text().strip()
                        if len(text) > min_length:
                            browser.close()
                            logger.info(f"[playwright] 成功提取内容: {url}")
                            return text
                except Exception:
                    continue
            # 兜底：取所有段落拼接
            ps = page.query_selector_all('p')
            text = '\n'.join(p.inner_text().strip() for p in ps if p.inner_text())
            browser.close()
            if len(text) > min_length:
                logger.info(f"[playwright] 成功提取段落内容: {url}")
                return text
    except Exception as e:
        logger.warning(f"[playwright] 正文抓取失败: {e}")
    
    # 3. 降级用 requests + BeautifulSoup
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for sel in selectors:
            node = soup.select_one(sel)
            if node and len(node.get_text(strip=True)) > min_length:
                logger.info(f"[requests] 成功提取内容: {url}")
                return node.get_text(separator='\n', strip=True)
        paragraphs = soup.find_all('p')
        text = '\n'.join(p.get_text(strip=True) for p in paragraphs)
        if len(text) > min_length:
            logger.info(f"[requests] 成功提取段落内容: {url}")
            return text
    except Exception as e:
        logger.warning(f"[requests] 正文抓取失败: {e}")
    
    logger.error(f"所有方法均无法提取内容: {url}")
    return None 