import openai
import os
from typing import Dict, Any
from modules.logger import get_logger
from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__)

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        
        if not self.api_key:
            logger.warning("OpenAI API key not configured")
            return
        
        openai.api_key = self.api_key
        logger.info("OpenAI client initialized", extra={"model": self.model})
    
    async def generate_minutes(self, transcript_content: str) -> str:
        if not self.api_key:
            raise Exception("OpenAI API key not configured")
        
        prompt = self._create_minutes_prompt(transcript_content)
        
        try:
            logger.info("Generating minutes with OpenAI", extra={
                "model": self.model,
                "transcript_length": len(transcript_content)
            })
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "あなたは議事録作成の専門家です。与えられたトランスクリプトから構造化された議事録を作成してください。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            minutes_content = response.choices[0].message.content.strip()
            
            logger.info("Minutes generated successfully", extra={
                "minutes_length": len(minutes_content),
                "tokens_used": response.usage.total_tokens
            })
            
            return minutes_content
            
        except Exception as e:
            logger.error("Failed to generate minutes", extra={"error": str(e)})
            raise Exception(f"Failed to generate minutes: {str(e)}")
    
    def _create_minutes_prompt(self, transcript_content: str) -> str:
        return f"""
以下のトランスクリプトから議事録を作成してください。

【要求事項】
1. 会議の概要を簡潔にまとめる
2. 主要な議題と決定事項を整理する
3. アクションアイテムがあれば明記する
4. 参加者の発言を要約する
5. 日本語で出力する

【出力形式】

- 日時: [推定]
- 参加者: [トランスクリプトから推定]
- 議題: [主要議題]

[主要な議論ポイントを整理]

[会議で決定された事項]

[今後のアクション項目]

[その他の重要事項]

【トランスクリプト】
{transcript_content}
"""

openai_client = OpenAIClient()
