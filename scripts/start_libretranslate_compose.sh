#!/bin/bash
# 使用 Docker Compose 部署 LibreTranslate

set -e

echo "=========================================="
echo "LibreTranslate Docker Compose 部署"
echo "=========================================="
echo ""

# 检查 docker-compose 是否安装
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null 2>&1; then
    echo "❌ 未安装 docker-compose"
    echo ""
    echo "安装方法："
    echo "  macOS: brew install docker-compose"
    echo "  Linux: sudo apt install docker-compose"
    exit 1
fi

# 创建数据目录
echo "1️⃣  创建数据目录..."
mkdir -p libretranslate-data
echo "✅ 完成"
echo ""

# 启动服务
echo "2️⃣  启动 LibreTranslate 服务..."
echo "   （首次启动需要下载镜像和语言模型，可能需要几分钟）"
echo ""

# 尝试使用新版命令，失败则使用旧版
if docker compose version &> /dev/null 2>&1; then
    docker compose up -d
else
    docker-compose up -d
fi

echo ""
echo "3️⃣  等待服务启动..."
sleep 5

# 查看日志
echo ""
echo "4️⃣  查看启动日志..."
if docker compose version &> /dev/null 2>&1; then
    docker compose logs --tail=20
else
    docker-compose logs --tail=20
fi

echo ""
echo "=========================================="
echo "✅ 部署完成！"
echo "=========================================="
echo ""
echo "📍 服务信息："
echo "   - 地址: http://localhost:5000"
echo "   - Web UI: http://localhost:5000"
echo ""
echo "🔧 管理命令："
echo "   - 查看日志: docker-compose logs -f"
echo "   - 停止服务: docker-compose down"
echo "   - 重启服务: docker-compose restart"
echo "   - 查看状态: docker-compose ps"
echo ""
echo "💡 在浏览器中打开："
if command -v open &> /dev/null; then
    echo "   执行: open http://localhost:5000"
elif command -v xdg-open &> /dev/null; then
    echo "   执行: xdg-open http://localhost:5000"
else
    echo "   访问: http://localhost:5000"
fi
echo ""
