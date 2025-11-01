# LibreTranslate 自托管部署指南

## 📦 什么是 LibreTranslate？

LibreTranslate 是一个**完全开源、免费、可自托管**的机器翻译 API，基于 Argos Translate 引擎。

### 优势
- ✅ **完全免费**：无使用限制，无需 API Key
- ✅ **隐私友好**：数据不会发送到第三方服务器
- ✅ **离线可用**：可以完全离线运行
- ✅ **可控性强**：可以自定义翻译模型和参数
- ✅ **无速率限制**：自己的服务器，想翻译多少翻译多少

## 🚀 部署方式

### 方式 1: Docker 部署（推荐）

#### 1.1 安装 Docker

**macOS**:
```bash
# 使用 Homebrew 安装
brew install --cask docker

# 或从官网下载
# https://www.docker.com/products/docker-desktop
```

**Linux**:
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker
```

#### 1.2 运行 LibreTranslate 容器

**基础部署**（端口 5000）:
```bash
# 拉取镜像并运行
docker run -d \
  --name libretranslate \
  -p 5000:5000 \
  libretranslate/libretranslate

# 访问：http://localhost:5000
```

**高级配置**（推荐）:
```bash
# 创建数据目录（用于持久化翻译模型）
mkdir -p ~/libretranslate-data

# 运行容器
docker run -d \
  --name libretranslate \
  -p 5000:5000 \
  -v ~/libretranslate-data:/home/libretranslate/.local \
  -e LT_DISABLE_WEB_UI=false \
  -e LT_UPDATE_MODELS=true \
  --restart unless-stopped \
  libretranslate/libretranslate
```

**参数说明**:
- `-p 5000:5000`: 映射端口 5000
- `-v ~/libretranslate-data:/home/libretranslate/.local`: 持久化数据
- `-e LT_DISABLE_WEB_UI=false`: 启用 Web 界面
- `-e LT_UPDATE_MODELS=true`: 自动更新翻译模型
- `--restart unless-stopped`: 自动重启

#### 1.3 验证部署

```bash
# 检查容器状态
docker ps

# 查看日志
docker logs libretranslate

# 测试 API
curl -X POST "http://localhost:5000/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "Hello, World!",
    "source": "en",
    "target": "zh",
    "format": "text"
  }'
```

#### 1.4 管理容器

```bash
# 停止容器
docker stop libretranslate

# 启动容器
docker start libretranslate

# 重启容器
docker restart libretranslate

# 删除容器
docker rm -f libretranslate

# 查看资源使用
docker stats libretranslate
```

---

### 方式 2: Python 直接安装

#### 2.1 系统要求

- Python 3.8 或更高版本
- 至少 2GB RAM
- 足够的磁盘空间（翻译模型可能需要几百 MB）

#### 2.2 安装步骤

```bash
# 创建虚拟环境
python3 -m venv libretranslate-env
source libretranslate-env/bin/activate  # macOS/Linux
# Windows: libretranslate-env\Scripts\activate

# 安装 LibreTranslate
pip install libretranslate

# 或从源代码安装（最新版本）
pip install git+https://github.com/LibreTranslate/LibreTranslate.git
```

#### 2.3 启动服务

**基础启动**:
```bash
libretranslate
# 默认运行在 http://127.0.0.1:5000
```

**自定义配置**:
```bash
# 指定端口
libretranslate --port 8080

# 允许所有 IP 访问
libretranslate --host 0.0.0.0

# 禁用 Web UI
libretranslate --disable-web-ui

# 启用 API Key 认证
libretranslate --api-keys

# 组合使用
libretranslate --host 0.0.0.0 --port 5000 --update-models
```

#### 2.4 配置文件方式

创建配置文件 `libretranslate-config.json`:
```json
{
  "host": "0.0.0.0",
  "port": 5000,
  "char_limit": 5000,
  "req_limit": 100,
  "batch_limit": 10,
  "ga_id": "",
  "disable_files_translation": false,
  "disable_web_ui": false,
  "update_models": true,
  "api_keys": false
}
```

启动:
```bash
libretranslate --config libretranslate-config.json
```

---

### 方式 3: Docker Compose（生产环境推荐）

#### 3.1 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  libretranslate:
    image: libretranslate/libretranslate:latest
    container_name: libretranslate
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - ./libretranslate-data:/home/libretranslate/.local
    environment:
      - LT_HOST=0.0.0.0
      - LT_PORT=5000
      - LT_DISABLE_WEB_UI=false
      - LT_UPDATE_MODELS=true
      - LT_CHAR_LIMIT=5000
      - LT_REQ_LIMIT=100
      - LT_BATCH_LIMIT=10
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### 3.2 启动服务

```bash
# 启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down

# 重启
docker-compose restart
```

---

## 🔧 配置 JsonKlingonizer 使用本地 LibreTranslate

### 1. 修改配置文件

编辑 `config/config.json`:

```json
{
  "translator": {
    "type": "libre",
    "source_lang": "auto",
    "target_lang": "zh"
  },
  "api": {
    "libre_url": "http://localhost:5000/translate",
    "libre_api_key": null
  }
}
```

### 2. 使用本地 LibreTranslate

```bash
# 确保 LibreTranslate 正在运行
docker ps | grep libretranslate

# 使用本地服务翻译
python main.py -i data/input/en.json -o data/output/zh.json \
  --translator libre \
  --source en \
  --target zh \
  --use-cache
