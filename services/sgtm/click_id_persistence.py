"""
Server-Side GTM Click ID Persistence endpoint.

Intercepts page requests, captures gclid/fbclid, writes HTTP-only first-party cookies
to survive iOS 17 Link Tracking Protection and Safari ITP.
"""

from http.cookies import SimpleCookie
from urllib.parse import parse_qs, urlparse

CLICK_COOKIE_MAX_AGE = 60 * 60 * 24 * 90  # 90 days
GCLID_COOKIE = "_amp_gclid"
FBCLID_COOKIE = "_amp_fbclid"


def extract_click_ids(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    out: dict[str, str] = {}
    if gclid := params.get("gclid", [None])[0]:
        out["gclid"] = gclid
    if fbclid := params.get("fbclid", [None])[0]:
        out["fbclid"] = fbclid
    return out


def build_set_cookie_headers(click_ids: dict[str, str], domain: str) -> list[str]:
    headers: list[str] = []
    cookie = SimpleCookie()
    if gclid := click_ids.get("gclid"):
        cookie[GCLID_COOKIE] = gclid
        cookie[GCLID_COOKIE]["httponly"] = True
        cookie[GCLID_COOKIE]["secure"] = True
        cookie[GCLID_COOKIE]["samesite"] = "Lax"
        cookie[GCLID_COOKIE]["path"] = "/"
        cookie[GCLID_COOKIE]["max-age"] = CLICK_COOKIE_MAX_AGE
        if domain:
            cookie[GCLID_COOKIE]["domain"] = domain
        headers.append(cookie.output(header="").strip())
    if fbclid := click_ids.get("fbclid"):
        cookie[FBCLID_COOKIE] = fbclid
        cookie[FBCLID_COOKIE]["httponly"] = True
        cookie[FBCLID_COOKIE]["secure"] = True
        cookie[FBCLID_COOKIE]["samesite"] = "Lax"
        cookie[FBCLID_COOKIE]["path"] = "/"
        cookie[FBCLID_COOKIE]["max-age"] = CLICK_COOKIE_MAX_AGE
        if domain:
            cookie[FBCLID_COOKIE]["domain"] = domain
        headers.append(cookie.output(header="").strip())
    return headers
