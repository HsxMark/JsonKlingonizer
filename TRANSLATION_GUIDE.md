# 翻译指南 🌍

本文档介绍如何使用 JsonKlingonizer 进行各种语言翻译。

## 快速开始

### 1. 英文 → 中文

最常见的使用场景：

```bash
# 基本用法
python main.py -i en.json -o zh.json --translator google --source en --target zh-cn

# 使用缓存（推荐）
python main.py -i en.json -o zh.json --translator google --source en --target zh-cn --use-cache

# 自动检测源语言
python main.py -i en.json -o zh.json --translator google --source auto --target zh-cn --use-cache
```

### 2. 中文 → 英文

```bash
python main.py -i zh.json -o en.json --translator google --source zh-cn --target en --use-cache
```

### 3. 多语言翻译

```bash
# 英文 → 日文
python main.py -i en.json -o ja.json --translator google --source en --target ja --use-cache

# 英文 → 韩文
python main.py -i en.json -o ko.json --translator google --source en --target ko --use-cache

# 英文 → 法文
python main.py -i en.json -o fr.json --translator google --source en --target fr --use-cache

# 英文 → 西班牙文
python main.py -i en.json -o es.json --translator google --source en --target es --use-cache
```

## 翻译器选择

### Google Translator（推荐）

**优点：**
- ✅ 完全免费，无需 API Key
- ✅ 支持 100+ 种语言
- ✅ 翻译质量高
- ✅ 速度快

**使用方法：**
```bash
python main.py -i input.json -o output.json \
  --translator google \
  --source en \
  --target zh-cn \
  --use-cache
```

**注意事项：**
- 使用非官方 API，可能会遇到网络问题
- 建议启用缓存以提高效率
- 如遇问题可尝试使用 VPN

### LibreTranslate

**优点：**
- ✅ 开源、可自托管
- ✅ 隐私友好
- ✅ 支持多种语言

**使用方法：**
```bash
# 使用公共实例
python main.py -i input.json -o output.json \
  --translator libre \
  --source en \
  --target zh \
  --use-cache

# 使用自托管实例（需要在 config.json 中配置）
# "api": {
#   "libre_url": "http://your-server:5000/translate",
#   "libre_api_key": "your-api-key"
# }
```

**注意事项：**
- 公共实例可能有速率限制
- 推荐自托管以获得更好的性能和隐私保护
- 语言代码使用 `zh` 而不是 `zh-cn`

### Klingon Translator（趣味）

**优点：**
- ✅ 支持克林贡语等特殊语言
- ✅ 趣味性强

**缺点：**
- ❌ API 限制严格（每小时 5 次）
- ❌ 仅适合小规模使用

**使用方法：**
```bash
python main.py -i input.json -o output.json \
  --translator klingon \
  --use-cache
```

## 常见场景

### 场景 1：网站/应用国际化

将应用的英文语言包翻译成多种语言：

```bash
#!/bin/bash
# translate_all.sh

INPUT="locales/en.json"

# 翻译成中文
python main.py -i $INPUT -o locales/zh-cn.json --translator google --source en --target zh-cn --use-cache

# 翻译成日文
python main.py -i $INPUT -o locales/ja.json --translator google --source en --target ja --use-cache

# 翻译成韩文
python main.py -i $INPUT -o locales/ko.json --translator google --source en --target ko --use-cache

# 翻译成法文
python main.py -i $INPUT -o locales/fr.json --translator google --source en --target fr --use-cache

# 翻译成德文
python main.py -i $INPUT -o locales/de.json --translator google --source en --target de --use-cache

echo "✅ 所有翻译完成！"
```

### 场景 2：批量翻译多个文件

```bash
#!/bin/bash
# batch_translate.sh

SOURCE_DIR="data/input"
OUTPUT_DIR="data/output"
SOURCE_LANG="en"
TARGET_LANG="zh-cn"

for file in $SOURCE_DIR/*.json; do
  filename=$(basename "$file" .json)
  echo "正在翻译: $filename"
  
  python main.py \
    -i "$file" \
    -o "$OUTPUT_DIR/${filename}_${TARGET_LANG}.json" \
    --translator google \
    --source $SOURCE_LANG \
    --target $TARGET_LANG \
    --use-cache
done

echo "✅ 批量翻译完成！"
```

### 场景 3：手动翻译（高质量翻译）

当需要更高质量的翻译时，可以结合 DeepL、ChatGPT 等工具：

