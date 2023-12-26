from fastapi.responses import JSONResponse

from . import server


@server.post("/logout")
def index():
    response = JSONResponse(content={})
    
    response.delete_cookie("token")

    return response
