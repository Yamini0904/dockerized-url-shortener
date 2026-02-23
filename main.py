from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
import random
import string

from database import engine, get_db
from models import Base, URL, ClickLog

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# -------------------------
# API KEY SECURITY
# -------------------------

API_KEY = "mysecretkey123"

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")


# -------------------------
# Utility: Generate Short Code
# -------------------------

def generate_short_code(length: int = 6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# -------------------------
# Root Endpoint
# -------------------------

@app.get("/")
def read_root():
    return {"message": "Secure URL Analytics Platform Running"}


# -------------------------
# Shorten URL (Protected)
# -------------------------

@app.post("/shorten")
def shorten_url(
    original_url: str,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    short_code = generate_short_code()

    # Ensure unique short code
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    new_url = URL(
        original_url=original_url,
        short_code=short_code
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "short_url": f"http://127.0.0.1:8000/{new_url.short_code}"
    }


# -------------------------
# Redirect (Public)
# -------------------------

@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()

    if url:
        # Increment click count
        url.click_count += 1

        # Log click event
        click_entry = ClickLog(url_id=url.id)
        db.add(click_entry)

        db.commit()

        return RedirectResponse(url.original_url)

    return {"error": "URL not found"}


# -------------------------
# Analytics Summary (Protected)
# -------------------------

@app.get("/analytics/summary")
def get_analytics_summary(
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key)
):
    # Total URLs
    total_urls = db.query(func.count(URL.id)).scalar()

    # Total clicks
    total_clicks = db.query(func.sum(URL.click_count)).scalar()
    if total_clicks is None:
        total_clicks = 0

    # Top 5 URLs
    top_urls_data = (
        db.query(URL.short_code, URL.click_count)
        .order_by(URL.click_count.desc())
        .limit(5)
        .all()
    )

    top_urls = []
    for url in top_urls_data:
        top_urls.append({
            "short_code": url.short_code,
            "clicks": url.click_count
        })

    # Clicks today
    today = date.today()
    clicks_today = (
        db.query(func.count(ClickLog.id))
        .filter(func.date(ClickLog.timestamp) == today)
        .scalar()
    )

    return {
        "total_urls": total_urls,
        "total_clicks": total_clicks,
        "top_urls": top_urls,
        "clicks_today": clicks_today
    }