```

---

## 🌐 远程访问配置

### 1. 使用 Nginx 反向代理

安装 Nginx:
```bash
# macOS
brew install nginx

# Ubuntu/Debian
sudo apt install nginx
```

配置文件 `/etc/nginx/sites-available/libretranslate`:
```nginx
server {
    listen 80;
    server_name translate.yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置（翻译可能需要较长时间）
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
    }
}
```

启用配置:
```bash
sudo ln -s /etc/nginx/sites-available/libretranslate /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 2. 使用 HTTPS（Let's Encrypt）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d translate.yourdomain.com

# 自动续期
sudo certbot renew --dry-run
```

---

## 🔐 安全配置

### 1. 启用 API Key 认证

**Docker 方式**:
```bash
docker run -d \
  --name libretranslate \
  -p 5000:5000 \
  -e LT_API_KEYS=true \
  -e LT_API_KEYS_DB_PATH=/home/libretranslate/.local/api_keys.db \
  libretranslate/libretranslate
```

**生成 API Key**:
```bash
# 进入容器
docker exec -it libretranslate bash

# 生成 API Key
ltmanage keys add my-secret-key

# 查看所有 API Key
ltmanage keys
```

### 2. 配置使用 API Key

修改 `config/config.json`:
```json
{
  "api": {
    "libre_url": "http://localhost:5000/translate",
    "libre_api_key": "my-secret-key"
  }
}
```

### 3. 限制访问

**只允许本地访问**:
```bash
docker run -d \
  --name libretranslate \
  -p 127.0.0.1:5000:5000 \
  libretranslate/libretranslate
```

**使用防火墙**:
```bash
# Ubuntu/Debian (ufw)
sudo ufw allow from 192.168.1.0/24 to any port 5000
sudo ufw deny 5000
```

---

## 📊 性能优化

### 1. 增加内存限制

```bash
docker run -d \
  --name libretranslate \
  -p 5000:5000 \
  --memory="4g" \
  --memory-swap="4g" \
  libretranslate/libretranslate
```

### 2. 使用 GPU 加速（如果有 NVIDIA GPU）

```bash
# 安装 nvidia-docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# 运行容器
docker run -d \
  --name libretranslate \
  --gpus all \
  -p 5000:5000 \
  libretranslate/libretranslate
```

### 3. 预加载翻译模型

```bash
# 进入容器
docker exec -it libretranslate bash

# 下载常用语言对的模型
cd /home/libretranslate/.local/share/argos-translate/packages
argospm install translate-en_zh
argospm install translate-zh_en
argospm install translate-en_ja
argospm install translate-ja_en
```

---

## 🔍 监控和维护

### 1. 健康检查

```bash
# 检查服务状态
curl http://localhost:5000/health

# 获取支持的语言列表
curl http://localhost:5000/languages
```

### 2. 日志管理

```bash
# 实时查看日志
docker logs -f libretranslate

# 查看最后 100 行
docker logs --tail 100 libretranslate

# 保存日志到文件
docker logs libretranslate > libretranslate.log 2>&1
```

### 3. 备份和恢复

```bash
# 备份数据
docker cp libretranslate:/home/libretranslate/.local ./libretranslate-backup

# 恢复数据
docker cp ./libretranslate-backup libretranslate:/home/libretranslate/.local
docker restart libretranslate
```

---

## 🆚 LibreTranslate vs Google Translate

| 特性 | LibreTranslate | Google Translate (googletrans) |
|------|----------------|-------------------------------|
| 费用 | 完全免费 | 免费（非官方） |
| 隐私 | 完全私有 | 数据发送到 Google |
| 稳定性 | 非常稳定 | 可能不稳定 |
| 速率限制 | 无限制 | 可能被封 IP |
| 翻译质量 | 良好 | 优秀 |
| 离线使用 | 支持 | 不支持 |
| 部署复杂度 | 中等 | 简单 |
| 维护成本 | 需要服务器 | 无 |

---

## 💡 最佳实践

1. **开发环境**：使用 Docker 快速部署
2. **生产环境**：使用 Docker Compose + Nginx + HTTPS
3. **高并发**：增加内存限制，考虑使用多个实例 + 负载均衡
4. **安全性**：启用 API Key，限制访问 IP
5. **性能**：预加载常用语言模型，使用 SSD
6. **监控**：配置健康检查和日志监控

---

## 🐛 常见问题

### Q1: 容器启动失败
```bash
# 检查端口是否被占用
lsof -i :5000

# 使用其他端口
docker run -d -p 8080:5000 libretranslate/libretranslate
```

### Q2: 翻译速度慢
- 首次翻译需要下载模型，之后会快很多
- 增加容器内存限制
- 使用 SSD 存储
- 考虑使用 GPU 加速

### Q3: 支持的语言较少
```bash
# 安装更多语言包
docker exec -it libretranslate bash
argospm install translate-[source]_[target]
```

### Q4: 内存占用高
- 这是正常的，翻译模型需要较多内存
- 可以限制同时处理的请求数量
- 使用较小的语言模型

---

## 📚 参考资源

- [LibreTranslate 官方文档](https://github.com/LibreTranslate/LibreTranslate)
- [Argos Translate](https://github.com/argosopentech/argos-translate)
- [Docker 文档](https://docs.docker.com/)
- [Nginx 文档](https://nginx.org/en/docs/)
