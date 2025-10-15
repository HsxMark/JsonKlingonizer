"""
JSON Value Extractor
提取 JSON 文件中的所有字符串值，保留路径信息以便后续重建
"""

import json
from typing import Dict, List, Any, Union


class JSONExtractor:
    """JSON 值提取器"""
    
    def __init__(self):
        self.values = []
    
    def extract_from_file(self, file_path: str) -> tuple:
        """
        从文件中提取 JSON 值
        
        Args:
            file_path: JSON 文件路径
            
        Returns:
            (原始JSON对象, 提取的值列表)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        self.values = []
        self._extract_recursive(json_data, "")
        
        return json_data, self.values
    
    def _extract_recursive(self, obj: Any, path: str) -> None:
        """
        递归提取 JSON 中的所有字符串值
        
        Args:
            obj: JSON 对象（可能是 dict, list, str 等）
            path: 当前值的路径（用于后续重建）
        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                self._extract_recursive(value, new_path)
                
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                new_path = f"{path}[{idx}]"
                self._extract_recursive(item, new_path)
                
        elif isinstance(obj, str):
            # 只提取字符串类型的值
            self.values.append({
                "path": path,
                "original": obj,
                "translated": None  # 将在翻译后填充
            })
    
    def export_to_text(self, output_path: str, line_separator: str = "~") -> None:
        """
        将提取的值导出为纯文本文件（每行一个值）
        用于手动翻译
        
        Args:
            output_path: 输出文本文件路径
            line_separator: 行分隔符（默认为 "~"），用于标记每行结尾，翻译后可以正确分割
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in self.values:
                # 不再转义换行符，而是在末尾添加分隔符
                # 这样即使文本被翻译成一行，也能通过分隔符正确还原
                f.write(f"{item['original']}{line_separator}\n")
    
    def get_values(self) -> List[Dict[str, Any]]:
        """获取提取的值列表"""
        return self.values
    
    def get_text_list(self) -> List[str]:
        """获取纯文本值列表（仅值，不含路径信息）"""
        return [item['original'] for item in self.values]


def extract_json_values(file_path: str) -> tuple:
    """
    便捷函数：从 JSON 文件提取值
    
    Args:
        file_path: JSON 文件路径
        
    Returns:
        (原始JSON对象, 提取的值列表)
    """
    extractor = JSONExtractor()
    return extractor.extract_from_file(file_path)


if __name__ == "__main__":
    # 测试代码
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python extractor.py <json文件路径>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    extractor = JSONExtractor()
    original_json, values = extractor.extract_from_file(input_file)
    
    print(f"从 {input_file} 提取了 {len(values)} 个字符串值：")
    for idx, item in enumerate(values[:5], 1):  # 只显示前5个
        print(f"{idx}. [{item['path']}] = \"{item['original']}\"")
    
    if len(values) > 5:
        print(f"... 还有 {len(values) - 5} 个值")
