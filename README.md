# JsonKlingonizer 🌐

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个通用的 JSON 值提取、翻译和重建工具。支持多种翻译服务：
- **Google Translate** - 免费，支持 100+ 种语言，无需 API Key
- **LibreTranslate** - 开源、可自托管的翻译服务
- **Klingon API** - 趣味翻译，支持克林贡语等特殊语言

## ✨ 特性

- 🔍 **智能提取**：递归提取 JSON 中的所有字符串值，保留完整路径信息
- � **部分翻译**：根据关键词（如 `%TODO`）只翻译未完成的内容，跳过已翻译部分
- �🌐 **多翻译器支持**：支持 Google Translate、LibreTranslate、Klingon API 等
- 🌍 **多语言支持**：支持中文、英文、日文、韩文等 100+ 种语言
- 💾 **缓存机制**：自动缓存翻译结果，避免重复调用 API
- ⚡ **速率控制**：智能处理 API 速率限制
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

### 基本使用 - Google 翻译（推荐）

```bash
# 英文翻译成中文
python main.py -i data/input/en.json -o data/output/zh.json --translator google --source en --target zh-cn

# 中文翻译成英文
python main.py -i data/input/zh.json -o data/output/en.json --translator google --source zh-cn --target en

# 自动检测源语言
python main.py -i data/input/any.json -o data/output/zh.json --translator google --source auto --target zh-cn
```

### 使用其他翻译器

```bash
# 使用 LibreTranslate
python main.py -i en.json -o zh.json --translator libre --source en --target zh

# 使用克林贡语翻译（趣味）
python main.py -i en.json -o tlh.json --translator klingon

# 使用反转翻译（趣味）
python main.py -i en.json -o reverse.json --translator reverse
```

### 使用缓存（推荐）

```bash
# 启用缓存可以避免重复翻译相同的文本
python main.py -i en.json -o zh.json --translator google --use-cache
```

### 部分翻译（增量翻译）🆕

当 JSON 文件中有些内容已翻译，有些还未翻译（标记为 `%TODO` 等）时，可以只翻译未完成的部分：

```bash
# 只翻译包含 %TODO 标记的内容，翻译后移除标记
python main.py -i fr.json -o fr.json \
  --translator google --source zh-cn --target fr \
  --filter-keyword "%TODO" --remove-keyword --use-cache

# 提取包含 %TODO 的内容到文本文件（用于手动翻译）
python main.py -i fr.json --extract-only -t todo.txt --filter-keyword "%TODO"

# 从翻译好的文本文件导入
python main.py -i fr.json -o fr-translated.json --from-text todo-translated.txt
```

**示例**：

输入文件包含已翻译和未翻译的内容：
```json
{
  "settings": {
    "version": "Version",
    "checkUpdate": "%TODO 检查更新",
    "author": "Auteur"
  }
}
```

运行翻译后，只有包含 `%TODO` 的内容被翻译：
```json
{
  "settings": {
    "version": "Version",
    "checkUpdate": "Vérifier les mises à jour",
    "author": "Auteur"
  }
}
```

详细说明请参考：[部分翻译功能使用指南](docs/PARTIAL_TRANSLATION_GUIDE.md)

### 手动翻译模式

当需要精确翻译或处理特殊内容时，可以使用手动翻译模式：

```bash
# 1. 提取所有值到文本文件
python main.py -i data/input/en.json --extract-only -t values.txt

# 2. 手动翻译 values.txt 文件
#    注意：每行末尾都有一个 ~ 符号，这是行分隔符，翻译时请务必保留
#    可以使用任何翻译工具（DeepL、ChatGPT等）进行翻译

# 3. 从翻译好的文本文件重建 JSON
python main.py -i data/input/en.json -o data/output/zh.json --from-text translated.txt
```

**重要提示**：
- 提取的文本文件中，每行末尾都有一个 `~` 符号作为行分隔符
- 翻译时**必须保留**这个符号，它用于标记每个值的结尾
- 即使将所有文本复制到翻译网站后变成一行，只要保留了 `~` 符号，导入时就能正确分割

### 查看可用的翻译器

```bash
python main.py --list-translators
```

## 📖 使用说明

### 命令行参数

