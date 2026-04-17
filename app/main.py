from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import user, items

app=FastAPI()


# utilising user from routes, all the routes defined inside users route will come as we have included routes within context of app
app.include_router(user.router)

app.include_router(items.router)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}