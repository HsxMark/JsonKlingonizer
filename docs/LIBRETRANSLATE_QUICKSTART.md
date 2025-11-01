# LibreTranslate 快速开始指南

## 🚀 一键部署（推荐）

### macOS / Linux

```bash
# 方式 1: 使用自动部署脚本（最简单）
bash scripts/deploy_libretranslate.sh

# 方式 2: 使用 Docker Compose
bash scripts/start_libretranslate_compose.sh

# 方式 3: 直接使用 Docker
docker run -d --name libretranslate -p 5000:5000 libretranslate/libretranslate
```

### Windows

```powershell
# 使用 PowerShell（需要先安装 Docker Desktop）
docker run -d --name libretranslate -p 5000:5000 libretranslate/libretranslate
```

## ✅ 验证部署

### 1. 检查容器状态
```bash
docker ps | grep libretranslate
```

### 2. 访问 Web 界面
打开浏览器访问：http://localhost:5000

### 3. 测试 API
```bash
curl -X POST "http://localhost:5000/translate" \
  -H "Content-Type: application/json" \
  -d '{"q":"Hello","source":"en","target":"zh","format":"text"}'
```

## 🔧 配置 JsonKlingonizer

### 1. 修改配置文件

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

### 2. 开始翻译

```bash
# 英文 -> 中文
python main.py -i data/input/en.json -o data/output/zh.json \
  --translator libre --source en --target zh --use-cache

# 中文 -> 英文
python main.py -i data/input/zh.json -o data/output/en.json \
  --translator libre --source zh --target en --use-cache
```

## 📊 管理命令

```bash
# 查看日志
docker logs -f libretranslate

# 停止服务
docker stop libretranslate

# 启动服务
docker start libretranslate

# 重启服务
docker restart libretranslate

# 删除容器
docker rm -f libretranslate

# 查看资源使用
docker stats libretranslate
```

## 🎯 常见问题

### Q: 首次启动很慢？
A: 正常现象，需要下载语言模型（几百 MB），之后会很快。

### Q: 翻译质量如何？
A: 基于 Argos Translate，质量良好，适合大部分场景。

### Q: 支持哪些语言？
A: 支持 30+ 种语言，包括英语、中文、日语、韩语、法语、德语等。

### Q: 可以离线使用吗？
A: 可以！模型下载后即可离线翻译。

### Q: 内存占用多少？
A: 约 1-2GB RAM，首次运行时可能更高。

### Q: 如何更新？
A: 
```bash
docker pull libretranslate/libretranslate:latest
docker rm -f libretranslate
bash scripts/deploy_libretranslate.sh
```

## 📚 详细文档

完整部署指南：[docs/LIBRETRANSLATE_SETUP.md](docs/LIBRETRANSLATE_SETUP.md)

包含：
- 详细的部署步骤
- 高级配置选项
- 性能优化建议
- 安全配置
- 监控和维护
- 故障排除

## 💡 最佳实践

1. ✅ **开发环境**：使用 Docker 快速部署到本地
2. ✅ **生产环境**：使用 Docker Compose + Nginx + HTTPS
3. ✅ **性能优化**：增加内存限制，预加载常用语言模型
4. ✅ **安全性**：启用 API Key，限制访问 IP
5. ✅ **备份**：定期备份 libretranslate-data 目录

## 🆚 对比

| 特性 | LibreTranslate (自托管) | Google Translate (googletrans) |
|------|------------------------|-------------------------------|
| 费用 | 完全免费 | 免费（非官方） |
| 隐私 | 完全私有 | 数据发送到 Google |
| 稳定性 | 非常稳定 | 可能不稳定 |
| 速率限制 | 无限制 | 可能被封 IP |
| 翻译质量 | 良好 | 优秀 |
| 离线使用 | ✅ 支持 | ❌ 不支持 |
| 部署难度 | 简单 | 无需部署 |
| 维护成本 | 需要服务器资源 | 无 |

## 🎉 开始使用

1. 运行部署脚本：`bash scripts/deploy_libretranslate.sh`
2. 等待服务启动（首次约 2-5 分钟）
3. 访问 http://localhost:5000 验证
4. 开始翻译！

---

**享受免费、稳定、无限制的翻译服务！** 🌍✨
