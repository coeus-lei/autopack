from fastapi import Request
import uuid
from common.logger import trace_id_contextvar

async def add_trace_id_middleware(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    trace_id_contextvar.set(trace_id)
    request.state.trace_id = trace_id

    response = await call_next(request)
    response.headers["X-Trace-ID"] = trace_id

    return response
