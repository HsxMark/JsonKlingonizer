# LibreTranslate 自托管配置完成！ 🎉

## ✅ 已创建的文件

### 📚 文档
- `docs/LIBRETRANSLATE_SETUP.md` - **完整部署指南**
  - 详细的安装步骤（Docker、Python、Docker Compose）
  - 高级配置（Nginx、HTTPS、API Key）
  - 性能优化建议
  - 安全配置
  - 监控和维护
  - 故障排除

- `docs/LIBRETRANSLATE_QUICKSTART.md` - **快速开始指南**
  - 最简化的部署步骤
  - 常见问题解答
  - 对比表格

- `LIBRETRANSLATE_README.md` - **配置说明总览**
  - 文件结构说明
  - 三种部署方式对比
  - 使用场景

### 🛠️ 部署脚本
- `scripts/deploy_libretranslate.sh` - **一键部署脚本**（推荐）
  - 自动检查 Docker 环境
  - 智能处理端口冲突
  - 自动创建数据目录
  - 拉取并启动容器
  - 等待服务就绪并测试
  - 显示详细的使用说明

- `scripts/start_libretranslate_compose.sh` - **Docker Compose 启动脚本**
  - 使用 docker-compose.yml 配置
  - 更易于管理和维护

- `scripts/test_libretranslate.py` - **服务测试脚本**
  - 测试连接
  - 测试翻译功能
  - 列出支持的语言

### ⚙️ 配置文件
- `docker-compose.yml` - **Docker Compose 配置**
  - 完整的服务配置
  - 环境变量设置
  - 资源限制
  - 健康检查

## 🚀 快速开始

### 步骤 1: 部署 LibreTranslate

选择以下任一方式：

**方式 A: 自动部署（最推荐）**
```bash
bash scripts/deploy_libretranslate.sh
```

**方式 B: Docker Compose**
```bash
bash scripts/start_libretranslate_compose.sh
```

**方式 C: 直接使用 Docker**
```bash
docker run -d --name libretranslate -p 5000:5000 libretranslate/libretranslate
```

### 步骤 2: 验证服务

```bash
# 测试连接和翻译功能
python scripts/test_libretranslate.py

# 或访问 Web 界面
open http://localhost:5000
```

### 步骤 3: 配置 JsonKlingonizer

编辑 `config/config.json`：
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

### 步骤 4: 开始翻译

```bash
# 英文 -> 中文
python main.py -i data/input/en.json -o data/output/zh.json \
  --translator libre --source en --target zh --use-cache

# 中文 -> 英文
python main.py -i data/input/zh.json -o data/output/en.json \
  --translator libre --source zh --target en --use-cache
```

## 📊 三种部署方式对比

| 方式 | 复杂度 | 适用场景 | 优点 |
|------|--------|----------|------|
| **自动脚本** | ⭐ 简单 | 开发/测试 | 全自动、友好提示、错误处理 |
| **Docker Compose** | ⭐⭐ 中等 | 生产环境 | 配置化、易管理、可扩展 |
| **直接 Docker** | ⭐ 简单 | 快速测试 | 一条命令、最快部署 |

## 🎯 使用场景

### 场景 1: 个人开发
```bash
# 本地开发，快速部署
bash scripts/deploy_libretranslate.sh

# 翻译测试
python main.py -i test.json -o output.json --translator libre
```

### 场景 2: 团队协作
```bash
# 部署到团队服务器
ssh user@team-server
cd /opt/libretranslate
docker-compose up -d

# 团队成员配置
# config.json: "libre_url": "http://team-server:5000/translate"
```

### 场景 3: 生产环境
```bash
# Docker Compose + Nginx + HTTPS + API Key
# 详见: docs/LIBRETRANSLATE_SETUP.md
```

## 🆚 对比：LibreTranslate vs Google Translate

