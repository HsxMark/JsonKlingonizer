"""
工具函数模块
包含缓存管理、日志记录、进度显示等工具
"""

import json
import hashlib
from pathlib import Path
from typing import Optional, Any
from datetime import datetime


class CacheManager:
    """翻译缓存管理器"""
    
    def __init__(self, cache_dir: str = "data/cache"):
        """
        初始化缓存管理器
        
        Args:
            cache_dir: 缓存目录路径
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "translation_cache.json"
        self.cache = self._load_cache()
    
    def _load_cache(self) -> dict:
        """加载缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  加载缓存失败: {e}")
                return {}
        return {}
    
    def _save_cache(self) -> None:
        """保存缓存"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  保存缓存失败: {e}")
    
    def _hash_key(self, text: str) -> str:
        """生成缓存键（使用 MD5 哈希）"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def get(self, text: str) -> Optional[str]:
        """
        从缓存获取翻译
        
        Args:
            text: 原文
            
        Returns:
            翻译结果，如果不存在返回 None
        """
        key = self._hash_key(text)
        if key in self.cache:
            return self.cache[key]['translated']
        return None
    
    def set(self, text: str, translated: str) -> None:
        """
        保存翻译到缓存
        
        Args:
            text: 原文
            translated: 译文
        """
        key = self._hash_key(text)
        self.cache[key] = {
            'original': text,
            'translated': translated,
            'timestamp': datetime.now().isoformat()
        }
        self._save_cache()
    
    def get_stats(self) -> dict:
        """获取缓存统计信息"""
        return {
            'total_entries': len(self.cache),
            'cache_file': str(self.cache_file),
            'cache_size_bytes': self.cache_file.stat().st_size if self.cache_file.exists() else 0
        }
    
    def clear(self) -> None:
        """清空缓存"""
        self.cache = {}
        self._save_cache()
        print("✅ 缓存已清空")


class ProgressTracker:
    """进度跟踪器"""
    
    def __init__(self, total: int, description: str = "处理中"):
        """
        初始化进度跟踪器
        
        Args:
            total: 总数
            description: 描述文本
        """
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = datetime.now()
    
    def update(self, current: int, success_count: int = None) -> None:
        """
        更新进度
        
        Args:
            current: 当前进度
            success_count: 成功数量（可选）
        """
        self.current = current
        percentage = (current / self.total * 100) if self.total > 0 else 0
        
        # 计算预计剩余时间
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if current > 0:
            avg_time = elapsed / current
            remaining = avg_time * (self.total - current)
            eta = f"ETA: {int(remaining)}s"
        else:
            eta = "ETA: N/A"
        
        # 显示进度
        bar_length = 30
        filled = int(bar_length * current / self.total) if self.total > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)
        
        status = f"\r{self.description}: [{bar}] {current}/{self.total} ({percentage:.1f}%)"
        if success_count is not None:
            status += f" | 成功: {success_count}"
        status += f" | {eta}"
        
        print(status, end='', flush=True)
        
        if current >= self.total:
            print()  # 换行
    
    def finish(self) -> None:
        """完成进度"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        print(f"\n✅ 完成！总耗时: {elapsed:.2f}秒")


class Logger:
    """简单的日志记录器"""
    
    def __init__(self, log_file: Optional[str] = None, level: str = "INFO"):
        """
        初始化日志记录器
        
        Args:
            log_file: 日志文件路径（可选）
            level: 日志级别
        """
        self.log_file = Path(log_file) if log_file else None
        self.level = level
        self.levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
    
    def _log(self, level: str, message: str) -> None:
        """记录日志"""
        if self.levels.get(level, 1) >= self.levels.get(self.level, 1):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] [{level}] {message}"
            
            # 输出到控制台
            print(log_message)
            
            # 输出到文件
            if self.log_file:
                try:
                    with open(self.log_file, 'a', encoding='utf-8') as f:
                        f.write(log_message + '\n')
                except Exception as e:
                    print(f"⚠️  写入日志文件失败: {e}")
    
    def debug(self, message: str) -> None:
        """调试日志"""
        self._log("DEBUG", message)
    
    def info(self, message: str) -> None:
        """信息日志"""
        self._log("INFO", message)
    
    def warning(self, message: str) -> None:
        """警告日志"""
        self._log("WARNING", message)
    
    def error(self, message: str) -> None:
        """错误日志"""
        self._log("ERROR", message)


def load_config(config_path: str = "config/config.json") -> dict:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载配置文件失败: {e}")
        return {}


def ensure_dir(dir_path: str) -> None:
    """
    确保目录存在
    
    Args:
        dir_path: 目录路径
    """
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def format_bytes(bytes_size: int) -> str:
    """
    格式化字节大小
    
    Args:
        bytes_size: 字节数
        
    Returns:
        格式化的字符串（如 "1.5 KB"）
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


if __name__ == "__main__":
    # 测试缓存管理器
    print("测试缓存管理器...")
    cache = CacheManager("data/cache")
    cache.set("Hello", "nuqneH")
    print(f"缓存查询 'Hello': {cache.get('Hello')}")
    print(f"缓存统计: {cache.get_stats()}")
    
    # 测试进度跟踪器
    print("\n测试进度跟踪器...")
    import time
    tracker = ProgressTracker(10, "测试进度")
    for i in range(11):
        tracker.update(i, i)
        time.sleep(0.2)
    tracker.finish()
