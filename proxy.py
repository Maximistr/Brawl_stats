from fastapi import FastAPI, Request
import httpx

app = FastAPI()
API_KEY = "your_brawlstars_api_key"

@app.get("/myip")
async def myip():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.ipify.org?format=json")
    return r.json()

@app.get("/brawlstars/{path:path}")
async def proxy(path: str, request: Request):
    url = f"https://api.brawlstars.com/v1/{path}"
    params = dict(request.query_params)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params=params,
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
    return response.json()