| 特性 | LibreTranslate（自托管） | Google Translate（googletrans） |
|------|--------------------------|--------------------------------|
| 💰 **费用** | 完全免费 | 免费（非官方 API） |
| 🔒 **隐私** | ✅ 完全私有，数据不离开服务器 | ❌ 数据发送到 Google |
| 🏃 **稳定性** | ✅ 非常稳定 | ⚠️ 可能不稳定 |
| ⚡ **速率限制** | ✅ 无限制（自己的服务器） | ⚠️ 频繁请求可能被封 IP |
| 🎯 **翻译质量** | 😊 良好 | 😄 优秀 |
| 📡 **网络依赖** | ✅ 可完全离线 | ❌ 必须联网 |
| 🛠️ **部署难度** | ⚠️ 需要 Docker | ✅ 无需部署 |
| 💻 **资源需求** | ⚠️ 需要服务器资源（2GB+ RAM） | ✅ 无 |
| 🔧 **维护成本** | ⚠️ 需要维护服务器 | ✅ 无 |
| 🌍 **适用场景** | 企业、隐私敏感、大量翻译 | 个人、轻量使用 |

## 💡 推荐配置

### 开发环境
```bash
# 使用自动部署脚本
bash scripts/deploy_libretranslate.sh

# 配置
{
  "translator": {"type": "libre"},
  "api": {"libre_url": "http://localhost:5000/translate"}
}
```

### 生产环境
```bash
# 使用 Docker Compose
docker-compose up -d

# 配置 Nginx 反向代理 + HTTPS
# 启用 API Key 认证
# 配置资源限制
# 详见: docs/LIBRETRANSLATE_SETUP.md
```

## 📋 管理命令速查

```bash
# 查看容器状态
docker ps | grep libretranslate

# 查看日志
docker logs -f libretranslate

# 停止/启动/重启
docker stop/start/restart libretranslate

# 删除容器
docker rm -f libretranslate

# 查看资源使用
docker stats libretranslate

# 测试服务
python scripts/test_libretranslate.py

# 访问 Web UI
open http://localhost:5000
```

## 🐛 常见问题

### Q: 部署后无法访问？
```bash
# 1. 检查容器是否运行
docker ps | grep libretranslate

# 2. 查看日志
docker logs libretranslate

# 3. 测试连接
curl http://localhost:5000/languages
```

### Q: 首次启动很慢？
A: **正常现象**！首次启动需要下载语言模型（几百 MB），这可能需要 2-5 分钟。

查看进度：
```bash
docker logs -f libretranslate
```

### Q: 翻译质量如何？
A: LibreTranslate 基于 Argos Translate 引擎：
- ✅ **日常使用**：足够好
- ✅ **技术文档**：可以接受
- ⚠️ **文学翻译**：可能不够精准
- 💡 **建议**：对于重要内容，使用手动翻译模式配合 DeepL/ChatGPT

### Q: 支持哪些语言？
A: 30+ 种语言，包括：
- 英语 (en)
- 中文 (zh)
- 日语 (ja)
- 韩语 (ko)
- 法语 (fr)
- 德语 (de)
- 西班牙语 (es)
- 俄语 (ru)
- 等等...

查看完整列表：
```bash
curl http://localhost:5000/languages
```

### Q: 内存占用多少？
A: 约 **1-2GB RAM**，具体取决于：
- 加载的语言模型数量
- 并发翻译请求数量
- 缓存大小

### Q: 可以离线使用吗？
A: ✅ **可以**！模型下载后即可完全离线翻译。

### Q: 如何更新？
```bash
# 拉取最新镜像
docker pull libretranslate/libretranslate:latest

# 删除旧容器
docker rm -f libretranslate

# 重新部署
bash scripts/deploy_libretranslate.sh
```

## 📚 详细文档

- **完整部署指南**: `docs/LIBRETRANSLATE_SETUP.md`
- **快速开始**: `docs/LIBRETRANSLATE_QUICKSTART.md`
- **配置说明**: `LIBRETRANSLATE_README.md`
- **LibreTranslate 官方**: https://github.com/LibreTranslate/LibreTranslate

## 🎉 总结

现在你已经拥有：

1. ✅ **完整的 LibreTranslate 自托管方案**
2. ✅ **一键部署脚本**（超级简单！）
3. ✅ **详细的配置文档**
4. ✅ **测试和管理工具**
5. ✅ **完全免费、无限制、隐私友好的翻译服务**

## 🚀 立即开始

```bash
# 一键部署（推荐）
bash scripts/deploy_libretranslate.sh

# 等待服务启动（2-5 分钟）

# 测试服务
python scripts/test_libretranslate.py

# 开始翻译！
python main.py -i input.json -o output.json \
  --translator libre --source en --target zh --use-cache
```

---

**享受自托管的自由和隐私！** 🌍🔒✨
