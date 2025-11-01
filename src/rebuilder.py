"""
JSON Rebuilder
将翻译后的值重新组装成 JSON 文件
"""

import json
import copy
from typing import Dict, List, Any, Union


class JSONRebuilder:
    """JSON 重建器"""
    
    def __init__(self, original_json: Any):
        """
        初始化重建器
        
        Args:
            original_json: 原始 JSON 数据结构
        """
        self.original_json = original_json
    
    def rebuild(self, translated_values: List[Dict[str, Any]], 
                partial_update: bool = False, 
                filter_keyword: str = None) -> Any:
        """
        使用翻译后的值重建 JSON
        
        Args:
            translated_values: 包含路径和翻译值的列表
            partial_update: 是否为部分更新模式（只更新提供的值）
            filter_keyword: 过滤关键词（用于在部分更新时去除关键词）
            
        Returns:
            重建后的 JSON 对象
        """
        # 深拷贝原始结构
        result = copy.deepcopy(self.original_json)
        
        # 替换所有值
        for item in translated_values:
            path = item['path']
            translated = item.get('translated', item['original'])
            
            # 如果是部分更新模式且有过滤关键词，需要移除关键词
            if partial_update and filter_keyword and translated:
                # 移除关键词（如 %TODO ）
                translated = translated.replace(filter_keyword, '').strip()
            
            self._set_value_by_path(result, path, translated)
        
        return result
    
    def _set_value_by_path(self, obj: Any, path: str, value: str) -> None:
        """
        根据路径设置值
        
        Args:
            obj: JSON 对象
            path: 路径字符串（如 "user.name" 或 "items[0].title"）
            value: 要设置的值
        """
        if not path:
            return
        
        # 解析路径
        parts = self._parse_path(path)
        
        # 遍历到倒数第二个元素
        current = obj
        for part in parts[:-1]:
            if isinstance(part, int):
                current = current[part]
            else:
                current = current[part]
        
        # 设置最后一个元素的值
        last_part = parts[-1]
        if isinstance(last_part, int):
            current[last_part] = value
        else:
            current[last_part] = value
    
    def _parse_path(self, path: str) -> List[Union[str, int]]:
        """
        解析路径字符串为部分列表
        
        Args:
            path: 路径字符串（如 "user.name" 或 "items[0].title"）
            
        Returns:
            路径部分列表，数组索引为整数
        
        Examples:
            "user.name" -> ["user", "name"]
            "items[0].title" -> ["items", 0, "title"]
            "data.list[2].nested[1].value" -> ["data", "list", 2, "nested", 1, "value"]
        """
        parts = []
        current = ""
        i = 0
        
        while i < len(path):
            char = path[i]
            
            if char == '.':
                if current:
                    parts.append(current)
                    current = ""
            elif char == '[':
                if current:
                    parts.append(current)
                    current = ""
                # 提取数组索引
                j = i + 1
                while j < len(path) and path[j] != ']':
                    j += 1
                index = int(path[i+1:j])
                parts.append(index)
                i = j  # 跳过 ']'
            else:
                current += char
            
            i += 1
        
        if current:
            parts.append(current)
        
        return parts
    
    def save_to_file(self, json_obj: Any, output_path: str, 
                     indent: int = 2, ensure_ascii: bool = False) -> None:
        """
        将 JSON 对象保存到文件
        
        Args:
            json_obj: JSON 对象
            output_path: 输出文件路径
            indent: 缩进空格数
            ensure_ascii: 是否转义非 ASCII 字符
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_obj, f, indent=indent, ensure_ascii=ensure_ascii)


def rebuild_json(original_json: Any, translated_values: List[Dict[str, Any]], 
                 partial_update: bool = False, filter_keyword: str = None) -> Any:
    """
    便捷函数：重建 JSON
    
    Args:
        original_json: 原始 JSON 数据
        translated_values: 翻译后的值列表
        partial_update: 是否为部分更新模式
        filter_keyword: 过滤关键词
        
    Returns:
        重建后的 JSON 对象
    """
    rebuilder = JSONRebuilder(original_json)
    return rebuilder.rebuild(translated_values, partial_update, filter_keyword)


if __name__ == "__main__":
    # 测试代码
    test_json = {
        "app": {
            "name": "My App",
            "version": "1.0.0"
        },
        "messages": [
            "Hello",
            "World"
        ]
    }
    
    test_values = [
        {"path": "app.name", "original": "My App", "translated": "wIj App"},
        {"path": "app.version", "original": "1.0.0", "translated": "1.0.0"},
        {"path": "messages[0]", "original": "Hello", "translated": "nuqneH"},
        {"path": "messages[1]", "original": "World", "translated": "qo'"}
    ]
    
    rebuilder = JSONRebuilder(test_json)
    result = rebuilder.rebuild(test_values)
    
    print("原始 JSON:")
    print(json.dumps(test_json, indent=2, ensure_ascii=False))
    print("\n重建后的 JSON:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
