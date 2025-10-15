# JsonKlingonizer 🖖

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个 JSON 值提取、翻译和重建工具，可以将 JSON 文件中的所有文本值提取出来，通过 [Fun Translations Klingon API](https://funtranslations.com/klingon) 翻译成克林贡语（或其他语言），然后重新生成新的语言版本 JSON 文件。

## ✨ 特性

- 🔍 **智能提取**：递归提取 JSON 中的所有字符串值，保留完整路径信息
- 🌐 **API 翻译**：集成 Fun Translations API 进行自动翻译
- 💾 **缓存机制**：自动缓存翻译结果，避免重复调用 API
- ⚡ **速率控制**：智能处理 API 速率限制（每小时 5 次，每天 60 次）
- 🔄 **断点续传**：支持中断后继续翻译
- 📝 **手动模式**：支持导出纯文本，手动翻译后再导入
- 🎯 **精确重建**：保持原 JSON 结构，仅替换文本值
- 📊 **进度显示**：实时显示翻译进度和预计完成时间

## 📦 安装

### 1. 克隆仓库

```bash
git clone https://github.com/HsxMark/JsonKlingonizer.git
cd JsonKlingonizer
```

### 2. 创建虚拟环境（推荐）

使用 Python 虚拟环境可以避免依赖冲突：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 在 Windows 上使用: venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 🚀 快速开始

### 基本使用

```bash
# 翻译 JSON 文件
python main.py -i data/input/en.json -o data/output/tlh.json
```

### 使用缓存（推荐）

```bash
# 启用缓存可以避免重复翻译相同的文本
python main.py -i data/input/en.json -o data/output/tlh.json --use-cache
```

### 手动翻译模式

当 API 限制较多时，可以使用手动翻译模式：

```bash
# 1. 提取所有值到文本文件
python main.py -i data/input/en.json --extract-only -t values.txt

# 2. 手动翻译 values.txt 文件
#    注意：每行末尾都有一个 ~ 符号，这是行分隔符，翻译时请务必保留
#    即使翻译后所有文本都在一行，只要保留了 ~ 符号就能正确导入

# 3. 从翻译好的文本文件重建 JSON
python main.py -i data/input/en.json -o data/output/tlh.json --from-text translated.txt
```

**重要提示**：
- 提取的文本文件中，每行末尾都有一个 `~` 符号作为行分隔符
- 翻译时**必须保留**这个符号，它用于标记每个值的结尾
- 即使将所有文本复制到翻译网站后变成一行，只要保留了 `~` 符号，导入时就能正确分割
- 可以在 `config/config.json` 中修改 `processing.line_separator` 来自定义分隔符

## 📖 使用说明

### 命令行参数

```
必需参数:
  -i, --input INPUT        输入的 JSON 文件路径

可选参数:
  -o, --output OUTPUT      输出的 JSON 文件路径
  -c, --config CONFIG      配置文件路径 (默认: config/config.json)
  --use-cache             使用翻译缓存
  --clear-cache           清空翻译缓存并退出
  --extract-only          仅提取值到文本文件，不翻译
  -t, --text-file TEXT    文本文件路径（用于提取或导入）
  --from-text TEXT        从翻译好的文本文件导入
  --log-file LOG          日志文件路径
  -v, --verbose           显示详细信息
```

### 配置文件

配置文件位于 `config/config.json`，可以自定义以下设置：

```json
{
  "api": {
    "base_url": "https://api.funtranslations.com/translate/klingon.json",
    "rate_limit": {
      "requests_per_hour": 5,
      "requests_per_day": 60,
      "wait_on_limit": true
    },
    "retry": {
      "max_retries": 3,
      "backoff_factor": 2
    }
  },
  "processing": {
    "use_cache": true,
    "cache_dir": "data/cache",
    "batch_short_texts": true,
    "max_batch_length": 900,
    "line_separator": "~"
  },
  "logging": {
    "level": "INFO",
    "show_progress": true
  }
}
```

## 📁 项目结构

```
JsonKlingonizer/
├── src/
│   ├── __init__.py           # 包初始化
│   ├── extractor.py          # JSON 值提取器
│   ├── translator.py         # 克林贡语翻译器
│   ├── rebuilder.py          # JSON 重建器
│   └── utils.py              # 工具函数（缓存、日志等）
├── data/
│   ├── input/                # 输入 JSON 文件
│   ├── output/               # 输出翻译后的 JSON
│   └── cache/                # 翻译缓存
├── config/
│   └── config.json           # 配置文件
├── main.py                   # 主入口脚本
├── requirements.txt          # Python 依赖
├── LICENSE                   # MIT 许可证
└── README.md                 # 本文件
```

## 💡 使用示例

### 示例 1：简单翻译

**输入文件** (`data/input/en.json`):
```json
{
  "app": {
    "name": "My Application",
    "version": "1.0.0"
  },
  "messages": {
    "welcome": "Welcome to our app!",
    "goodbye": "See you later!"
  }
}
```

**运行命令**:
```bash
python main.py -i data/input/en.json -o data/output/tlh.json --use-cache
```

**输出文件** (`data/output/tlh.json`):
```json
{
  "app": {
    "name": "wIj application",
    "version": "1.0.0"
  },
  "messages": {
    "welcome": "qavan to maj app!",
    "goodbye": "legh SoH later!"
  }
}
```

### 示例 2：批量处理

```bash
# 处理多个文件
for file in data/input/*.json; do
  filename=$(basename "$file" .json)
  python main.py -i "$file" -o "data/output/${filename}_tlh.json" --use-cache
done
```

## ⚠️ 注意事项

### API 限制

Fun Translations 免费 API 有以下限制：
- 每小时 5 次请求
- 每天 60 次请求

**建议**：
1. 使用 `--use-cache` 参数启用缓存，避免重复翻译相同内容
2. 对于大型文件，使用手动翻译模式（`--extract-only` 和 `--from-text`）
3. 如需更高频率使用，可考虑升级到付费 API 或使用其他翻译服务

### 缓存管理

```bash
# 查看缓存统计
# 缓存文件位于: data/cache/translation_cache.json

# 清空缓存
python main.py --clear-cache
```

## 🔧 高级用法

### 自定义翻译器

您可以修改 `src/translator.py` 来支持其他翻译 API：

```python
class CustomTranslator:
    def translate(self, text: str) -> str:
        # 实现您的翻译逻辑
        pass
```

### 扩展支持的数据类型

默认情况下，工具只翻译字符串值。您可以修改 `src/extractor.py` 来支持其他数据类型。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Fun Translations API](https://funtranslations.com/) - 提供克林贡语翻译服务
- 所有贡献者和使用者

## 📮 联系方式

- GitHub: [@HsxMark](https://github.com/HsxMark)
- Project Link: [https://github.com/HsxMark/JsonKlingonizer](https://github.com/HsxMark/JsonKlingonizer)

---

**Qapla'!** (克林贡语：成功！) 🖖