#!/bin/bash
# LibreTranslate 快速部署脚本
# 适用于 macOS 和 Linux

set -e  # 遇到错误立即退出

echo "=========================================="
echo "LibreTranslate 自托管部署脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否安装了 Docker
check_docker() {
    echo "1️⃣  检查 Docker 安装状态..."
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ 未安装 Docker${NC}"
        echo ""
        echo "请先安装 Docker："
        echo ""
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "macOS 安装方式："
            echo "  1. 使用 Homebrew: brew install --cask docker"
            echo "  2. 或从官网下载: https://www.docker.com/products/docker-desktop"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            echo "Linux 安装方式："
            echo "  curl -fsSL https://get.docker.com -o get-docker.sh"
            echo "  sudo sh get-docker.sh"
        fi
        exit 1
    fi
    
    # 检查 Docker 是否运行
    if ! docker info &> /dev/null; then
        echo -e "${RED}❌ Docker 未运行${NC}"
        echo "请启动 Docker Desktop 或运行: sudo systemctl start docker"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker 已安装并运行${NC}"
    docker --version
    echo ""
}

# 检查端口是否被占用
check_port() {
    local port=$1
    echo "2️⃣  检查端口 $port 是否可用..."
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  端口 $port 已被占用${NC}"
        echo ""
        echo "占用端口的进程："
        lsof -i :$port
        echo ""
        echo "请选择操作："
        echo "  1. 停止占用端口的进程"
        echo "  2. 使用其他端口"
        read -p "请选择 [1/2]: " choice
        
        case $choice in
            1)
                pid=$(lsof -t -i:$port)
                echo "正在停止进程 $pid..."
                kill -9 $pid 2>/dev/null || sudo kill -9 $pid
                echo -e "${GREEN}✅ 进程已停止${NC}"
                ;;
            2)
                read -p "请输入新端口号: " port
                echo "将使用端口: $port"
                ;;
            *)
                echo "无效选择，退出"
                exit 1
                ;;
        esac
    else
        echo -e "${GREEN}✅ 端口 $port 可用${NC}"
    fi
    echo ""
    echo "$port"
}

# 创建数据目录
create_data_dir() {
    echo "3️⃣  创建数据目录..."
    
    DATA_DIR="$HOME/libretranslate-data"
    
    if [ -d "$DATA_DIR" ]; then
        echo -e "${YELLOW}⚠️  数据目录已存在: $DATA_DIR${NC}"
        read -p "是否删除并重新创建? [y/N]: " recreate
        if [[ $recreate =~ ^[Yy]$ ]]; then
            rm -rf "$DATA_DIR"
            mkdir -p "$DATA_DIR"
            echo -e "${GREEN}✅ 已重新创建数据目录${NC}"
        fi
    else
        mkdir -p "$DATA_DIR"
        echo -e "${GREEN}✅ 数据目录已创建: $DATA_DIR${NC}"
    fi
    
    echo ""
}

# 拉取 Docker 镜像
pull_image() {
    echo "4️⃣  拉取 LibreTranslate Docker 镜像..."
    echo "   （首次拉取可能需要几分钟，请耐心等待）"
    echo ""
    
    docker pull libretranslate/libretranslate:latest
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 镜像拉取成功${NC}"
    else
        echo -e "${RED}❌ 镜像拉取失败${NC}"
        exit 1
    fi
    echo ""
}

# 停止并删除旧容器
remove_old_container() {
    echo "5️⃣  检查是否存在旧容器..."
    
    if docker ps -a --format '{{.Names}}' | grep -q '^libretranslate$'; then
        echo -e "${YELLOW}⚠️  发现旧容器，正在删除...${NC}"
        docker stop libretranslate 2>/dev/null || true
        docker rm libretranslate 2>/dev/null || true
        echo -e "${GREEN}✅ 旧容器已删除${NC}"
    else
        echo -e "${GREEN}✅ 无旧容器${NC}"
    fi
    echo ""
}

# 启动 LibreTranslate 容器
start_container() {
    local port=$1
    
    echo "6️⃣  启动 LibreTranslate 容器..."
    echo "   端口: $port"
    echo "   数据目录: $DATA_DIR"
    echo ""
    
    docker run -d \
        --name libretranslate \
        -p $port:5000 \
        -v "$DATA_DIR:/home/libretranslate/.local" \
        -e LT_HOST=0.0.0.0 \
        -e LT_DISABLE_WEB_UI=false \
        -e LT_UPDATE_MODELS=true \
        -e LT_CHAR_LIMIT=5000 \
        --restart unless-stopped \
        libretranslate/libretranslate:latest
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 容器已启动${NC}"
    else
        echo -e "${RED}❌ 容器启动失败${NC}"
        exit 1
    fi
    echo ""
}

