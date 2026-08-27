# PV Jobs India — v1 (Milestone 1)

This is a real, working job board for 4 companies (IQVIA, Parexel, ICON, GSK) —
confirmed live on Workday, pulling actual current postings with working apply
links. No fake data, no placeholder jobs. It currently filters to India-based
locations only.

You do not need to know how to code to get this live. Follow the steps below
exactly, in order. Total time: about 20–30 minutes the first time.

---

## Part A — Test it on your own computer first (5 minutes)

1. **Install Python**: go to https://www.python.org/downloads/ and install it.
   On the very first install screen, **tick "Add Python to PATH"** before
   clicking Install. (Easy to miss — if you skip this, later steps won't work.)

2. **Open a terminal**:
   - Windows: press the Windows key, type `cmd`, press Enter.
   - Mac: open the "Terminal" app (search with Spotlight, Cmd+Space).

3. **Navigate to this folder.** Type `cd ` (with a space after it), then drag
   this folder into the terminal window, then press Enter.

4. **Install the one thing this script needs:**
   ```
   pip install requests
   ```

5. **Run the scraper — this pulls real, live jobs right now:**
   ```
   python scraper.py
   ```
   You'll see it print progress for each company, then say how many India-based
   jobs it found. A new file `jobs.json` appears in the folder — that's the
   real data.

6. **View the website locally:**
   ```
   python -m http.server 8000
   ```
   Now open your browser and go to: `http://localhost:8000`
   You should see real job cards with working "Apply on company site" buttons.
   Click one — it should take you straight to that company's actual posting.
   Press Ctrl+C in the terminal when you're done to stop the server.

If step 6 shows real jobs with real, working links — the whole thing works.
Everything past this point is just about making it live on the internet
instead of only on your computer.

---

## Part B — Put it on the internet for free (15 minutes, one-time setup)

We'll use **GitHub** (free account, stores your code) + **GitHub Pages**
(free hosting for the website) + **GitHub Actions** (a free robot that
re-runs the scraper every hour automatically, forever, at no cost).

1. **Create a GitHub account**: https://github.com/signup (needs your email —
   this is the one signup step only you can do).

2. **Create a new repository**:
   - Click the "+" icon top-right → "New repository"
   - Name it something like `pv-jobs-india`
   - Keep it **Public** (required for free GitHub Pages)
   - Click "Create repository"

3. **Upload these files**: on the new repository's page, click
   "uploading an existing file", then drag in every file and folder from
   this project (including the hidden `.github` folder — if your file
   browser hides it, you may need to show hidden files, or I can walk you
   through uploading it via GitHub's website UI specifically).
   Click "Commit changes".

4. **Turn on GitHub Pages**:
   - In your repository, go to Settings → Pages (left sidebar)
   - Under "Branch", choose `main` and folder `/ (root)`, click Save
   - After a minute, GitHub shows you a live URL like:
     `https://yourusername.github.io/pv-jobs-india/`
   - That URL is your live website. Bookmark it.

5. **Turn on the auto-scraper**:
   - Go to the "Actions" tab in your repository
   - You should see "Update PV Jobs" listed — click it, then click
     "Run workflow" to trigger it once manually and confirm it works
   - After that, it runs automatically every hour by itself, forever,
     for free, and updates the live site — this is the part that solves
     "I found out too late."

That's it — you now have a live, self-updating job board with zero ongoing
cost and zero server to maintain.

---

## What's next (tell me when you're ready for each one)

- **M2**: Add more of your 80 companies (I'll look up their exact Workday/other
  ATS URLs the same way I did for these 4), plus more filters and a
  Telegram/email alert so you get pinged the moment something new matches.
- **M3**: MCQ-based interview prep — a quiz bank of PV interview questions
  with instant scoring, built the same "no server needed" way.
- **M4**: AI mock interview — you answer out loud or by typing, and get
  structured feedback on technical accuracy, confidence/tone, and answer
  clarity. This one needs a small paid API connection (a few cents per
  interview session) since it needs real AI reasoning — I'll explain the
  cost and setup when we get there.

Just tell me "let's add more companies" or "let's build the MCQ prep" whenever
you're ready, and I'll pick up from here — you don't need to remember any of
the technical details in between.
