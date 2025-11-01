"""
LibreTranslate Translator
使用 LibreTranslate API 进行翻译（开源、可自托管）
"""

import requests
import time
from typing import Optional, Dict, Any

from .base_translator import BaseTranslator


class LibreTranslator(BaseTranslator):
    """LibreTranslate 翻译器"""
    
    def __init__(self, config: Dict[str, Any], cache_manager=None):
        """
        初始化翻译器
        
        Args:
            config: 配置字典
            cache_manager: 缓存管理器实例（可选）
        """
        super().__init__(config, cache_manager)
        
        # LibreTranslate API 配置
        self.api_url = config.get('api', {}).get('libre_url', 'https://libretranslate.com/translate')
        self.api_key = config.get('api', {}).get('libre_api_key', None)
        
        # 重试配置
        self.max_retries = config.get('api', {}).get('retry', {}).get('max_retries', 3)
        self.backoff_factor = config.get('api', {}).get('retry', {}).get('backoff_factor', 2)
    
    def translate(self, text: str, source_lang: str = 'auto', target_lang: str = 'en') -> Optional[str]:
        """
        翻译单个文本
        
        Args:
            text: 要翻译的文本
            source_lang: 源语言代码（如 'en', 'zh', 'auto'）
            target_lang: 目标语言代码
            
        Returns:
            翻译后的文本，如果失败返回 None
        """
        # 检查缓存
        if self.cache_manager:
            cache_key = f"{source_lang}:{target_lang}:{text}"
            cached = self.cache_manager.get(cache_key)
            if cached:
                return cached
        
        # LibreTranslate 使用 'zh' 而不是 'zh-cn'
        if source_lang == 'zh-cn' or source_lang == 'zh-tw':
            source_lang = 'zh'
        if target_lang == 'zh-cn' or target_lang == 'zh-tw':
            target_lang = 'zh'
        
        # 尝试翻译
        for attempt in range(self.max_retries):
            try:
                payload = {
                    'q': text,
                    'source': source_lang,
                    'target': target_lang,
                    'format': 'text'
                }
                
                # 如果有 API Key，添加到请求中
                if self.api_key:
                    payload['api_key'] = self.api_key
                
                response = requests.post(
                    self.api_url,
                    json=payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    translated = data.get('translatedText', '')
                    
                    # 保存到缓存
                    if self.cache_manager:
                        cache_key = f"{source_lang}:{target_lang}:{text}"
                        self.cache_manager.set(cache_key, translated)
                    
                    return translated
                
                else:
                    print(f"❌ API 错误 {response.status_code}: {response.text}")
                    if attempt < self.max_retries - 1:
                        wait_time = self.backoff_factor ** attempt
                        print(f"   等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                    else:
                        return None
            
            except Exception as e:
                print(f"❌ 请求异常: {str(e)}")
                if attempt < self.max_retries - 1:
                    wait_time = self.backoff_factor ** attempt
                    print(f"   等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    return None
        
        return None
    
    @staticmethod
    def get_supported_languages() -> Dict[str, str]:
        """
        获取支持的语言列表
        
        Returns:
            语言代码到语言名称的映射字典
        """
        return {
            'auto': '自动检测',
            'en': 'English',
            'zh': '中文',
            'ja': '日本語',
            'ko': '한국어',
            'fr': 'Français',
            'de': 'Deutsch',
            'es': 'Español',
            'ru': 'Русский',
            'ar': 'العربية',
            'pt': 'Português',
            'it': 'Italiano',
            'nl': 'Nederlands',
            'pl': 'Polski',
            'tr': 'Türkçe',
            'vi': 'Tiếng Việt',
            'hi': 'हिन्दी',
        }
