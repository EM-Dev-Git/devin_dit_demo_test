import openai
import os
from typing import Dict, Any
from modules.logger import get_logger
from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

class OpenAIClient:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = OPENAI_MODEL
    
    def generate_minutes(self, transcript_content: str) -> str:
        try:
            logger.info("Generating meeting minutes with OpenAI", extra={"model": self.model})
            
            prompt = self._create_minutes_prompt(transcript_content)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは会議の議事録を作成する専門家です。提供されたトランスクリプトから、構造化された議事録を日本語で作成してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            minutes_content = response.choices[0].message.content
            logger.info("Meeting minutes generated successfully")
            return minutes_content
            
        except Exception as e:
            logger.error("Failed to generate meeting minutes", extra={"error": str(e)})
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _create_minutes_prompt(self, transcript_content: str) -> str:
        return f"""
以下のトランスクリプトから議事録を作成してください。

トランスクリプト:
{transcript_content}

以下の形式で議事録を作成してください:


- 日時: [推定される日時または「記載なし」]
- 参加者: [発言者から推定される参加者]
- 議題: [会話内容から推定される主要議題]

[重要な議論ポイントを箇条書きで整理]

[会議で決定された事項があれば記載]

[今後のアクションが必要な項目があれば記載]

[その他重要な情報があれば記載]

構造化された、読みやすい議事録を作成してください。
"""

openai_client = OpenAIClient()
