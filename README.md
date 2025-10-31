这是一个 ai 面试助手

## 环境变量
- `DEEPSEEK_API_KEY`: 必填，用于访问 DeepSeek 官方 API。
- `DEEPSEEK_BASE_URL`: 选填，默认 `https://api.deepseek.com/v1`。
- `DEEPSEEK_MODEL`: 选填，默认 `deepseek-chat`。

可在本机临时设置（以 zsh 为例）：
```bash
export DEEPSEEK_API_KEY="your_key_here"
# 可选：
export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
export DEEPSEEK_MODEL="deepseek-chat"
```

## 安装依赖
使用 uv 或 pip 安装：
```bash
# uv（推荐）
uv pip install -e .

# 或 pip
pip install -e .
```

## 代码结构
- `core/config.py`: DeepSeek 与 LangChain 的统一配置与 LLM 工厂。
- `api/interviewer.py`: 使用 LangChain 的面试官对话逻辑。

## 快速测试
```bash
python -m api.interviewer
```

预期：终端输出中文面试开场问题。