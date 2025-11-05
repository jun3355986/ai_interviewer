"""
阿里云 text-embedding-v4 模型集成
"""
import os
from typing import List, Optional

import dashscope
from langchain_core.embeddings import Embeddings

from core.config import get_env


DASHSCOPE_API_KEY_ENV = "DASHSCOPE_API_KEY"


class DashScopeEmbeddings(Embeddings):
    """阿里云 DashScope text-embedding-v4 模型"""
    
    def __init__(
        self,
        model: str = "text-embedding-v4",
        api_key: Optional[str] = None,
        dimension: int = 1024,
    ):
        """
        初始化 DashScope Embeddings
        
        Args:
            model: 模型名称，默认 text-embedding-v4
            api_key: API密钥，如果不提供则从环境变量 DASHSCOPE_API_KEY 读取
            dimension: 向量维度，支持 64, 128, 256, 512, 768, 1024, 1536, 2048，默认 1024
        """
        self.model = model
        self.api_key = api_key or get_env(DASHSCOPE_API_KEY_ENV)
        if not self.api_key:
            raise ValueError(
                f"需要配置 {DASHSCOPE_API_KEY_ENV} 环境变量或传入 api_key 参数"
            )
        
        # 设置 dashscope API key
        dashscope.api_key = self.api_key
        
        self.dimension = dimension
    
    def _embed(self, texts: List[str]) -> List[List[float]]:
        """
        批量生成embeddings
        
        Args:
            texts: 文本列表
            
        Returns:
            embeddings列表
        """
        try:
            response = dashscope.TextEmbedding.call(
                model=self.model,
                input=texts,
                dimension=self.dimension,
            )
            
            if response.status_code != 200:
                raise Exception(
                    f"DashScope API 调用失败: {response.status_code}, {response.message}"
                )
            
            # 提取embeddings
            # response.output['embeddings'] 是一个列表，每个元素是 {'embedding': [...]}
            if hasattr(response, 'output') and 'embeddings' in response.output:
                embeddings = []
                for item in response.output['embeddings']:
                    embeddings.append(item['embedding'])
                return embeddings
            else:
                raise Exception(f"DashScope API 返回格式错误: status_code={response.status_code}, response={response}")
            
        except Exception as e:
            raise Exception(f"生成embeddings失败: {str(e)}")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        为文档列表生成embeddings
        
        Args:
            texts: 文档文本列表
            
        Returns:
            embeddings列表
        """
        # DashScope API 限制每批最多 10 个文本
        batch_size = 10
        all_embeddings = []
        
        # 分批处理
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self._embed(batch)
            all_embeddings.extend(batch_embeddings)
        
        return all_embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """
        为查询文本生成embedding
        
        Args:
            text: 查询文本
            
        Returns:
            embedding向量
        """
        try:
            response = dashscope.TextEmbedding.call(
                model=self.model,
                input=[text],
                dimension=self.dimension,
            )
            
            if response.status_code != 200:
                raise Exception(
                    f"DashScope API 调用失败: {response.status_code}, {response.message}"
                )
            
            # 提取embedding
            # response.output['embeddings'][0]['embedding'] 是单个向量
            if response.status_code == 200 and hasattr(response, 'output'):
                return response.output['embeddings'][0]['embedding']
            else:
                raise Exception(f"DashScope API 返回格式错误: status_code={response.status_code}, response={response}")
                
        except Exception as e:
            raise Exception(f"生成query embedding失败: {str(e)}")

