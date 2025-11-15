"""
Flip Translator
趣味翻译器,将英文字符翻转成上下颠倒的样子
"""

import re
from typing import Dict, Any, Optional
from .base_translator import BaseTranslator


class FlipTranslator(BaseTranslator):
    """字符翻转翻译器，将英文字符转换为上下颠倒的Unicode字符"""

    # 字符映射表：正常字符 -> 翻转后的字符
    FLIP_MAP = {
        'a': 'ɐ',
        'b': 'q',
        'c': 'ɔ',
        'd': 'p',
        'e': 'ǝ',
        'f': 'ɟ',
        'g': 'ᵷ',
        'h': 'ɥ',
        'i': 'ᴉ',
        'j': 'ɾ',
        'k': 'ʞ',
        'l': 'ꞁ',
        'm': 'ɯ',
        'n': 'u',
        'o': 'o',
        'p': 'd',
        'q': 'b',
        'r': 'ɹ',
        's': 's',
        't': 'ʇ',
        'u': 'n',
        'v': 'ʌ',
        'w': 'ʍ',
        'x': 'x',
        'y': 'ʎ',
        'z': 'z',
        'A': 'Ɐ',
        'B': 'ᗺ',
        'C': 'Ɔ',
        'D': 'ᗡ',
        'E': 'Ǝ',
        'F': 'Ⅎ',
        'G': '⅁',
        'H': 'H',
        'I': 'I',
        'J': 'ſ',
        'K': 'ʞ',
        'L': 'Ꞁ',
        'M': 'W',
        'N': 'N',
        'O': 'O',
        'P': 'Ԁ',
        'Q': 'Ὂ',
        'R': 'ᴚ',
        'S': 'S',
        'T': '⟘',
        'U': '∩',
        'V': 'Λ',
        'W': 'M',
        'X': 'X',
        'Y': 'ʎ',
        'Z': 'Z',
        '0': '0',
        '1': 'Ɩ',
        '2': 'ᘔ',
        '3': 'Ɛ',
        '4': 'ㄣ',
        '5': 'ϛ',
        '6': '9',
        '7': 'ㄥ',
        '8': '8',
        '9': '6',
        '_': '‾',
        ',': '\'',
        ';': '⸵',
        '.': '˙',
        '?': '¿',
        '!': '¡',
        '/': '/',
        '\\': '\\',
        '\'': ',',
        '(': ')',
        ')': '(',
        '[': ']',
        ']': '[',
        '{': '}',
        '}': '{',
    }

    def translate(self, text: str, source_lang: str = 'auto', target_lang: str = 'en') -> Optional[str]:
        """
        将文本中的英文字符翻转为上下颠倒的样子

        Args:
            text: 要翻转的文本
            source_lang: 源语言代码（此翻译器忽略）
            target_lang: 目标语言代码（此翻译器忽略）

        Returns:
            翻转后的文本（字符被替换为上下颠倒的Unicode字符）
        """
        if not text:
            return text

        # 提取所有模板变量（如 {{variable}}、{variable}、%s、%d 等）
        placeholders = []
        placeholder_pattern = r'\{\{[^}]+\}\}|\{[^}]+\}|%[sd]|%\([^)]+\)[sd]'
        
        # 替换模板变量为临时占位符
        def save_placeholder(match):
            placeholders.append(match.group(0))
            return f'\x00{len(placeholders)-1}\x00'
        
        protected_text = re.sub(placeholder_pattern, save_placeholder, text)
        
        # 将每个字符替换为对应的翻转字符
        flipped_chars = []
        for char in protected_text:
            # 跳过占位符标记
            if char == '\x00':
                flipped_chars.append(char)
            # 如果字符在映射表中，使用映射后的字符
            elif char in self.FLIP_MAP:
                flipped_chars.append(self.FLIP_MAP[char])
            else:
                # 否则保持原样（如中文、空格等）
                flipped_chars.append(char)
        
        # 将翻转后的字符串再反转顺序（这样看起来像倒置的文本）
        reversed_text = ''.join(reversed(flipped_chars))
        
        # 恢复模板变量（注意：因为字符串已经反转，占位符的位置也反转了）
        def restore_placeholder(match):
            idx = int(match.group(1))
            return placeholders[idx]
        
        result = re.sub(r'\x00(\d+)\x00', restore_placeholder, reversed_text)
        
        return result

    @staticmethod
    def get_supported_languages() -> Dict[str, str]:
        """
        获取支持的语言列表

        Returns:
            语言代码到语言名称的映射字典
        """
        return {
            'flip': '上下翻转文本（英文字符）',
        }
