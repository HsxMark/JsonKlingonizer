# 部分翻译功能使用指南

## 功能概述

部分翻译功能允许您根据关键词提取 JSON 文件中未翻译的内容，翻译这些内容，然后将翻译结果塞回源文件。已翻译的部分将被自动跳过。

这个功能特别适用于以下场景：
- JSON 文件中有些内容标记了 `%TODO` 或其他待翻译标记
- 多语言文件需要增量更新，只翻译新增的未翻译内容
- 协作翻译项目，不同人员负责不同部分

## 工作流程

### 方式一：自动翻译（使用 API）

#### 1. 直接翻译包含关键词的内容

```bash
python main.py \
  -i data/input/fr.json \
  -o data/output/fr-translated.json \
  --translator google \
  --source zh-cn \
  --target fr \
  --filter-keyword "%TODO" \
  --remove-keyword \
  --use-cache
```

**参数说明：**
- `-i`: 输入文件（包含待翻译内容的 JSON 文件）
- `-o`: 输出文件（翻译后的 JSON 文件）
- `--translator`: 翻译器类型（google/libre/klingon）
- `--source`: 源语言代码（如 zh-cn 表示简体中文）
- `--target`: 目标语言代码（如 fr 表示法语）
- `--filter-keyword`: 过滤关键词（只提取包含此关键词的值）
- `--remove-keyword`: 翻译后从结果中移除关键词
- `--use-cache`: 使用翻译缓存（避免重复翻译）

**示例：**

原始文件 `fr.json`：
```json
{
  "settings": {
    "version": "Version",
    "checkUpdate": "%TODO 检查更新",
    "author": "Auteur"
  }
}
```

翻译后 `fr-translated.json`：
```json
{
  "settings": {
    "version": "Version",
    "checkUpdate": "Vérifier les mises à jour",
    "author": "Auteur"
  }
}
```

> **注意：** 只有 `checkUpdate` 包含 `%TODO` 关键词，因此只有它被翻译。其他已翻译的内容保持不变。

#### 2. 原地更新（覆盖原文件）

如果您想直接更新原文件，可以将输入和输出指定为同一个文件：

```bash
python main.py \
  -i data/input/fr.json \
  -o data/input/fr.json \
  --translator google \
  --source zh-cn \
  --target fr \
  --filter-keyword "%TODO" \
  --remove-keyword \
  --use-cache
```

> ⚠️ **警告：** 这会覆盖原文件，建议先备份或使用版本控制。

### 方式二：手动翻译（导出-翻译-导入）

适用于需要人工校对或使用其他翻译工具的场景。

#### 步骤 1：提取待翻译内容

```bash
python main.py \
  -i data/input/fr.json \
  --extract-only \
  -t data/output/todo-values.txt \
  --filter-keyword "%TODO"
```

生成的 `todo-values.txt` 文件内容：
```
%TODO 有新版本~
%TODO 检查更新~
%TODO 正在检查更新~
%TODO 当前已是最新版本~
%TODO 检查更新失败~
```

> **重要：** 每行末尾的 `~` 符号是行分隔符，翻译时请保留！

#### 步骤 2：手动翻译

使用您喜欢的工具（如 CAT 工具、人工翻译等）翻译文本，保存为 `todo-translated.txt`：

```
Il existe une nouvelle version de~
Vérifier les mises à jour~
vérifie les mises à jour~
est actuellement la dernière version~
Échec de la vérification des mises à jour~
```

> **重要：** 
> - 保留每行末尾的 `~` 符号
> - 保持行数与原文件相同
> - 不要删除或添加行

#### 步骤 3：导入翻译结果

```bash
python main.py \
  -i data/input/fr.json \
  -o data/output/fr-translated.json \
  --from-text data/output/todo-translated.txt
```

如果需要移除关键词（如 `%TODO`），可以手动在翻译文件中删除，或者在导入前使用文本编辑器批量替换。

## 高级用法

