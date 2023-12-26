import uvicorn
from views import app

if __name__== "__main__":
    uvicorn.run("server:app", reload=True, host="0.0.0.0")
