from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel
from common.config_loader import config
from common.upload import upload_file
from common.UpdateStatus import report_status
from common.logger import logger, trace_id_contextvar
from pathlib import Path
import os, subprocess, json, shutil

router = APIRouter()

class CommandRequest(BaseModel):
    nativeAppId: int
    tenantId: int
    apiInfo: dict

workdir = config.get("settings", 'workdir')
out_package_path = config.get('settings', 'out_package_path')

def run_command(full_command, cwd):
    process = subprocess.Popen(
        full_command,
        cwd=cwd,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    
    error_msg = ""
    for line in process.stdout:
        logger.info(f"Output: {line.strip()}")
    for line in process.stderr:
        logger.error(f"Error: {line.strip()}")
        error_msg += line.strip() + "\n"
    
    process.wait()
    return process.returncode, error_msg.strip()

def process_item(item: CommandRequest):
    trace_id = trace_id_contextvar.get()
    if not os.path.isdir(workdir):
        raise HTTPException(status_code=500, detail="Code Directory does not exist")
    
    body_info = item.apiInfo
    report_url = body_info["report"]["url"]
    upload_url = body_info["upload"]["url"]
    headers = {k: str(v) if isinstance(v, bool) else v for k, v in body_info["report"]["headers"].items()}
    headers["X-Trace-Id"] = trace_id
    
    command_path = shutil.which("node")
    full_command = [command_path, "build_android.js", f"t={item.nativeAppId}", f"p={json.dumps(body_info['info'])}"]

    try:
        return_code, error_msg = run_command(full_command, workdir)
        
        if return_code == 0:
            logger.info(f"Command executed successfully! {trace_id}")
            progress = "Packaged"
            out_package = Path(out_package_path) / str(item.nativeAppId)
            apk_file = next(out_package.rglob("*.apk"))
            downloadUrl = upload_file(upload_url, str(apk_file))
            logger.info(f"File synced successfully! {trace_id}")
            report_status(
                nativeAppId=item.nativeAppId,
                progress=progress,
                report_url=report_url,
                header_info=headers,
                download_url=downloadUrl
            )
        else:
            logger.error(f"Command execution failed: {error_msg}, {trace_id}")
            progress = "PackagingFailed"
            report_status(
                nativeAppId=item.nativeAppId,
                progress=progress,
                report_url=report_url,
                header_info=headers,
                error_msg=error_msg
            )
    except Exception as e:
        logger.exception(f"An exception occurred: {e}, {trace_id}")
        report_status(
            nativeAppId=item.nativeAppId,
            progress="PackagingFailed",
            report_url=report_url,
            header_info=headers,
            error_msg=str(e)
        )
    
    logger.info(f"process_item completed, {headers}")
    # logger.info(f"error_msg, {error_msg}")

@router.post("/build", tags=["build"])
async def build_command(
    item: CommandRequest, 
    background_tasks: BackgroundTasks,
    request: Request
):
    trace_id = trace_id_contextvar.get()
    logger.info(f"Received request at {request.url}, trace_id: {trace_id}")
    background_tasks.add_task(process_item, item)
    return {"message": "Request received, packaging process started", "trace_id": trace_id}
