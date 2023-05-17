import logging
from fastapi import APIRouter, Form, Request
from define.ReedV2T2VErrorCode import ReedV2T2VErrorCode
from define.ReedResult import ReedResult
from utils.EnderUtil import TimeUtil

health = APIRouter()

@health.get("/check", tags=["健康检查专用接口"])
async def health_check():
    result = ReedResult.get(ReedV2T2VErrorCode.SUCCESS, "check_time:"+TimeUtil.now())
    return result