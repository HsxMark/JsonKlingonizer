"""
Google Translator
使用 googletrans 库进行翻译（免费，无需 API Key）
"""

from typing import Optional, Dict, Any
import time

from .base_translator import BaseTranslator


class GoogleTranslator(BaseTranslator):
    """Google 翻译器（使用 googletrans 库）"""
    
    def __init__(self, config: Dict[str, Any], cache_manager=None):
        """
        初始化翻译器
        
        Args:
            config: 配置字典
            cache_manager: 缓存管理器实例（可选）
        """
        super().__init__(config, cache_manager)
        
        # 延迟导入，避免未安装时报错
        try:
            from googletrans import Translator
            self.translator = Translator()
            self.available = True
        except ImportError:
            print("⚠️  未安装 googletrans 库")
            print("   请运行: pip install googletrans==4.0.0-rc1")
            self.available = False
            self.translator = None
        
        # 重试配置
        self.max_retries = config.get('api', {}).get('retry', {}).get('max_retries', 3)
        self.backoff_factor = config.get('api', {}).get('retry', {}).get('backoff_factor', 2)
    
    def translate(self, text: str, source_lang: str = 'auto', target_lang: str = 'en') -> Optional[str]:
        """
        翻译单个文本
        
        Args:
            text: 要翻译的文本
            source_lang: 源语言代码（如 'en', 'zh-cn', 'auto'）
            target_lang: 目标语言代码
            
        Returns:
            翻译后的文本，如果失败返回 None
        """
        if not self.available:
            print("❌ Google Translator 不可用")
            return None
        
        # 检查缓存
        if self.cache_manager:
            cache_key = f"{source_lang}:{target_lang}:{text}"
            cached = self.cache_manager.get(cache_key)
            if cached:
                return cached
        
        # 尝试翻译
        for attempt in range(self.max_retries):
            try:
                result = self.translator.translate(
                    text,
                    src=source_lang,
                    dest=target_lang
                )
                
                translated = result.text
                
                # 保存到缓存
                if self.cache_manager:
                    cache_key = f"{source_lang}:{target_lang}:{text}"
                    self.cache_manager.set(cache_key, translated)
                
                return translated
            
            except Exception as e:
                print(f"❌ 翻译异常: {str(e)}")
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
            'zh-cn': '简体中文',
            'zh-tw': '繁体中文',
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
            'th': 'ไทย',
            'id': 'Bahasa Indonesia',
            'hi': 'हिन्दी',
        }