# 等待服务启动
wait_for_service() {
    local port=$1
    local max_attempts=30
    local attempt=0
    
    echo "7️⃣  等待服务启动..."
    echo "   （首次启动需要下载语言模型，可能需要几分钟）"
    echo ""
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s "http://localhost:$port/languages" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ 服务已就绪！${NC}"
            return 0
        fi
        
        attempt=$((attempt + 1))
        echo "   尝试 $attempt/$max_attempts - 等待中..."
        sleep 2
    done
    
    echo -e "${RED}❌ 服务启动超时${NC}"
    echo "请查看日志: docker logs libretranslate"
    return 1
}

# 测试服务
test_service() {
    local port=$1
    
    echo ""
    echo "8️⃣  测试翻译服务..."
    echo ""
    
    # 测试翻译
    response=$(curl -s -X POST "http://localhost:$port/translate" \
        -H "Content-Type: application/json" \
        -d '{
            "q": "Hello, World!",
            "source": "en",
            "target": "zh",
            "format": "text"
        }')
    
    if echo "$response" | grep -q "translatedText"; then
        translated=$(echo "$response" | grep -o '"translatedText":"[^"]*"' | cut -d'"' -f4)
        echo -e "${GREEN}✅ 翻译测试成功！${NC}"
        echo "   原文: Hello, World!"
        echo "   译文: $translated"
    else
        echo -e "${YELLOW}⚠️  翻译测试失败，但服务可能正在下载模型${NC}"
        echo "   响应: $response"
    fi
    echo ""
}

# 显示使用说明
show_usage() {
    local port=$1
    
    echo "=========================================="
    echo "✅ LibreTranslate 部署完成！"
    echo "=========================================="
    echo ""
    echo "📍 服务信息："
    echo "   - 地址: http://localhost:$port"
    echo "   - Web UI: http://localhost:$port"
    echo "   - API: http://localhost:$port/translate"
    echo "   - 数据目录: $DATA_DIR"
    echo ""
    echo "🎯 快速使用："
    echo ""
    echo "1. 在浏览器中打开 Web UI："
    echo "   open http://localhost:$port"
    echo ""
    echo "2. 使用 JsonKlingonizer 翻译："
    echo "   python main.py -i data/input/en.json -o data/output/zh.json \\"
    echo "     --translator libre --source en --target zh --use-cache"
    echo ""
    echo "3. 测试 API："
    echo "   curl -X POST \"http://localhost:$port/translate\" \\"
    echo "     -H \"Content-Type: application/json\" \\"
    echo "     -d '{\"q\":\"Hello\",\"source\":\"en\",\"target\":\"zh\",\"format\":\"text\"}'"
    echo ""
    echo "📚 容器管理："
    echo "   - 查看日志: docker logs -f libretranslate"
    echo "   - 停止服务: docker stop libretranslate"
    echo "   - 启动服务: docker start libretranslate"
    echo "   - 重启服务: docker restart libretranslate"
    echo "   - 删除容器: docker rm -f libretranslate"
    echo "   - 查看状态: docker ps"
    echo ""
    echo "🔧 更新配置文件："
    echo "   编辑 config/config.json，修改以下内容："
    echo "   {"
    echo "     \"translator\": {\"type\": \"libre\"},"
    echo "     \"api\": {"
    echo "       \"libre_url\": \"http://localhost:$port/translate\","
    echo "       \"libre_api_key\": null"
    echo "     }"
    echo "   }"
    echo ""
    echo "📖 详细文档："
    echo "   查看 docs/LIBRETRANSLATE_SETUP.md"
    echo ""
}

# 主函数
main() {
    # 默认端口
    PORT=5000
    
    # 检查 Docker
    check_docker
    
    # 检查端口
    PORT=$(check_port $PORT)
    
    # 创建数据目录
    create_data_dir
    
    # 拉取镜像
    pull_image
    
    # 删除旧容器
    remove_old_container
    
    # 启动容器
    start_container $PORT
    
    # 等待服务启动
    if wait_for_service $PORT; then
        # 测试服务
        test_service $PORT
        
        # 显示使用说明
        show_usage $PORT
    else
        echo ""
        echo "服务可能仍在初始化中，请稍后使用以下命令检查："
        echo "  docker logs -f libretranslate"
        echo ""
    fi
}

# 执行主函数
main
