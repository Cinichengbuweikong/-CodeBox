from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response, Depends
from fastapi.responses import JSONResponse

from depends.userInfoDependence import userInfo
from models.Users import Users
from schemas.operationResponseSchema import OpreationResponseSchema
from constants import ResopnseOperationResultType



class CheckUserPermissionsMiddleware(BaseHTTPMiddleware):
    """
    检查当前请求用户是否有权限访问后台接口 如果有的话则放行 如果没有的话则拦截用户
    我们认为 用户中 uid=0 的用户为网站的管理员
    """

    async def dispatch(
        self, 
        request: Request,
        call_next: RequestResponseEndpoint,
        user: Users | None = Depends(userInfo)
    ) -> Response:
        
        if user == None:
            return JSONResponse(
                content=OpreationResponseSchema(
                    code=403,
                    result=ResopnseOperationResultType.FAIL,
                    reason="user not login"
                ).model_dump()
            )
        
        if user.uid != 0:
            return JSONResponse(
                content=OpreationResponseSchema(
                    code=403,
                    result=ResopnseOperationResultType.FAIL,
                    reason="forbidden"
                ).model_dump()
            )
        
        response = await call_next(request)

        return response