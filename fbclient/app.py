from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()


@app.get('/', response_class=HTMLResponse)
async def get_client_token():
    import os
    base_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_path, 'index.html'), 'r', encoding='utf-8') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


if __name__ == '__main__':
    uvicorn.run(app, port=3333)
