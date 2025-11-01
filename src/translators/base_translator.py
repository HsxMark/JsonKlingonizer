"""
Base Translator
翻译器基类，定义翻译器的通用接口
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import re


class BaseTranslator(ABC):
    """翻译器基类"""
    
    def __init__(self, config: Dict[str, Any], cache_manager=None):
        """
        初始化翻译器
        
        Args:
            config: 配置字典
            cache_manager: 缓存管理器实例（可选）
        """
        self.config = config
        self.cache_manager = cache_manager
    
    @abstractmethod
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
        pass
    
    def translate_batch(self, values: List[Dict[str, Any]], 
                       source_lang: str = 'auto',
                       target_lang: str = 'en',
                       progress_callback=None) -> List[Dict[str, Any]]:
        """
        批量翻译
        
        Args:
            values: 值列表（包含 'original' 字段）
            source_lang: 源语言代码
            target_lang: 目标语言代码
            progress_callback: 进度回调函数
            
        Returns:
            翻译后的值列表（包含 'translated' 字段）
        """
        total = len(values)
        translated_count = 0
        skipped_count = 0
        
        # 第一步：处理缓存和跳过不需要翻译的项
        need_translation = []
        need_translation_indices = []
        
        for idx, item in enumerate(values):
            original = item['original']
            
            # 检查是否应该跳过翻译
            if self._should_skip_translation(original):
                item['translated'] = original
                skipped_count += 1
                continue
            
            # 检查缓存
            if self.cache_manager:
                cache_key = f"{source_lang}:{target_lang}:{original}"
                cached = self.cache_manager.get(cache_key)
                if cached:
                    item['translated'] = cached
                    translated_count += 1
                    continue
            
            # 需要翻译
            need_translation.append(original)
            need_translation_indices.append(idx)
        
        if skipped_count > 0:
            print(f"💡 跳过了 {skipped_count} 个不需要翻译的项（版本号、数字等）")
        
        if not need_translation:
            print(f"✅ 所有内容都已在缓存中或无需翻译！")
            return values
        
        print(f"📝 需要翻译 {len(need_translation)} 个新文本")
        
        # 第二步：逐个翻译
        for i, idx in enumerate(need_translation_indices):
            original = need_translation[i]
            translated = self.translate(original, source_lang, target_lang)
            
            if translated:
                values[idx]['translated'] = translated
                translated_count += 1
                
                # 保存到缓存
                if self.cache_manager:
                    cache_key = f"{source_lang}:{target_lang}:{original}"
                    self.cache_manager.set(cache_key, translated)
            else:
                values[idx]['translated'] = original
                print(f"⚠️  翻译失败，保留原文: {original[:50]}...")
            
            if progress_callback:
                progress_callback(idx + 1, total, translated_count)
        
        return values
    
    def _should_skip_translation(self, text: str) -> bool:
        """
        判断是否应该跳过翻译（如版本号、数字、ID等）
        
        Args:
            text: 要检查的文本
            
        Returns:
            True 表示应该跳过翻译
        """
        text = text.strip()
        
        # 跳过空字符串
        if not text:
            return True
        
        # 跳过纯数字
        if text.replace('.', '').replace('-', '').replace('_', '').isdigit():
            return True
        
        # 跳过版本号格式 (如 1.0.0, v1.2.3)
        if re.match(r'^v?\d+(\.\d+)*$', text, re.IGNORECASE):
            return True
        
        # 跳过纯数字 ID
        if re.match(r'^\d+$', text):
            return True
        
        # 跳过 URL
        if text.startswith(('http://', 'https://', 'ftp://', 'www.')):
            return True
        
        # 跳过 Email
        if '@' in text and '.' in text:
            return True
        
        # 跳过很短的文本（可能是代码或缩写）
        if len(text) <= 2 and text.isupper():
            return True
        
        return False
    
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
        }
