"""
PV Jobs India — Workday Scraper (v1)

WHAT THIS DOES:
Pulls REAL, LIVE job postings directly from each company's own Workday
careers API (the same one their own careers website calls in your browser).
No fake data, no guessed links — every job in the output has a working
"apply_url" that goes straight to that company's real job posting.

HOW TO RUN THIS (no coding knowledge needed — just copy/paste):
  1. Install Python from https://www.python.org/downloads/
     (On the install screen, TICK the box "Add Python to PATH" before clicking Install)
  2. Open a terminal / command prompt in this folder
  3. Run:  pip install requests
  4. Run:  python scraper.py
  5. A file called jobs.json will appear in this folder with the live results.

This script currently covers the companies listed in companies_config.json.
To add more companies later, just add another entry to that file with the
same tenant/wd_pod/site fields (I can look those up for any company you name).
"""

import json
import time
import requests
from datetime import datetime, timezone

CONFIG_FILE = "companies_config.json"
OUTPUT_FILE = "jobs.json"

# India-related location keywords — a job is kept if ANY of these appear
# in its location text. Extend this list any time.
INDIA_KEYWORDS = [
    "india", "bengaluru", "bangalore", "hyderabad", "mumbai", "pune",
    "chennai", "delhi", "gurugram", "gurgaon", "noida", "kochi",
    "ahmedabad", "vadodara", "navi mumbai", "kolkata"
]

# Very simple, transparent keyword rules to tell PV roles apart from
# other pharma/clinical roles. Extend freely.
PV_KEYWORDS = [
    "pharmacovigilance", "drug safety", "case processing", "signal detection",
    "signal management", "aggregate report", "psur", "pbrer", "icsr",
    "safety database", "argus safety", "medical safety review",
    "adverse event", "safety physician", "safety scientist"
]

OTHER_PHARMA_KEYWORDS = [
    "regulatory affairs", "clinical research associate", "cra ",
    "quality assurance", "medical writer", "medical writing",
    "biostatistic", "clinical data", "clinical trial", "regulatory affairs"
]


def classify_job(title: str) -> str:
    t = title.lower()
    if any(k in t for k in PV_KEYWORDS):
        return "PV"
    if any(k in t for k in OTHER_PHARMA_KEYWORDS):
        return "Pharma - Other"
    return "Other"


def is_india_job(location_text: str) -> bool:
    loc = (location_text or "").lower()
    return any(k in loc for k in INDIA_KEYWORDS)


def fetch_company_jobs(company: dict, all_locations: bool = False) -> list:
    """Pull every job posting for one Workday-powered company."""
    tenant = company["tenant"]
    wd_pod = company["wd_pod"]
    site = company["site"]
    base = f"https://{tenant}.{wd_pod}.myworkdayjobs.com"
    api_url = f"{base}/wday/cxs/{tenant}/{site}/jobs"

    results = []
    offset = 0
    limit = 20
    headers = {"Content-Type": "application/json"}

    while True:
        payload = {"appliedFacets": {}, "limit": limit, "offset": offset, "searchText": ""}
        try:
            resp = requests.post(api_url, json=payload, headers=headers, timeout=20)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"  [!] Error fetching {company['name']} at offset {offset}: {e}")
            break

        postings = data.get("jobPostings", [])
        if not postings:
            break

        for p in postings:
            location_text = p.get("locationsText", "")
            if not all_locations and not is_india_job(location_text):
                continue

            title = p.get("title", "").strip()
            external_path = p.get("externalPath", "")
            posted_on = p.get("postedOn", "")
            req_id = ""
            for bf in p.get("bulletFields", []):
                if bf:
                    req_id = bf
                    break

            apply_url = f"{base}/{site}{external_path}"

            results.append({
                "company": company["name"],
                "title": title,
                "location": location_text,
                "posted_on": posted_on,
                "req_id": req_id,
                "apply_url": apply_url,
                "category": classify_job(title),
                "source": "Workday (direct)",
            })

        total = data.get("total", 0)
        offset += limit
        if offset >= total:
            break
        time.sleep(0.5)  # be polite to the server

    return results


def main():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        companies = json.load(f)

    all_jobs = []
    for company in companies:
        print(f"Fetching {company['name']}...")
        jobs = fetch_company_jobs(company)
        print(f"  -> {len(jobs)} India-based postings found")
        all_jobs.extend(jobs)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_jobs": len(all_jobs),
        "jobs": all_jobs,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {len(all_jobs)} total India-based jobs written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
