from fastapi import FastAPI, Request
import httpx

app = FastAPI()
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImI5NjQxMmFkLWEzM2UtNGNiNC05MzQxLTg0MmM3MjhjYTNiOCIsImlhdCI6MTc3NDc5MDQ1NSwic3ViIjoiZGV2ZWxvcGVyLzE0ZjhhNjlhLTdlMzQtZWVlYy1jMjlmLTE3OTc5NGRlMzBkNyIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNzQuMjIwLjUxLjI1MCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.6NrFDO1GS-44Ar9v59JJgxyrJel2Gd5GFAuLoRCkaAh365lQPrBH_aXdNDlkLOhI0oWfIB8f7Y1cZk-aDdQEFw"

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