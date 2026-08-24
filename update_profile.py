import json
import os
import urllib.request
from datetime import datetime, timezone
from html import escape

USERNAME = os.getenv("GITHUB_REPOSITORY_OWNER", "fdogukanctk")

TITLE = "Full Stack Developer"
SUBTITLE = "Building things, breaking bugs, shipping fixes"
STACK = "C#, .NET, React, TypeScript, PostgreSQL"
TOOLS = "VS Code, Cursor, Docker, Git"
LANGS = "Turkish, English"
HOBBIES = "Coding, UI/UX, Automation"

GRAPHQL_URL = "https://api.github.com/graphql"


def graphql(query, variables):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN bulunamadı.")

    payload = json.dumps(
        {
            "query": query,
            "variables": variables,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "github-profile-generator",
        },
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    if result.get("errors"):
        raise RuntimeError(result["errors"])

    return result["data"]


def get_profile():
    query = """
    query($login: String!) {
      user(login: $login) {
        login
        name
        createdAt
        followers {
          totalCount
        }
        repositories(
          first: 100
          ownerAffiliations: OWNER
          privacy: PUBLIC
          isFork: false
        ) {
          totalCount
          nodes {
            stargazerCount
            primaryLanguage {
              name
            }
          }
        }
        contributionsCollection {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          restrictedContributionsCount
        }
      }
    }
    """

    data = graphql(query, {"login": USERNAME})
    user = data["user"]

    if user is None:
        raise RuntimeError(f"Kullanıcı bulunamadı: {USERNAME}")

    repositories = user["repositories"]["nodes"]
    stars = sum(repo["stargazerCount"] for repo in repositories)

    languages = {}
    for repo in repositories:
        language = repo.get("primaryLanguage")
        if language:
            name = language["name"]
            languages[name] = languages.get(name, 0) + 1

    top_languages = sorted(
        languages.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:5]

    created_at = datetime.fromisoformat(user["createdAt"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    account_days = (now - created_at).days

    contributions = user["contributionsCollection"]

    return {
        "login": user["login"],
        "name": user["name"] or user["login"],
        "followers": user["followers"]["totalCount"],
        "repos": user["repositories"]["totalCount"],
        "stars": stars,
        "commits": contributions["totalCommitContributions"],
        "pull_requests": contributions["totalPullRequestContributions"],
        "issues": contributions["totalIssueContributions"],
        "private_contributions": contributions["restrictedContributionsCount"],
        "account_days": account_days,
        "top_languages": ", ".join(name for name, _ in top_languages) or "N/A",
    }


def info_row(x, y, label, value, label_color, value_color):
    return f"""
    <text x="{x}" y="{y}" font-size="18" font-family="monospace">
      <tspan fill="{label_color}" font-weight="700">{escape(label)}</tspan>
      <tspan fill="{value_color}"> {escape(str(value))}</tspan>
    </text>
    """


def small_badge(x, y, text, fill, stroke, color):
    width = max(120, 12 * len(text))
    return f"""
    <rect x="{x}" y="{y}" rx="14" ry="14" width="{width}" height="34" fill="{fill}" stroke="{stroke}" />
    <text x="{x + 16}" y="{y + 22}" fill="{color}" font-size="14" font-family="monospace">{escape(text)}</text>
    """


def create_monkey_panel():
    return """
    <g>
      <rect x="35" y="35" width="420" height="650" rx="24" fill="#0a1220" stroke="#1c2b45" />
      <rect x="55" y="55" width="380" height="110" rx="18" fill="#0d1728" stroke="#1f3458" />

      <text x="78" y="92" fill="#35c2ff" font-size="20" font-family="monospace">$ whoami</text>
      <text x="78" y="122" fill="#9ecbff" font-size="18" font-family="monospace">coder-monkey --mode=focus</text>
      <circle cx="400" cy="90" r="8" fill="#3fb950"/>
      <text x="385" y="125" fill="#8b949e" font-size="13" font-family="monospace">online</text>

      <ellipse cx="245" cy="370" rx="105" ry="120" fill="#8b5e3c" />
      <ellipse cx="245" cy="385" rx="76" ry="88" fill="#d9b38c" />

      <ellipse cx="188" cy="292" rx="26" ry="34" fill="#8b5e3c" />
      <ellipse cx="302" cy="292" rx="26" ry="34" fill="#8b5e3c" />
      <ellipse cx="188" cy="294" rx="15" ry="20" fill="#d9b38c" />
      <ellipse cx="302" cy="294" rx="15" ry="20" fill="#d9b38c" />

      <ellipse cx="215" cy="360" rx="13" ry="16" fill="#ffffff"/>
      <ellipse cx="275" cy="360" rx="13" ry="16" fill="#ffffff"/>
      <circle cx="218" cy="362" r="6" fill="#0d1117"/>
      <circle cx="272" cy="362" r="6" fill="#0d1117"/>

      <ellipse cx="245" cy="408" rx="18" ry="13" fill="#6b4226" />
      <path d="M225 435 Q245 452 265 435" stroke="#6b4226" stroke-width="5" fill="none" stroke-linecap="round"/>

      <path d="M160 470 Q245 545 330 470 L340 620 Q245 650 150 620 Z" fill="#111827" stroke="#23324d" />
      <path d="M190 470 Q245 510 300 470" stroke="#35c2ff" stroke-width="3" fill="none" opacity="0.9"/>
      <path d="M245 510 L245 620" stroke="#23324d" stroke-width="3"/>

      <rect x="120" y="555" width="250" height="52" rx="10" fill="#0d1728" stroke="#29456f"/>
      <text x="139" y="588" fill="#7ee787" font-size="16" font-family="monospace">while(alive) &#123; code(); &#125;</text>

      <path d="M340 470 Q398 492 384 562 Q376 606 332 604" stroke="#8b5e3c" stroke-width="14" fill="none" stroke-linecap="round"/>
      <path d="M332 604 Q355 594 356 572" stroke="#d9b38c" stroke-width="8" fill="none" stroke-linecap="round"/>
    </g>
    """


def create_svg(profile, theme):
    dark = theme == "dark"

    bg = "#0d1117" if dark else "#f6f8fa"
    card = "#111827" if dark else "#ffffff"
    panel = "#0f172a" if dark else "#fdfdfd"
    border = "#253041" if dark else "#d0d7de"
    text = "#e6edf3" if dark else "#24292f"
    muted = "#8b949e" if dark else "#57606a"
    accent = "#35c2ff" if dark else "#0969da"
    accent2 = "#7ee787" if dark else "#1a7f37"
    accent3 = "#ffb86b" if dark else "#bc4c00"

    badge_fill = "#0d1728" if dark else "#eef6ff"
    badge_stroke = "#29456f" if dark else "#c6ddff"

    right_x = 500

    badges = [
        small_badge(right_x, 145, TITLE, badge_fill, badge_stroke, accent),
        small_badge(right_x + 185, 145, "terminal vibes", badge_fill, badge_stroke, accent2),
        small_badge(right_x, 190, "monkey mode", badge_fill, badge_stroke, accent3),
    ]

    rows = []
    rows.append(info_row(right_x, 270, "user:", f"{USERNAME}@github", accent, text))
    rows.append(info_row(right_x, 305, "about:", SUBTITLE, accent, text))
    rows.append(info_row(right_x, 355, "stack:", STACK, accent3, text))
    rows.append(info_row(right_x, 390, "tools:", TOOLS, accent3, text))
    rows.append(info_row(right_x, 425, "languages:", LANGS, accent3, text))
    rows.append(info_row(right_x, 460, "hobbies:", HOBBIES, accent3, text))

    rows.append(
        f'<text x="{right_x}" y="530" fill="{accent2}" font-size="24" font-family="monospace" font-weight="700">GitHub Stats</text>'
    )

    rows.append(info_row(right_x, 575, "repos:", f"{profile['repos']:,}", accent, text))
    rows.append(info_row(right_x + 230, 575, "stars:", f"{profile['stars']:,}", accent, text))

    rows.append(info_row(right_x, 615, "followers:", f"{profile['followers']:,}", accent, text))
    rows.append(info_row(right_x + 230, 615, "commits:", f"{profile['commits']:,}", accent, text))

    rows.append(info_row(right_x, 655, "pull_requests:", f"{profile['pull_requests']:,}", accent, text))
    rows.append(info_row(right_x + 320, 655, "account_age:", f"{profile['account_days']:,} days", accent, text))

    rows.append(
        f"""
        <rect x="{right_x}" y="690" width="620" height="85" rx="18" fill="{panel}" stroke="{border}" />
        <text x="{right_x + 18}" y="722" fill="{accent2}" font-size="18" font-family="monospace" font-weight="700">top_languages:</text>
        <text x="{right_x + 18}" y="754" fill="{text}" font-size="17" font-family="monospace">{escape(profile["top_languages"])}</text>
        """
    )

    rows.append(
        f'<text x="40" y="790" fill="{muted}" font-size="13" font-family="monospace">Last updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}</text>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="820" viewBox="0 0 1200 820">
      <rect width="1200" height="820" fill="{bg}" />
      <rect x="20" y="20" width="1160" height="780" rx="28" fill="{card}" stroke="{border}" stroke-width="2"/>

      <defs>
        <linearGradient id="glow" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="{accent}" stop-opacity="0.22"/>
          <stop offset="100%" stop-color="{accent2}" stop-opacity="0.08"/>
        </linearGradient>
      </defs>

      <rect x="35" y="35" width="1130" height="750" rx="22" fill="url(#glow)" opacity="0.35"/>

      {create_monkey_panel()}

      <text x="{right_x}" y="85" fill="{accent}" font-size="34" font-family="monospace" font-weight="700">{escape(USERNAME)}</text>
      <text x="{right_x}" y="118" fill="{muted}" font-size="18" font-family="monospace">{escape(SUBTITLE)}</text>

      {''.join(badges)}
      {''.join(rows)}
    </svg>
    """


def main():
    profile = get_profile()

    with open("dark_mode.svg", "w", encoding="utf-8") as file:
        file.write(create_svg(profile, "dark"))

    with open("light_mode.svg", "w", encoding="utf-8") as file:
        file.write(create_svg(profile, "light"))

    print("Profile generated.")
    print(f"User: {profile['login']}")
    print(f"Repos: {profile['repos']}")
    print(f"Stars: {profile['stars']}")
    print(f"Followers: {profile['followers']}")
    print(f"Commits: {profile['commits']}")


if __name__ == "__main__":
    main()
