import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Chakravyuh-OSINT/1.0)"
}

TIMEOUT = 6


# ============================================================
# PLATFORM DEFINITIONS
# ============================================================

SITES = {
    "GitHub": {
        "url": "https://github.com/{username}",
        "success": ["repositories", "followers", "following"],
        "failure": ["not found"]
    },

    "GitLab": {
        "url": "https://gitlab.com/{username}",
        "success": ["projects", "groups"],
        "failure": ["404", "not found"]
    },

    "Bitbucket": {
        "url": "https://bitbucket.org/{username}",
        "success": ["repositories"],
        "failure": ["not found"]
    },

    "Instagram": {
        "url": "https://www.instagram.com/{username}/",
        "success": ['"username"', '"profilepage_"'],
        "failure": ["page isn't available"]
    },

    "Twitter": {
        "url": "https://x.com/{username}",
        "success": ['"screen_name"', '"followers_count"'],
        "failure": ["doesn’t exist", "account suspended"]
    },

    "Facebook": {
        "url": "https://www.facebook.com/{username}",
        "success": ["timeline", "friends"],
        "failure": ["content isn't available"]
    },

    "LinkedIn": {
        "url": "https://www.linkedin.com/in/{username}",
        "success": ["experience", "education"],
        "failure": ["profile not found"]
    },

    "Reddit": {
        "url": "https://www.reddit.com/user/{username}",
        "success": ["karma", "cake day"],
        "failure": ["nobody on reddit goes by that name"]
    },

    "YouTube": {
        "url": "https://www.youtube.com/@{username}",
        "success": ["videos", "subscribers"],
        "failure": ["404"]
    },

    "TikTok": {
        "url": "https://www.tiktok.com/@{username}",
        "success": ["followers", "following"],
        "failure": ["couldn't find this account"]
    },

    "Pinterest": {
        "url": "https://www.pinterest.com/{username}/",
        "success": ['"profile-followers"'],
        "failure": ["couldn't find"]
    },

    "Medium": {
        "url": "https://medium.com/@{username}",
        "success": ["member since", "followers"],
        "failure": ["page not found"]
    },

    "Dev.to": {
        "url": "https://dev.to/{username}",
        "success": ["joined", "posts"],
        "failure": ["not found"]
    },

    "StackOverflow": {
        "url": "https://stackoverflow.com/users/{username}",
        "success": ["reputation"],
        "failure": ["page not found"]
    },

    "HackerRank": {
        "url": "https://www.hackerrank.com/{username}",
        "success": ["badges", "points"],
        "failure": ["404"]
    },

    "LeetCode": {
        "url": "https://leetcode.com/{username}/",
        "success": ["ranking", "solutions"],
        "failure": ["page not found"]
    },

    "Codeforces": {
        "url": "https://codeforces.com/profile/{username}",
        "success": ["rating"],
        "failure": ["not found"]
    },

    "Kaggle": {
        "url": "https://www.kaggle.com/{username}",
        "success": ["competitions", "datasets"],
        "failure": ["page not found"]
    },

    "Steam": {
        "url": "https://steamcommunity.com/id/{username}",
        "success": ["games", "badges"],
        "failure": ["profile not found"]
    },

    "Spotify": {
        "url": "https://open.spotify.com/user/{username}",
        "success": ["playlists"],
        "failure": ["404"]
    },

    "SoundCloud": {
        "url": "https://soundcloud.com/{username}",
        "success": ["tracks"],
        "failure": ["not found"]
    },

    "Twitch": {
        "url": "https://www.twitch.tv/{username}",
        "success": ["videos", "followers"],
        "failure": ["sorry. unless you’ve got a time machine"]
    },

    "Flickr": {
        "url": "https://www.flickr.com/people/{username}",
        "success": ["photos"],
        "failure": ["not found"]
    },

    "Quora": {
        "url": "https://www.quora.com/profile/{username}",
        "success": ["answers", "questions"],
        "failure": ["page not found"]
    },

    "About.me": {
        "url": "https://about.me/{username}",
        "success": ["about"],
        "failure": ["404"]
    },

    "Behance": {
        "url": "https://www.behance.net/{username}",
        "success": ["projects"],
        "failure": ["not found"]
    },

    "Dribbble": {
        "url": "https://dribbble.com/{username}",
        "success": ["shots"],
        "failure": ["not found"]
    },

    "Keybase": {
        "url": "https://keybase.io/{username}",
        "success": ["pgp", "proofs"],
        "failure": ["not found"]
    },

    "Pastebin": {
        "url": "https://pastebin.com/u/{username}",
        "success": ["pastes"],
        "failure": ["not found"]
    }
}


# ============================================================
# CORE FUNCTION (THIS WAS MISSING)
# ============================================================

def enumerate_username(username: str):
    results = {}

    for platform, cfg in SITES.items():
        url = cfg["url"].format(username=username)

        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)

            # 🔥 FIX 1: Normalize text (unicode + lowercase)
            page = r.text.encode("ascii", errors="ignore").decode().lower()

            found = False

            if r.status_code == 200:
                # 🔥 FIX 2: FAILURE FIRST (most reliable)
                if any(f.lower() in page for f in cfg["failure"]):
                    found = False
                # 🔥 FIX 3: ALL success markers must match
                elif all(s.lower() in page for s in cfg["success"]):
                    found = True

            if found:
                results[platform] = {
                    "url": url,
                    "status": "FOUND",
                    "confidence": "HIGH",
                    "visibility": "PUBLIC"
                }
            else:
                results[platform] = {
                    "url": url,
                    "status": "NOT FOUND",
                    "confidence": "LOW",
                    "visibility": "UNKNOWN"
                }

        except requests.RequestException as e:
            results[platform] = {
                "url": url,
                "status": "ERROR",
                "confidence": "UNKNOWN",
                "visibility": "UNKNOWN",
                "error": str(e)
            }

    return results