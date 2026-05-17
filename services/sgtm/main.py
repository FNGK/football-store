"""FastAPI microservice for sGTM click-ID persistence."""

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

from click_id_persistence import build_set_cookie_headers, extract_click_ids

app = FastAPI(title="sGTM Click ID Persistence", version="0.1.0")


class PersistIn(BaseModel):
    url: str
    cookie_domain: str = ""


@app.post("/persist", summary="Capture gclid/fbclid and return Set-Cookie headers")
async def persist(payload: PersistIn, request: Request) -> Response:
    ids = extract_click_ids(payload.url)
    domain = payload.cookie_domain or request.headers.get("host", "").split(":")[0]
    headers = build_set_cookie_headers(ids, domain)
    response = Response(content='{"ok":true}', media_type="application/json")
    for h in headers:
        if "=" in h:
            key, val = h.split("=", 1)
            response.headers.append("Set-Cookie", f"{key}={val}")
    return response
