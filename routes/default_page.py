from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse) 
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>My FastAPI App</title>
        </head>
        <body>
            <h1>Sever is running!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
