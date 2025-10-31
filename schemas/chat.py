from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["human", "ai", "system"] = Field(..., description="消息角色")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    question: str = Field(..., description="用户当前问题")
    history: Optional[List[Message]] = Field(default=None, description="历史对话")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="模型回答")


