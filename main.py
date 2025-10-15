#!/usr/bin/env python3
"""
JsonKlingonizer - JSON 值提取、翻译和重建工具
将 JSON 文件中的值提取出来，通过 Klingon API 翻译后重新生成新的语言文件
"""

import argparse
import json
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.extractor import JSONExtractor
from src.translator import KlingonTranslator
from src.rebuilder import JSONRebuilder
from src.utils import CacheManager, ProgressTracker, Logger, load_config, ensure_dir


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='JsonKlingonizer - 将 JSON 值翻译成克林贡语',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  # 基本使用
  python main.py -i data/input/en.json -o data/output/tlh.json
  
  # 使用缓存
  python main.py -i en.json -o tlh.json --use-cache
  
  # 仅提取值到文本文件（用于手动翻译）
  python main.py -i en.json --extract-only -t values.txt
  
  # 从翻译好的文本文件重建 JSON
  python main.py -i en.json -o tlh.json --from-text translated.txt
  
  # 清空翻译缓存
  python main.py --clear-cache
        '''
    )
    
    parser.add_argument('-i', '--input', type=str,
                       help='输入的 JSON 文件路径')
    parser.add_argument('-o', '--output', type=str,
                       help='输出的 JSON 文件路径')
    parser.add_argument('-c', '--config', type=str, default='config/config.json',
                       help='配置文件路径 (默认: config/config.json)')
    parser.add_argument('--use-cache', action='store_true',
                       help='使用翻译缓存')
    parser.add_argument('--clear-cache', action='store_true',
                       help='清空翻译缓存并退出')
    parser.add_argument('--extract-only', action='store_true',
                       help='仅提取值到文本文件，不翻译')
    parser.add_argument('-t', '--text-file', type=str,
                       help='文本文件路径（用于提取或导入）')
    parser.add_argument('--from-text', type=str,
                       help='从翻译好的文本文件导入')
    parser.add_argument('--log-file', type=str,
                       help='日志文件路径')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='显示详细信息')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    if not config:
        print("❌ 无法加载配置文件，使用默认配置")
        config = {
            'api': {
                'base_url': 'https://api.funtranslations.com/translate/klingon.json',
                'rate_limit': {'requests_per_hour': 5, 'requests_per_day': 60, 'wait_on_limit': True},
                'retry': {'max_retries': 3, 'backoff_factor': 2}
            },
            'processing': {'use_cache': True, 'cache_dir': 'data/cache'},
            'logging': {'level': 'INFO', 'show_progress': True}
        }
    
    # 初始化日志
    log_level = 'DEBUG' if args.verbose else config['logging'].get('level', 'INFO')
    logger = Logger(args.log_file, log_level)
    
    # 清空缓存
    if args.clear_cache:
        cache_dir = config['processing'].get('cache_dir', 'data/cache')
        cache_manager = CacheManager(cache_dir)
        cache_manager.clear()
        return 0
    
    # 检查必需参数
    if not args.input:
        parser.print_help()
        return 1
    
    # 确保输出目录存在
    if args.output:
        ensure_dir(Path(args.output).parent)
    
    try:
        # ============= 提取阶段 =============
        logger.info(f"📖 正在读取 JSON 文件: {args.input}")
        extractor = JSONExtractor()
        original_json, values = extractor.extract_from_file(args.input)
        logger.info(f"✅ 提取了 {len(values)} 个字符串值")
        
        # 仅提取模式
        if args.extract_only:
            if not args.text_file:
                logger.error("❌ 使用 --extract-only 时必须指定 --text-file")
                return 1
            
            line_separator = config['processing'].get('line_separator', '~')
            logger.info(f"💾 正在导出到文本文件: {args.text_file}")
            logger.info(f"💡 使用行分隔符: '{line_separator}' (翻译后请保留此符号)")
            extractor.export_to_text(args.text_file, line_separator)
            logger.info(f"✅ 已导出到 {args.text_file}")
            logger.info(f"💡 每行末尾的 '{line_separator}' 符号用于标记换行，翻译时请保留它")
            logger.info("💡 翻译完成后使用 --from-text 导入")
            return 0
        
        # ============= 翻译阶段 =============
        if args.from_text:
            # 从文本文件导入翻译
            logger.info(f"📖 正在从文本文件导入翻译: {args.from_text}")
            line_separator = config['processing'].get('line_separator', '~')
            
            with open(args.from_text, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 使用行分隔符分割文本，而不是按换行符
            # 这样即使翻译后所有文本都在一行，也能正确分割
            translated_lines = content.split(line_separator)
            
            # 移除最后一个元素，如果它只是文件末尾的空白
            # 但要保留中间的空字符串（因为某些原始值可能就是空的）
            if translated_lines and translated_lines[-1].strip() == '':
                translated_lines = translated_lines[:-1]
            
            # 去除每个条目两端的换行符，但保留空字符串
            translated_lines = [line.strip('\n\r') for line in translated_lines]
            
            if len(translated_lines) != len(values):
                logger.error(f"❌ 文本条目数 ({len(translated_lines)}) 与提取的值数量 ({len(values)}) 不匹配")
                logger.error(f"💡 提示：请确保翻译时保留了每行末尾的 '{line_separator}' 分隔符")
                logger.info(f"📊 调试信息：提取了 {len(values)} 个值，导入了 {len(translated_lines)} 个条目")
                return 1
            
            for i, translated_text in enumerate(translated_lines):
                # 直接使用分割后的文本
                values[i]['translated'] = translated_text
            
            logger.info(f"✅ 已导入 {len(values)} 个翻译值")
        
        else:
            # 使用 API 翻译
            logger.info("🌐 开始翻译...")
            
            # 初始化缓存管理器
            cache_manager = None
            if args.use_cache or config['processing'].get('use_cache', True):
                cache_dir = config['processing'].get('cache_dir', 'data/cache')
                cache_manager = CacheManager(cache_dir)
                stats = cache_manager.get_stats()
                logger.info(f"💾 缓存状态: {stats['total_entries']} 条记录")
            
            # 初始化翻译器
            translator = KlingonTranslator(config, cache_manager)
            
            # 进度跟踪
            if config['logging'].get('show_progress', True):
                tracker = ProgressTracker(len(values), "翻译进度")
                
                def progress_callback(current, total, success_count):
                    tracker.update(current, success_count)
                
                values = translator.translate_batch(values, progress_callback)
                tracker.finish()
            else:
                values = translator.translate_batch(values)
            
            # 统计翻译结果
            translated_count = sum(1 for v in values if v.get('translated') and v['translated'] != v['original'])
            logger.info(f"✅ 翻译完成: {translated_count}/{len(values)} 个值已翻译")
        
        # ============= 重建阶段 =============
        if not args.output:
            logger.error("❌ 必须指定输出文件 (-o/--output)")
            return 1
        
        logger.info("🔨 正在重建 JSON...")
        rebuilder = JSONRebuilder(original_json)
        translated_json = rebuilder.rebuild(values)
        
        # 保存到文件
        logger.info(f"💾 正在保存到: {args.output}")
        rebuilder.save_to_file(translated_json, args.output, indent=2, ensure_ascii=False)
        
        logger.info(f"🎉 完成！翻译后的文件已保存到: {args.output}")
        
        return 0
    
    except KeyboardInterrupt:
        logger.warning("\n⚠️  用户中断")
        return 130
    
    except Exception as e:
        logger.error(f"❌ 发生错误: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
