FROM python:3.11-alpine

WORKDIR /app

# 安装系统依赖（Alpine 用 apk）
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-client \
    libffi-dev

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
