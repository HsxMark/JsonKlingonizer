"""
Reverse Translator
趣味翻译器，将文本反转顺序
"""

from typing import Dict, Any, Optional
from .base_translator import BaseTranslator


class ReverseTranslator(BaseTranslator):
    """反转翻译器，将文本字符顺序颠倒"""

    def translate(self, text: str, source_lang: str = 'auto', target_lang: str = 'en') -> Optional[str]:
        """
        将文本反转

        Args:
            text: 要反转的文本
            source_lang: 源语言代码（此翻译器忽略）
            target_lang: 目标语言代码（此翻译器忽略）

        Returns:
            反转后的文本
        """
        if not text:
            return text

        # 将文本反转
        return text[::-1]

    @staticmethod
    def get_supported_languages() -> Dict[str, str]:
        """
        获取支持的语言列表

        Returns:
            语言代码到语言名称的映射字典
        """
        return {
            'reverse': '反转文本',
        }