from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.bootstrap import bootstrap
from app.utils.common import APP_TITLE, APP_VERSION, APP_DESCRIPTION
from app.core.lifespan import lifespan

app=FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    docs_url="/docs",
    lifespan=lifespan,
)

bootstrap(app)
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}