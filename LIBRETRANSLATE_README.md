# LibreTranslate 自托管配置说明

本目录包含 LibreTranslate 自托管部署的所有配置和脚本。

## 📁 文件说明

### 核心文件

- **`docker-compose.yml`** - Docker Compose 配置文件
  - 用于快速部署 LibreTranslate 服务
  - 包含完整的环境变量和资源配置

### 部署脚本

- **`scripts/deploy_libretranslate.sh`** - 自动部署脚本（推荐）
  - 一键部署 LibreTranslate
  - 自动检查依赖、端口、创建数据目录
  - 包含完整的错误处理和用户提示

- **`scripts/start_libretranslate_compose.sh`** - Docker Compose 启动脚本
  - 使用 Docker Compose 部署
  - 更简洁的配置管理

- **`scripts/test_libretranslate.py`** - 连接测试脚本
  - 测试 LibreTranslate 服务是否正常
  - 验证翻译功能
  - 列出支持的语言

### 文档

- **`docs/LIBRETRANSLATE_SETUP.md`** - 完整部署指南
  - 详细的安装步骤
  - 多种部署方式
  - 高级配置选项
  - 性能优化
  - 安全配置
  - 监控和维护
  - 故障排除

- **`docs/LIBRETRANSLATE_QUICKSTART.md`** - 快速开始指南
  - 最简化的部署步骤
  - 常见问题解答
  - 快速验证方法

## 🚀 快速部署（三种方式）

### 方式 1: 自动部署脚本（最推荐）

```bash
bash scripts/deploy_libretranslate.sh
```

**优点**：
- ✅ 全自动，无需手动操作
- ✅ 完整的错误检查和处理
- ✅ 友好的用户提示
- ✅ 自动测试服务是否正常

### 方式 2: Docker Compose

```bash
bash scripts/start_libretranslate_compose.sh
```

**优点**：
- ✅ 配置文件化，易于管理
- ✅ 支持多服务编排
- ✅ 适合生产环境

### 方式 3: 直接使用 Docker

```bash
docker run -d \
  --name libretranslate \
  -p 5000:5000 \
  -v ~/libretranslate-data:/home/libretranslate/.local \
  --restart unless-stopped \
  libretranslate/libretranslate
```

**优点**：
- ✅ 最简单，一条命令
- ✅ 适合快速测试

## ✅ 验证部署

### 1. 测试连接

```bash
python scripts/test_libretranslate.py
```

### 2. 访问 Web 界面

打开浏览器：http://localhost:5000

### 3. 测试 API

```bash
curl -X POST "http://localhost:5000/translate" \
  -H "Content-Type: application/json" \
  -d '{"q":"Hello","source":"en","target":"zh","format":"text"}'
```

## 🔧 配置 JsonKlingonizer

### 1. 更新配置文件

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
```

## 📊 管理命令

```bash
# 查看容器状态
docker ps | grep libretranslate

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

## 🎯 使用场景

### 场景 1: 个人开发

```bash
# 快速部署到本地
bash scripts/deploy_libretranslate.sh

# 使用默认配置即可
```

### 场景 2: 团队使用

```bash
# 部署到团队服务器
# 修改 docker-compose.yml 中的端口和资源限制
docker-compose up -d

# 配置 Nginx 反向代理
# 参考 docs/LIBRETRANSLATE_SETUP.md
```

### 场景 3: 生产环境

```bash
# 使用 Docker Compose + Nginx + HTTPS
# 启用 API Key 认证
# 配置资源限制和监控
# 参考 docs/LIBRETRANSLATE_SETUP.md 的生产环境部署章节
```

## 🔐 安全建议

1. **启用 API Key**（生产环境必须）
   ```bash
   docker run -d \
     --name libretranslate \
     -p 5000:5000 \
     -e LT_API_KEYS=true \
     libretranslate/libretranslate
   ```

2. **限制访问 IP**
   ```bash
   # 只允许本地访问
   docker run -d -p 127.0.0.1:5000:5000 libretranslate/libretranslate
   ```

3. **使用 HTTPS**（远程访问时必须）
   - 配置 Nginx 反向代理
   - 使用 Let's Encrypt 证书

## 💡 性能优化

1. **增加内存限制**
   ```yaml
   # docker-compose.yml
   deploy:
     resources:
       limits:
         memory: 4G
   ```

2. **预加载语言模型**
   ```bash
   docker exec -it libretranslate bash
   argospm install translate-en_zh
   ```

3. **使用 SSD 存储**
   - 将数据目录放在 SSD 上
   - 提高模型加载速度

## 🐛 故障排除

### 问题 1: 端口被占用
```bash
# 查看占用端口的进程
lsof -i :5000

# 使用其他端口
docker run -d -p 8080:5000 libretranslate/libretranslate
```

### 问题 2: 首次启动很慢
- 正常现象，需要下载语言模型
- 查看日志确认进度：`docker logs -f libretranslate`

### 问题 3: 翻译失败
- 确认服务已完全启动：`curl http://localhost:5000/languages`
- 查看日志：`docker logs libretranslate`

## 📚 延伸阅读

- [LibreTranslate 官方文档](https://github.com/LibreTranslate/LibreTranslate)
- [Argos Translate](https://github.com/argosopentech/argos-translate)
- [Docker 使用指南](https://docs.docker.com/)
- [Nginx 配置指南](https://nginx.org/en/docs/)

## 🆘 获取帮助

如果遇到问题：

1. 查看 `docs/LIBRETRANSLATE_SETUP.md` 的故障排除章节
2. 运行测试脚本：`python scripts/test_libretranslate.py`
3. 查看日志：`docker logs libretranslate`
4. 提交 GitHub Issue

---

**享受自托管的自由和隐私！** 🌍🔒
