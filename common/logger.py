from loguru import logger
import sys,os
from contextvars import ContextVar

# 创建一个 ContextVar 来存储 trace_id
trace_id_contextvar: ContextVar[str] = ContextVar("trace_id", default=None)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取上层目录
log_file_path = os.path.join(base_dir, 'logs/app.log')

# 配置 loguru，包含 trace_id
logger.remove()

def trace_id_filter(record):
    trace_id = trace_id_contextvar.get()
    record["extra"]["trace_id"] = trace_id if trace_id else "N/A"
    return True

logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
           "<level>{level: <8}</level> | "
           "Trace ID: <cyan>{extra[trace_id]}</cyan> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
    level="INFO",
    filter=trace_id_filter,
)
logger.add(
    log_file_path,
    rotation="500 MB",
    retention="10 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
           "Trace ID: {extra[trace_id]} | "
           "{name}:{function}:{line} - {message}",
    level="INFO",
    filter=trace_id_filter,
)
