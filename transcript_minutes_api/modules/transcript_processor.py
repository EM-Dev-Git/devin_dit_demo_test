import json
from typing import Dict, Any
from fastapi import UploadFile, HTTPException
from modules.logger import get_logger

logger = get_logger(__name__)

class TranscriptProcessor:
    ALLOWED_EXTENSIONS = {'.txt', '.json'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    def __init__(self):
        pass
    
    async def process_file(self, file: UploadFile) -> str:
        try:
            logger.info("Processing transcript file", extra={"filename": file.filename})
            
            self._validate_file(file)
            
            content = await file.read()
            
            if len(content) > self.MAX_FILE_SIZE:
                raise HTTPException(status_code=413, detail="File too large")
            
            text_content = self._extract_text_content(content, file.filename)
            processed_content = self._preprocess_content(text_content)
            
            logger.info("Transcript file processed successfully", extra={"filename": file.filename})
            return processed_content
            
        except Exception as e:
            logger.error("Failed to process transcript file", extra={"filename": file.filename, "error": str(e)})
            raise HTTPException(status_code=400, detail=f"Failed to process file: {str(e)}")
    
    def _validate_file(self, file: UploadFile):
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_extension = self._get_file_extension(file.filename)
        if file_extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed types: {', '.join(self.ALLOWED_EXTENSIONS)}"
            )
    
    def _get_file_extension(self, filename: str) -> str:
        return '.' + filename.split('.')[-1].lower() if '.' in filename else ''
    
    def _extract_text_content(self, content: bytes, filename: str) -> str:
        file_extension = self._get_file_extension(filename)
        
        try:
            if file_extension == '.txt':
                return content.decode('utf-8')
            elif file_extension == '.json':
                json_data = json.loads(content.decode('utf-8'))
                return self._extract_from_json(json_data)
            else:
                raise ValueError(f"Unsupported file extension: {file_extension}")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File encoding not supported. Please use UTF-8.")
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
    
    def _extract_from_json(self, json_data: Dict[Any, Any]) -> str:
        if isinstance(json_data, dict):
            if 'transcript' in json_data:
                return str(json_data['transcript'])
            elif 'text' in json_data:
                return str(json_data['text'])
            elif 'content' in json_data:
                return str(json_data['content'])
            else:
                return json.dumps(json_data, ensure_ascii=False, indent=2)
        elif isinstance(json_data, list):
            return '\n'.join([str(item) for item in json_data])
        else:
            return str(json_data)
    
    def _preprocess_content(self, content: str) -> str:
        content = content.strip()
        
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)

transcript_processor = TranscriptProcessor()
