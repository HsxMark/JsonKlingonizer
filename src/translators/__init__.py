"""
翻译器模块
支持多种翻译服务
"""

from .base_translator import BaseTranslator
from .klingon_translator import KlingonTranslator
from .googletrans_translator import GoogleTranslator
from .libre_translator import LibreTranslator

__all__ = [
    'BaseTranslator',
    'KlingonTranslator', 
    'GoogleTranslator',
    'LibreTranslator',
]
