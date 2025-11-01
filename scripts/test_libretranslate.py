#!/usr/bin/env python3
"""
LibreTranslate 连接测试脚本
"""

import json
import sys
import requests
from typing import Dict, Any

def test_connection(url: str = "http://localhost:5000") -> bool:
    """测试 LibreTranslate 连接"""
    try:
        print(f"正在测试连接: {url}")
        response = requests.get(f"{url}/languages", timeout=5)
        
        if response.status_code == 200:
            languages = response.json()
            print(f"✅ 连接成功！")
            print(f"   支持 {len(languages)} 种语言")
            return True
        else:
            print(f"❌ 连接失败 (状态码: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到 {url}")
        print(f"   请确保 LibreTranslate 正在运行")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_translation(url: str = "http://localhost:5000", 
                    text: str = "Hello, World!",
                    source: str = "en",
                    target: str = "zh") -> bool:
    """测试翻译功能"""
    try:
        print(f"\n正在测试翻译...")
        print(f"   原文 ({source}): {text}")
        
        response = requests.post(
            f"{url}/translate",
            json={
                "q": text,
                "source": source,
                "target": target,
                "format": "text"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            translated = result.get("translatedText", "")
            print(f"   译文 ({target}): {translated}")
            print(f"✅ 翻译成功！")
            return True
        else:
            print(f"❌ 翻译失败 (状态码: {response.status_code})")
            print(f"   响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 翻译错误: {e}")
        return False

def list_languages(url: str = "http://localhost:5000") -> None:
    """列出支持的语言"""
    try:
        response = requests.get(f"{url}/languages", timeout=5)
        if response.status_code == 200:
            languages = response.json()
            print(f"\n支持的语言列表:")
            for lang in languages:
                code = lang.get("code", "")
                name = lang.get("name", "")
                print(f"   - {code}: {name}")
    except Exception as e:
        print(f"❌ 获取语言列表失败: {e}")

def main():
    print("=" * 60)
    print("LibreTranslate 连接测试")
    print("=" * 60)
    print()
    
    # 默认 URL
    url = "http://localhost:5000"
    
    # 允许命令行参数指定 URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    # 测试连接
    if not test_connection(url):
        print()
        print("💡 提示:")
        print("   1. 确保已启动 LibreTranslate:")
        print("      bash scripts/deploy_libretranslate.sh")
        print()
        print("   2. 检查容器状态:")
        print("      docker ps | grep libretranslate")
        print()
        print("   3. 查看日志:")
        print("      docker logs libretranslate")
        print()
        sys.exit(1)
    
    # 测试翻译
    print()
    tests = [
        ("Hello, World!", "en", "zh"),
        ("你好，世界！", "zh", "en"),
        ("こんにちは", "ja", "en"),
    ]
    
    success = 0
    for text, source, target in tests:
        if test_translation(url, text, source, target):
            success += 1
        print()
    
    # 列出支持的语言
    list_languages(url)
    
    print()
    print("=" * 60)
    print(f"测试完成: {success}/{len(tests)} 通过")
    print("=" * 60)
    print()
    
    if success == len(tests):
        print("✅ LibreTranslate 工作正常！")
        print()
        print("🎯 下一步:")
        print("   1. 更新配置文件 config/config.json:")
        print('      {"translator": {"type": "libre"}}')
        print()
        print("   2. 开始翻译:")
        print("      python main.py -i input.json -o output.json \\")
        print("        --translator libre --source en --target zh --use-cache")
        print()
    else:
        print("⚠️  部分测试失败")
        print("   LibreTranslate 可能仍在初始化中，请稍后重试")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  测试中断")
        sys.exit(130)