```
必需参数:
  -i, --input INPUT              输入的 JSON 文件路径

可选参数:
  -o, --output OUTPUT            输出的 JSON 文件路径
  -c, --config CONFIG            配置文件路径 (默认: config/config.json)
  --translator {google,klingon,libre}
                                 翻译器类型
  --source, --source-lang LANG   源语言代码（如 en, zh-cn, auto）
  --target, --target-lang LANG   目标语言代码（如 en, zh-cn, ja）
  --list-translators             列出所有可用的翻译器
  --use-cache                    使用翻译缓存
  --clear-cache                  清空翻译缓存并退出
  --extract-only                 仅提取值到文本文件，不翻译
  -t, --text-file TEXT           文本文件路径（用于提取或导入）
  --from-text TEXT               从翻译好的文本文件导入
  --filter-keyword KEYWORD       过滤关键词，只提取包含此关键词的值（如 %TODO）
  --remove-keyword               翻译后从结果中移除过滤关键词
  --log-file LOG                 日志文件路径
  -v, --verbose                  显示详细信息
```

### 支持的语言代码

**Google Translator / LibreTranslate：**
- `auto` - 自动检测
- `en` - English（英文）
- `zh-cn` - 简体中文
- `zh-tw` - 繁体中文
- `ja` - 日本語
- `ko` - 한국어
- `fr` - Français（法语）
- `de` - Deutsch（德语）
- `es` - Español（西班牙语）
- `ru` - Русский（俄语）
- `ar` - العربية（阿拉伯语）
- `pt` - Português（葡萄牙语）
- `it` - Italiano（意大利语）
- 更多语言请使用 `--list-translators` 查看

### 配置文件

配置文件位于 `config/config.json`，可以自定义以下设置：

```json
{
  "translator": {
    "type": "google",           // 默认翻译器: google, klingon, libre
    "source_lang": "auto",      // 默认源语言
    "target_lang": "zh-cn"      // 默认目标语言
  },
  "api": {
    "base_url": "https://api.funtranslations.com/translate/klingon.json",
    "libre_url": "https://libretranslate.com/translate",
    "libre_api_key": null,      // LibreTranslate API Key（可选）
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
│   ├── translators/          # 翻译器模块
│   │   ├── __init__.py       # 模块初始化
│   │   ├── base_translator.py      # 翻译器基类
│   │   ├── googletrans_translator.py  # Google 翻译器
│   │   ├── libre_translator.py     # LibreTranslate 翻译器
│   │   ├── klingon_translator.py   # 克林贡语翻译器
│   │   └── reverse_translator.py   # 反转翻译器
│   ├── __init__.py           # 包初始化
│   ├── extractor.py          # JSON 值提取器
│   ├── rebuilder.py          # JSON 重建器
│   └── utils.py              # 工具函数（缓存、日志等）
├── data/
│   ├── input/                # 输入 JSON 文件
│   ├── output/               # 输出翻译后的 JSON
│   └── cache/                # 翻译缓存
├── config/
│   └── config.json           # 配置文件
├── docs/
│   └── LIBRETRANSLATE_SETUP.md  # LibreTranslate 部署指南
├── scripts/
│   ├── deploy_libretranslate.sh  # LibreTranslate 部署脚本
│   └── start_libretranslate_compose.sh  # Docker Compose 启动脚本
├── examples/                 # 示例文件
├── docker-compose.yml        # Docker Compose 配置
├── main.py                   # 主入口脚本
├── requirements.txt          # Python 依赖
├── LICENSE                   # MIT 许可证
└── README.md                 # 本文件
```

## 💡 使用示例

### 示例 1：英文翻译成中文

**输入文件** (`data/input/en.json`):
```json
{
  "app": {
    "name": "My Application",
    "version": "1.0.0",
    "description": "A powerful translation tool"
  },
  "messages": {
    "welcome": "Welcome to our app!",
    "goodbye": "See you later!"
  }
}
```

**运行命令**:
```bash
python main.py -i data/input/en.json -o data/output/zh.json \
  --translator google --source en --target zh-cn --use-cache
```

**输出文件** (`data/output/zh.json`):
```json
{
  "app": {
    "name": "我的应用程序",
    "version": "1.0.0",
    "description": "一个强大的翻译工具"
  },
  "messages": {
    "welcome": "欢迎使用我们的应用！",
    "goodbye": "再见！"
  }
}
```

### 示例 2：中文翻译成英文

```bash
python main.py -i zh.json -o en.json \
  --translator google --source zh-cn --target en --use-cache
```

