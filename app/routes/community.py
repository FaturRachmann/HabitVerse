# app/routes/community.py
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.db.models import User

router = APIRouter()


def page_shell(title: str, body: str) -> str:
    return f"""
    <!doctype html>
    <html lang=\"en\">
    <head>
      <meta charset=\"utf-8\">
      <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
      <title>{title} • HabitVerse</title>
      <script src=\"https://cdn.tailwindcss.com\"></script>
      <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap\" rel=\"stylesheet\">
      <style>
        html,body{{font-family:'Inter',system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif}}
        @keyframes floaty{{0%{{transform:translateY(0) rotate(0deg)}}50%{{transform:translateY(-12px) rotate(3deg)}}100%{{transform:translateY(0) rotate(0deg)}}}}
        .aurora{{filter: blur(60px); opacity:.55; animation: floaty 12s ease-in-out infinite}}
        .glass{{background:rgba(255,255,255,.3); backdrop-filter:blur(18px); border:1px solid rgba(255,255,255,.25); box-shadow:0 8px 30px rgba(31,38,135,.15)}}
        .btn-primary{{background-image:linear-gradient(135deg,#6366F1,#A855F7); color:#fff}}
        .btn-primary:hover{{filter:brightness(1.05)}}
      </style>
    </head>
    <body class="relative bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 text-slate-800">
      <!-- Animated aurora background -->
      <div aria-hidden="true" class="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
        <div class="aurora absolute -top-20 -left-20 w-[380px] h-[380px] bg-gradient-to-br from-indigo-300 to-purple-300 rounded-full"></div>
        <div class="aurora absolute bottom-0 right-[-60px] w-[420px] h-[420px] bg-gradient-to-br from-pink-300 to-rose-300 rounded-full" style="animation-delay: -6s"></div>
      </div>
      <header class="glass backdrop-blur-md border-b border-white/20 text-slate-900">
        <div class="max-w-5xl mx-auto px-4 py-6 flex items-center justify-between">
          <a href="/dashboard" class="text-xl font-semibold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-fuchsia-600">HabitVerse</a>
          <nav class="hidden sm:flex space-x-4 text-sm">
            <a class="hover:underline/50" href="/dashboard">Dashboard</a>
            <a class="hover:underline/50" href="/habits">Habits</a>
            <a class="hover:underline/50" href="/community">Community</a>
          </nav>
        </div>
      </header>
      <main class="max-w-5xl mx-auto px-4 py-6 sm:py-8 pb-24">{body}</main>
      <!-- Mobile bottom nav -->
      <nav class="sm:hidden fixed bottom-0 inset-x-0 bg-white/80 backdrop-blur-md border-t border-slate-200/60 shadow-lg">
        <div class="max-w-5xl mx-auto grid grid-cols-4">
          <a href="/dashboard" class="flex flex-col items-center justify-center py-3 text-[11px] text-slate-700 hover:bg-white/60">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0h6"/></svg>
            Home
          </a>
          <a href="/habits" class="flex flex-col items-center justify-center py-3 text-[11px] text-slate-700 hover:bg-white/60">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8c-1.657 0-3 1.343-3 3v7m6-10a3 3 0 00-3-3m0 0a3 3 0 013 3m-3-3v0"/></svg>
            Habits
          </a>
          <a href="/community" class="flex flex-col items-center justify-center py-3 text-[11px] text-slate-700 hover:bg-white/60">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5V4H2v16h5m10 0V10M7 20v-6"/></svg>
            Community
          </a>
          <a href="/coach" class="flex flex-col items-center justify-center py-3 text-[11px] text-slate-700 hover:bg-white/60">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 18l-3.5 2 1-3.9L6 12.5l4-.3L12 8l2 4.2 4 .3-3.5 3.6 1 3.9z"/></svg>
            Coach
          </a>
        </div>
      </nav>
      <footer class="py-8 text-center text-sm text-slate-500">Grow together • Join a challenge ✨</footer>
    </body>
    </html>
    """


@router.get("/community", response_class=HTMLResponse)
async def community(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Community page with challenges and leaderboard placeholders"""
    body = f"""
      <div class=\"flex items-center justify-between\">
        <div>
          <h1 class=\"text-2xl font-semibold\">Community</h1>
          <p class=\"text-slate-600\">Ikuti tantangan dan naik ke leaderboard.</p>
        </div>
        <a href=\"#\" class=\"px-4 py-2 rounded-lg btn-primary shadow-sm\">Buat Challenge</a>
      </div>

      <div class=\"mt-6 grid gap-6 md:grid-cols-3\">
        <section class=\"md:col-span-2 space-y-3\">
          <h2 class=\"text-lg font-semibold\">Trending Challenges</h2>
          <div class=\"grid gap-3 sm:grid-cols-2\">
            {''.join([
              f'<a href=\"#\" class=\"block p-4 rounded-2xl glass backdrop-blur-xl border border-white/20 shadow-lg ring-1 ring-white/10 hover:shadow-xl transition\"><div class=\"font-medium\">30 Hari {name}</div><div class=\"text-sm text-slate-600\">{members} peserta • hadiah XP</div></a>'
              for name, members in [("Baca", 124), ("Lari Pagi", 98), ("Meditasi", 76), ("No Sugar", 52)]
            ])}
          </div>
        </section>
        <aside class=\"space-y-3\">
          <h2 class=\"text-lg font-semibold\">Leaderboard Minggu Ini</h2>
          <div class=\"rounded-2xl glass backdrop-blur-xl border border-white/20 shadow-lg ring-1 ring-white/10 divide-y divide-white/30\">
            {''.join([
              f'<div class=\"p-3 flex items-center justify-between\"><div class=\"flex items-center gap-3\"><div class=\"w-7 h-7 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center text-sm\">{i}</div><div><div class=\"text-sm font-medium\">{name}</div><div class=\"text-xs text-slate-500\">{xp} XP</div></div></div><div class=\"text-sm text-slate-500\">{streak}🔥</div></div>'
              for i,(name,xp,streak) in enumerate([(current_user.name, 1200, 21),("Alya",1100,16),("Budi",980,12),("Sari",860,10)], start=1)
            ])}
          </div>
        </aside>
      </div>
    """

    return HTMLResponse(content=page_shell("Community", body))