### 1. 使用不同的关键词

您可以使用任何关键词作为过滤器：

```bash
# 使用 [TODO] 作为关键词
python main.py -i input.json -o output.json --filter-keyword "[TODO]" --translator google

# 使用 UNTRANSLATED 作为关键词
python main.py -i input.json -o output.json --filter-keyword "UNTRANSLATED" --translator google

# 使用中文标记
python main.py -i input.json -o output.json --filter-keyword "待翻译" --translator google
```

### 2. 不移除关键词

如果您想保留关键词（例如用于后续追踪），可以不使用 `--remove-keyword` 参数：

```bash
python main.py \
  -i input.json \
  -o output.json \
  --translator google \
  --source zh-cn \
  --target fr \
  --filter-keyword "%TODO"
  # 注意：没有 --remove-keyword
```

这样翻译后的内容仍会保留 `%TODO` 标记。

### 3. 结合缓存使用

使用缓存可以避免重复翻译相同的内容，节省 API 调用次数：

```bash
# 第一次翻译
python main.py -i file1.json -o file1-out.json --translator google --filter-keyword "%TODO" --use-cache

# 第二次翻译（相同内容会从缓存读取）
python main.py -i file2.json -o file2-out.json --translator google --filter-keyword "%TODO" --use-cache
```

查看缓存统计：

```bash
python main.py --list-translators  # 会显示缓存信息
```

清空缓存：

```bash
python main.py --clear-cache
```

### 4. 批量处理多个文件

您可以使用 shell 脚本批量处理多个文件：

```bash
#!/bin/bash

# 批量翻译所有包含 %TODO 的 JSON 文件
for file in data/input/*.json; do
  filename=$(basename "$file")
  echo "Processing $filename..."
  python main.py \
    -i "$file" \
    -o "data/output/${filename%.json}-translated.json" \
    --translator google \
    --source zh-cn \
    --target fr \
    --filter-keyword "%TODO" \
    --remove-keyword \
    --use-cache
done
```

## 支持的翻译器

### 1. Google 翻译（推荐）

- **类型：** `google`
- **优点：** 免费、快速、准确、支持多种语言
- **缺点：** 可能有速率限制
- **使用示例：**
  ```bash
  --translator google --source zh-cn --target fr
  ```

### 2. LibreTranslate（开源）

- **类型：** `libre`
- **优点：** 开源、可自托管、隐私保护
- **缺点：** 需要配置 API 地址
- **使用示例：**
  ```bash
  --translator libre --source zh --target fr
  ```

### 3. Klingon 翻译器（娱乐）

- **类型：** `klingon`
- **优点：** 有趣的克林贡语翻译
- **缺点：** 免费 API 限制严格（每小时 5 次）
- **使用示例：**
  ```bash
  --translator klingon
  ```

## 常见语言代码

| 语言 | Google 代码 | LibreTranslate 代码 |
|------|------------|-------------------|
| 简体中文 | zh-cn | zh |
| 繁体中文 | zh-tw | zt |
| 英语 | en | en |
| 法语 | fr | fr |
| 德语 | de | de |
| 日语 | ja | ja |
| 韩语 | ko | ko |
| 西班牙语 | es | es |
| 俄语 | ru | ru |

查看完整语言列表：

```bash
python main.py --list-translators
```

## 常见问题

### Q1: 翻译后的文件格式错乱怎么办？

A: 检查以下几点：
1. 输入文件是否为有效的 JSON 格式
2. 使用 `--from-text` 时，文本文件的行数是否与提取时一致
3. 是否保留了行分隔符 `~`

### Q2: 为什么有些内容没有被翻译？

A: 可能的原因：
1. 内容不包含指定的过滤关键词
2. 使用了缓存，且缓存中已有该内容
3. 内容被识别为不需要翻译（如版本号、数字等）

### Q3: 如何处理嵌套很深的 JSON？

A: 工具自动递归处理所有层级的 JSON，无需特殊配置。

