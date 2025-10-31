"""
先引入langchain框架 + deepseek大模型，创建一个简单的对话agent
"""

from typing import List, Dict, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from core.config import get_llm


class Interviewer:
    def __init__(self, model: Optional[str] = None) -> None:
        self.llm = get_llm(model=model)

    def ask(self, question: str, history: Optional[List[Dict]] = None) -> str:
        """
        简单对话接口：
        - question: 当前用户问题
        - history: 形如 [{"role": "human"|"ai"|"system", "content": "..."}] 的历史消息
        返回：模型生成的中文应答字符串
        """
        safe_history = history or []

        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一位专业的高级JAVA开发工程师面试官，要求：\n"
                        "- 问题要简洁明确；\n"
                        "- 回答要结构化，突出重点；\n"
                        "- 必要时指出改进建议，但保持礼貌；"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ])

        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "question": question,
            "history": safe_history,
        })

    """
    循环对话，直到用户说end结束 
    """
    def loop_ask(self, question: str, history: Optional[List[Dict]] = None) -> str:
        # 确保 history 不是 None
        history = history or []
        
        while True:
            answer = self.ask(question, history)
            print(f"\n面试官：{answer}\n")
            # 将 AI 的回答添加到历史记录
            history.append({"role": "ai", "content": answer})
            # 将用户的问题添加到历史记录
            history.append({"role": "human", "content": question})
            
            question = input("请输入你的问题（输入 'end' 结束）：")
            if question.lower().strip() == "end":
                break
        
        return "对话已结束"



# 便于简单本地手动测试：
if __name__ == "__main__":
    interviewer = Interviewer()
    answer = interviewer.loop_ask(question="请扮演面试官，先问一个JAVA相关的开场问题。", history=[])
    print(answer)