```bash
# 1. 提取文本
python main.py -i en.json --extract-only -t to_translate.txt

# 2. 复制 to_translate.txt 的内容到 DeepL/ChatGPT
#    注意保留每行末尾的 ~ 符号

# 3. 将翻译结果保存为 translated.txt

# 4. 重建 JSON
python main.py -i en.json -o zh.json --from-text translated.txt
```

### 场景 4：双向翻译对照

生成英中对照文件：

```bash
# 原始英文
python main.py -i en.json -o output/en.json --translator google --source en --target en --use-cache

# 翻译成中文
python main.py -i en.json -o output/zh-cn.json --translator google --source en --target zh-cn --use-cache

# 反向翻译（验证翻译质量）
python main.py -i output/zh-cn.json -o output/en-from-zh.json --translator google --source zh-cn --target en --use-cache
```

## 配置优化

### 1. 设置默认翻译器

编辑 `config/config.json`：

```json
{
  "translator": {
    "type": "google",        // 默认使用 Google 翻译
    "source_lang": "auto",   // 自动检测源语言
    "target_lang": "zh-cn"   // 默认翻译成简体中文
  }
}
```

这样就可以简化命令：

```bash
# 使用默认配置
python main.py -i en.json -o zh.json --use-cache

# 只需要临时修改目标语言
python main.py -i en.json -o ja.json --target ja --use-cache
```

### 2. 启用缓存（强烈推荐）

```json
{
  "processing": {
    "use_cache": true,        // 自动启用缓存
    "cache_dir": "data/cache"
  }
}
```

### 3. 配置日志

```json
{
  "logging": {
    "level": "INFO",          // DEBUG, INFO, WARNING, ERROR
    "show_progress": true     // 显示进度条
  }
}
```

## 语言代码参考

### 常用语言代码

| 语言 | Google/Libre 代码 |
|------|-------------------|
| 自动检测 | `auto` |
| 英语 | `en` |
| 简体中文 | `zh-cn` (Google) / `zh` (Libre) |
| 繁体中文 | `zh-tw` (Google) / `zh` (Libre) |
| 日语 | `ja` |
| 韩语 | `ko` |
| 法语 | `fr` |
| 德语 | `de` |
| 西班牙语 | `es` |
| 俄语 | `ru` |
| 阿拉伯语 | `ar` |
| 葡萄牙语 | `pt` |
| 意大利语 | `it` |
| 荷兰语 | `nl` |
| 波兰语 | `pl` |
| 土耳其语 | `tr` |
| 越南语 | `vi` |
| 泰语 | `th` |
| 印尼语 | `id` |
| 印地语 | `hi` |

### 查看完整语言列表

```bash
python main.py --list-translators
```

## 性能优化

### 1. 使用缓存

缓存可以显著提高重复翻译的速度：

```bash
# 第一次翻译（慢）
python main.py -i en.json -o zh.json --translator google --use-cache

# 再次翻译相同内容（快！）
python main.py -i en.json -o zh.json --translator google --use-cache
```

### 2. 清空缓存

如果翻译结果不理想，可以清空缓存重新翻译：

```bash
python main.py --clear-cache
```

### 3. 批处理优化

处理多个文件时，使用相同的缓存目录：

```bash
for file in *.json; do
  python main.py -i "$file" -o "output/$file" --translator google --use-cache
done
```

## 故障排除

### 问题 1：Google Translator 连接失败

**解决方案：**
- 检查网络连接
- 尝试使用 VPN
- 等待一段时间后重试
- 考虑使用 LibreTranslate 作为替代

### 问题 2：翻译质量不理想

**解决方案：**
- 使用手动翻译模式
- 结合 DeepL、ChatGPT 等工具
- 使用 `--extract-only` 导出后手动调整

### 问题 3：Klingon API 速率限制

**解决方案：**
- 使用 `--use-cache` 启用缓存
- 使用手动翻译模式
- 等待速率限制重置

### 问题 4：翻译后 JSON 格式错误

**解决方案：**
- 检查原始 JSON 是否有效
- 使用 `--verbose` 查看详细错误信息
- 检查是否跳过了某些值的翻译

## 最佳实践

1. **始终使用缓存** - 使用 `--use-cache` 参数
2. **自动检测源语言** - 使用 `--source auto`
3. **批量处理前测试** - 先测试单个文件
4. **备份原始文件** - 翻译前备份原始 JSON
5. **验证翻译结果** - 翻译后检查输出文件
6. **版本控制** - 将翻译结果纳入版本控制

## 贡献

如果您有更好的翻译方案或建议，欢迎提交 Issue 或 Pull Request！