### 示例 3：批量处理多个文件

```bash
# 将所有英文 JSON 翻译成中文
for file in data/input/*.json; do
  filename=$(basename "$file" .json)
  python main.py -i "$file" -o "data/output/${filename}_zh.json" \
    --translator google --source en --target zh-cn --use-cache
done
```

## ⚠️ 注意事项

### 翻译器对比

| 翻译器 | 优点 | 缺点 | 适用场景 |
|--------|------|------|----------|
| **Google** | 免费、快速、质量高、支持100+语言 | 非官方API，可能不稳定 | 日常翻译、多语言支持 |
| **LibreTranslate** | 开源、可自托管、隐私友好 | 需要部署服务器或API Key | 企业内部、隐私敏感场景 |
| **Klingon** | 趣味性强 | API限制严格（每小时5次） | 趣味项目、特殊语言 |
| **Reverse** | 本地处理、无网络依赖、即时响应 | 仅用于趣味翻译 | 开发测试、娱乐用途 |

### Google Translator 使用说明

- 使用免费的 `googletrans` 库，无需 API Key
- 翻译速度快，质量高
- 建议启用缓存以提高效率
- 如遇到网络问题，可尝试使用 VPN

### LibreTranslate 使用说明

**三种使用方式**：

1. **自托管（推荐）** - 完全免费、无限制、隐私友好
   ```bash
   # 一键部署（推荐）
   bash scripts/deploy_libretranslate.sh
   
   # 或使用 Docker Compose
   bash scripts/start_libretranslate_compose.sh
   
   # 或直接使用 Docker
   docker run -d -p 5000:5000 libretranslate/libretranslate
   ```
   
   详细部署指南：查看 [`docs/LIBRETRANSLATE_SETUP.md`](docs/LIBRETRANSLATE_SETUP.md)

2. **使用公共实例** - 免费但有速率限制
   - 公共实例：https://libretranslate.com
   - 配置：`"libre_url": "https://libretranslate.com/translate"`

3. **自己的服务器** - 完全控制
   - 部署到云服务器（AWS、阿里云等）
   - 配置：`"libre_url": "http://your-server:5000/translate"`

**配置示例**：
```json
{
  "translator": {
    "type": "libre",
    "source_lang": "en",
    "target_lang": "zh"
  },
  "api": {
    "libre_url": "http://localhost:5000/translate",
    "libre_api_key": null
  }
}
```

### Klingon API 限制

Fun Translations 免费 API 有以下限制：
- 每小时 5 次请求
- 每天 60 次请求

**建议**：
1. 对于克林贡语翻译，使用 `--use-cache` 参数启用缓存
2. 对于大型文件，使用手动翻译模式
3. 如需更高频率使用，可考虑升级到付费 API

### 缓存管理

```bash
# 查看缓存统计
# 缓存文件位于: data/cache/translation_cache.json

# 清空缓存
python main.py --clear-cache
```

## 🔧 高级用法

### 自定义翻译器

您可以轻松添加新的翻译服务。创建一个继承 `BaseTranslator` 的类：

```python
from src.translators.base_translator import BaseTranslator

class MyTranslator(BaseTranslator):
    def translate(self, text: str, source_lang: str = 'auto', 
                  target_lang: str = 'en') -> str:
        # 实现您的翻译逻辑
        pass
```

### 使用 DeepL API

虽然项目暂未内置 DeepL 支持，但您可以：
1. 使用 `--extract-only` 导出文本
2. 使用 DeepL 网站或 API 翻译
3. 使用 `--from-text` 导入翻译结果

### 配置 LibreTranslate 自托管实例

```json
{
  "api": {
    "libre_url": "http://your-server:5000/translate",
    "libre_api_key": "your-api-key"
  }
}
```

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

- [googletrans](https://github.com/ssut/googletrans) - Google Translate 非官方 Python API
- [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate) - 开源机器翻译 API
- [Fun Translations API](https://funtranslations.com/) - 提供克林贡语等趣味翻译服务
- 所有贡献者和使用者

## 📮 联系方式

- GitHub: [@HsxMark](https://github.com/HsxMark)
- Project Link: [https://github.com/HsxMark/JsonKlingonizer](https://github.com/HsxMark/JsonKlingonizer)

---

**Made with ❤️ for the translation community** 🌍