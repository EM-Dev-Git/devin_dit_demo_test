import structlog
import logging
import os
from dotenv import load_dotenv

load_dotenv()

def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_file_path = os.getenv("LOG_FILE_PATH", "./logs/app.log")
    
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )
    
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

def get_logger(name: str):
    return structlog.get_logger(name)
