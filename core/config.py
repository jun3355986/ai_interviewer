import os
from typing import Optional

from langchain_openai import ChatOpenAI


DEEPSEEK_API_KEY_ENV = "DEEPSEEK_API_KEY"
DEEPSEEK_BASE_URL_ENV = "DEEPSEEK_BASE_URL"
DEEPSEEK_MODEL_ENV = "DEEPSEEK_MODEL"


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value is not None and value != "" else default


def get_llm(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> ChatOpenAI:
    """
    返回配置好的 DeepSeek Chat LLM（OpenAI 兼容）。

    优先使用传入参数，其次读取环境变量：
      - DEEPSEEK_API_KEY（必需）
      - DEEPSEEK_BASE_URL（可选，默认 https://api.deepseek.com/v1）
      - DEEPSEEK_MODEL（可选，默认 deepseek-chat）
    """

    resolved_api_key = api_key or get_env(DEEPSEEK_API_KEY_ENV)
    if not resolved_api_key:
        raise RuntimeError(
            f"缺少 {DEEPSEEK_API_KEY_ENV}，请在环境变量中配置 DeepSeek API Key"
        )

    resolved_base_url = base_url or get_env(DEEPSEEK_BASE_URL_ENV, "https://api.deepseek.com/v1")
    resolved_model = model or get_env(DEEPSEEK_MODEL_ENV, "deepseek-chat")

    # 使用 OpenAI 兼容的 ChatOpenAI 客户端，并指定 base_url 与 api_key
    return ChatOpenAI(
        model=resolved_model,
        api_key=resolved_api_key,
        base_url=resolved_base_url,
        temperature=0.3,
    )