### Q4: 可以同时使用多个关键词吗？

A: 目前不支持。如需处理多个关键词，可以多次运行：

```bash
# 第一次处理 %TODO
python main.py -i input.json -o temp.json --filter-keyword "%TODO" --translator google --remove-keyword

# 第二次处理 [UNTRANSLATED]
python main.py -i temp.json -o output.json --filter-keyword "[UNTRANSLATED]" --translator google --remove-keyword
```

### Q5: 翻译失败后如何重试？

A: 工具内置了重试机制。如果仍然失败：
1. 检查网络连接
2. 使用 `--verbose` 参数查看详细错误信息
3. 尝试使用不同的翻译器
4. 考虑使用手动翻译方式（导出-翻译-导入）

## 实战示例

### 示例 1：更新多语言项目

假设您有一个多语言项目，新增了一些中文字符串，需要翻译成法语：

```bash
# 1. 在需要翻译的地方添加 %TODO 标记
# "newFeature": "%TODO 新功能"

# 2. 运行翻译
python main.py \
  -i locales/fr.json \
  -o locales/fr.json \
  --translator google \
  --source zh-cn \
  --target fr \
  --filter-keyword "%TODO" \
  --remove-keyword \
  --use-cache

# 3. 检查结果
# "newFeature": "Nouvelle fonctionnalité"
```

### 示例 2：团队协作翻译

团队需要翻译一个大型 JSON 文件：

```bash
# 1. 提取待翻译内容
python main.py -i app.json --extract-only -t todo.txt --filter-keyword "%TODO"

# 2. 将 todo.txt 分发给翻译人员

# 3. 收到翻译后的文件 todo-translated.txt

# 4. 导入翻译结果
python main.py -i app.json -o app-translated.json --from-text todo-translated.txt
```

### 示例 3：多语言批量更新

需要将中文翻译成多种语言：

```bash
#!/bin/bash

LANGUAGES=("fr" "de" "ja" "ko" "es")

for lang in "${LANGUAGES[@]}"; do
  echo "Translating to $lang..."
  python main.py \
    -i "locales/${lang}.json" \
    -o "locales/${lang}.json" \
    --translator google \
    --source zh-cn \
    --target "$lang" \
    --filter-keyword "%TODO" \
    --remove-keyword \
    --use-cache
done

echo "All translations completed!"
```

## 技术说明

### 工作原理

1. **提取阶段：** 递归遍历 JSON，提取包含关键词的字符串值，记录其路径
2. **翻译阶段：** 使用指定的翻译器翻译提取的内容
3. **重建阶段：** 根据记录的路径，将翻译后的内容放回原位置

### 关键词处理

- 关键词匹配是字符串包含匹配（区分大小写）
- 翻译后，关键词会被完整移除（包括前后空格）
- 如果不使用 `--remove-keyword`，关键词会保留在翻译结果中

### 缓存机制

- 缓存以 (源文本, 翻译器类型, 源语言, 目标语言) 为键
- 缓存文件位于 `data/cache/translation_cache.json`
- 使用缓存可以显著提高批量翻译效率

## 最佳实践

1. **备份原文件：** 在原地更新前，务必备份原文件
2. **使用版本控制：** 将 JSON 文件纳入 Git 等版本控制
3. **统一关键词：** 团队统一使用相同的待翻译标记（如 `%TODO`）
4. **启用缓存：** 大规模翻译时启用缓存节省资源
5. **校对翻译：** 机器翻译可能不准确，建议人工校对
6. **测试后部署：** 翻译后先在测试环境验证，确认无误后再部署

## 相关文档

- [README.md](../README.md) - 项目总体说明
- [TRANSLATION_GUIDE.md](../TRANSLATION_GUIDE.md) - 完整翻译指南
- [config/config.json](../config/config.json) - 配置文件说明

## 问题反馈

如遇到问题或有改进建议，欢迎通过 GitHub Issues 反馈。
