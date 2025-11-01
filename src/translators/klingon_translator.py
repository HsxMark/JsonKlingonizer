"""
Klingon Translator
调用 Fun Translations API 进行克林贡语翻译
包含速率限制、重试机制和缓存支持
"""

import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .base_translator import BaseTranslator


class KlingonTranslator(BaseTranslator):
    """克林贡语翻译器"""
    
    def __init__(self, config: Dict[str, Any], cache_manager=None):
        """
        初始化翻译器
        
        Args:
            config: 配置字典
            cache_manager: 缓存管理器实例（可选）
        """
        super().__init__(config, cache_manager)
        self.api_url = config['api']['base_url']
        
        # 速率限制
        self.requests_per_hour = config['api']['rate_limit']['requests_per_hour']
        self.requests_per_day = config['api']['rate_limit']['requests_per_day']
        self.wait_on_limit = config['api']['rate_limit']['wait_on_limit']
        
        # 重试配置
        self.max_retries = config['api']['retry']['max_retries']
        self.backoff_factor = config['api']['retry']['backoff_factor']
        
        # 请求计数
        self.hourly_requests = []
        self.daily_requests = []
    
    def translate(self, text: str, source_lang: str = 'auto', target_lang: str = 'klingon') -> Optional[str]:
        """
        翻译单个文本为克林贡语
        
        Args:
            text: 要翻译的文本
            source_lang: 源语言（克林贡API忽略此参数）
            target_lang: 目标语言（克林贡API忽略此参数）
            
        Returns:
            翻译后的文本，如果失败返回 None
        """
        # 检查缓存
        if self.cache_manager:
            cached = self.cache_manager.get(text)
            if cached:
                return cached
        
        # 检查速率限制
        self._check_rate_limit()
        
        # 尝试翻译
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    self.api_url,
                    params={'text': text},
                    timeout=30
                )
                
                # 记录请求
                self._record_request()
                
                if response.status_code == 200:
                    data = response.json()
                    translated = data['contents']['translated']
                    
                    # 保存到缓存
                    if self.cache_manager:
                        self.cache_manager.set(text, translated)
                    
                    return translated
                
                elif response.status_code == 429:
                    # 速率限制
                    self._handle_rate_limit(response)
                    if attempt < self.max_retries - 1:
                        continue
                    else:
                        print(f"⚠️  达到最大重试次数，跳过: {text[:50]}...")
                        return None
                
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
    
    def translate_batch(self, values: List[Dict[str, Any]], 
                       source_lang: str = 'auto',
                       target_lang: str = 'klingon',
                       progress_callback=None) -> List[Dict[str, Any]]:
        """
        批量翻译（合并多个文本为一次 API 调用）
        
        Args:
            values: 值列表（包含 'original' 字段）
            source_lang: 源语言（克林贡API忽略此参数）
            target_lang: 目标语言（克林贡API忽略此参数）
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
                cached = self.cache_manager.get(original)
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
        print(f"⚠️  注意：免费 API 限制为每小时 5 次请求，建议使用手动翻译模式")
        print(f"   提示：使用 --extract-only 导出文本，手动翻译后用 --from-text 导入")
        
        # 第二步：批量翻译（将多个文本合并）
        # 使用分隔符合并文本
        separator = " ||| "
        merged_text = separator.join(need_translation)
        
        print(f"\n🔄 尝试批量翻译 {len(need_translation)} 个文本...")
        print(f"   合并后长度: {len(merged_text)} 字符")
        
        # 尝试一次性翻译所有文本
        translated_merged = self.translate(merged_text)
        
        if translated_merged:
            # 分割翻译结果
            translated_parts = translated_merged.split(separator)
            
            # 如果分割后的数量匹配
            if len(translated_parts) == len(need_translation):
                for i, idx in enumerate(need_translation_indices):
                    values[idx]['translated'] = translated_parts[i].strip()
                    translated_count += 1
                
                print(f"✅ 批量翻译成功！")
            else:
                # 分割失败，回退到逐个翻译
                print(f"⚠️  批量翻译分割失败，回退到逐个翻译...")
                for i, idx in enumerate(need_translation_indices):
                    original = need_translation[i]
                    translated = self.translate(original)
                    
                    if translated:
                        values[idx]['translated'] = translated
                        translated_count += 1
                    else:
                        values[idx]['translated'] = original
                        print(f"⚠️  翻译失败，保留原文: {original[:50]}...")
                    
                    if progress_callback:
                        progress_callback(idx + 1, total, translated_count)
        else:
            # 批量翻译失败，回退到逐个翻译
            print(f"⚠️  批量翻译失败，回退到逐个翻译...")
            for i, idx in enumerate(need_translation_indices):
                original = need_translation[i]
                translated = self.translate(original)
                
                if translated:
                    values[idx]['translated'] = translated
                    translated_count += 1
                else:
                    values[idx]['translated'] = original
                    print(f"⚠️  翻译失败，保留原文: {original[:50]}...")
                
                if progress_callback:
                    progress_callback(idx + 1, total, translated_count)
        
        return values
    
    def _check_rate_limit(self) -> None:
        """检查是否超过速率限制，如果超过则等待"""
        now = datetime.now()
        
        # 清理过期的请求记录
        self.hourly_requests = [
            req_time for req_time in self.hourly_requests 
            if now - req_time < timedelta(hours=1)
        ]
        self.daily_requests = [
            req_time for req_time in self.daily_requests 
            if now - req_time < timedelta(days=1)
        ]
        
        # 检查小时限制
        if len(self.hourly_requests) >= self.requests_per_hour:
            if self.wait_on_limit:
                wait_until = self.hourly_requests[0] + timedelta(hours=1)
                wait_seconds = (wait_until - now).total_seconds()
                if wait_seconds > 0:
                    print(f"⏳ 达到小时限制，等待 {wait_seconds:.0f} 秒...")
                    time.sleep(wait_seconds + 1)
                    self._check_rate_limit()  # 递归检查
            else:
                raise Exception("已达到每小时请求限制")
        
        # 检查每日限制
        if len(self.daily_requests) >= self.requests_per_day:
            if self.wait_on_limit:
                wait_until = self.daily_requests[0] + timedelta(days=1)
                wait_seconds = (wait_until - now).total_seconds()
                if wait_seconds > 0:
                    print(f"⏳ 达到每日限制，等待 {wait_seconds:.0f} 秒...")
                    time.sleep(wait_seconds + 1)
                    self._check_rate_limit()  # 递归检查
            else:
                raise Exception("已达到每日请求限制")
    
    def _record_request(self) -> None:
        """记录一次请求"""
        now = datetime.now()
        self.hourly_requests.append(now)
        self.daily_requests.append(now)
    
    def _handle_rate_limit(self, response: requests.Response) -> None:
        """处理 API 返回的速率限制"""
        # 尝试从响应头获取重试时间
        retry_after = response.headers.get('Retry-After')
        if retry_after:
            wait_seconds = int(retry_after)
        else:
            # 默认等待1小时
            wait_seconds = 3600
        
        print(f"⏳ API 速率限制，等待 {wait_seconds} 秒...")
        if self.wait_on_limit:
            time.sleep(wait_seconds)
        else:
            raise Exception("API 速率限制")
