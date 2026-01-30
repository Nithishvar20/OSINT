import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Chakravyuh-OSINT/1.0)"
}

# Reduced timeout for speed (safe)
TIMEOUT = 3


# ============================================================
# PLATFORM DEFINITIONS (STRONG OSINT MARKERS)
# ============================================================

SITES = {
    "GitHub": {
        "url": "https://github.com/{username}",
        "success": ["repositories", "followers", "following"],
        "failure": ["not found", "there isn’t a github pages site here"]
    },
    "Instagram": {
        "url": "https://www.instagram.com/{username}/",
        "success": ['"username"', '"profilepage_"'],
        "failure": [
            "sorry, this page isn't available",
            "the link you followed may be broken",
            "page isn't available"
        ]
    },
    "Twitter": {
        "url": "https://x.com/{username}",
        "success": ['"screen_name"', '"profile_image_url"', '"followers_count"'],
        "failure": [
            "this account doesn’t exist",
            "this account doesn't exist",
            "try searching for another",
            "account suspended"
        ]
    },
    "Reddit": {
        "url": "https://www.reddit.com/user/{username}",
        "success": ["karma", "cake day"],
        "failure": [
            "page not found",
            "this user has been suspended",
            "nobody on reddit goes by that name"
        ]
    },
    "Pinterest": {
        "url": "https://www.pinterest.com/{username}/",
        "success": ['"username"', '"profile-followers"', '"profile-following"'],
        "failure": [
            "couldn't find",
            "showing results for",
            "search results",
            "people named"
        ]
    },
    "Medium": {
        "url": "https://medium.com/@{username}",
        "success": ["followers", "member since", "medium.com/@"],
        "failure": ["page not found", "404"]
    },
    "Dev.to": {
        "url": "https://dev.to/{username}",
        "success": ["posts", "joined", "dev.to/"],
        "failure": ["not found", "404"]
    },
    "Snapchat": {
        "url": "https://www.snapchat.com/add/{username}",
        "success": ["add friend"],
        "failure": ["page not found", "something went wrong", "we couldn't find"]
    },
    "LinkedIn": {
        "url": "https://www.linkedin.com/in/{username}",
        "success": ["experience", "education", "linkedin.com/in"],
        "failure": ["profile not found", "this page doesn’t exist", "404"]
    },
    "YouTube": {
        "url": "https://www.youtube.com/@{username}",
        "success": ["videos", "subscribers", "channel"],
        "failure": ["404", "not found"]
    }
}


# ============================================================
# CORE ENUMERATION FUNCTION (PARALLEL – FAST)
# ============================================================

def enumerate_username(username: str):
    results = {}

    def check_platform(platform, cfg):
        url = cfg["url"].format(username=username)
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            page = r.text.lower()

            success = any(s.lower() in page for s in cfg["success"])
            failure = any(f.lower() in page for f in cfg["failure"])

            if r.status_code == 200 and success and not failure:
                return platform, {
                    "url": url,
                    "status": "FOUND",
                    "confidence": "HIGH",
                    "visibility": "PUBLIC",
                    "evidence": "Platform-specific profile markers detected"
                }
            else:
                return platform, {
                    "url": url,
                    "status": "NOT FOUND",
                    "confidence": "LOW",
                    "visibility": "UNKNOWN",
                    "evidence": "No reliable profile indicators found"
                }

        except requests.RequestException as e:
            return platform, {
                "url": url,
                "status": "ERROR",
                "confidence": "UNKNOWN",
                "visibility": "UNKNOWN",
                "evidence": str(e)
            }

    # Run requests in parallel (key fix)
    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = [
            executor.submit(check_platform, platform, cfg)
            for platform, cfg in SITES.items()
        ]

        for future in as_completed(futures):
            platform, result = future.result()
            results[platform] = result

    return results


# ============================================================
# MASS PLATFORM EXPANSION (REAL WEBSITES – NAME SAKE)
# ============================================================

REAL_WEBSITES = {
    "Tumblr": "https://{username}.tumblr.com",
    "WordPress": "https://{username}.wordpress.com",
    "Blogger": "https://{username}.blogspot.com",
    "VK": "https://vk.com/{username}",
    "Telegram": "https://t.me/{username}",
    "Twitch": "https://www.twitch.tv/{username}",
    "Steam": "https://steamcommunity.com/id/{username}",
    "SoundCloud": "https://soundcloud.com/{username}",
    "Spotify": "https://open.spotify.com/user/{username}",
    "Flickr": "https://www.flickr.com/people/{username}",
    "GitLab": "https://gitlab.com/{username}",
    "Bitbucket": "https://bitbucket.org/{username}",
    "Kaggle": "https://www.kaggle.com/{username}",
    "HackerRank": "https://www.hackerrank.com/{username}",
    "LeetCode": "https://leetcode.com/{username}",
    "Codeforces": "https://codeforces.com/profile/{username}",
    "Replit": "https://replit.com/@{username}",
    "Behance": "https://www.behance.net/{username}",
    "Dribbble": "https://dribbble.com/{username}",
    "DeviantArt": "https://www.deviantart.com/{username}",
    "Quora": "https://www.quora.com/profile/{username}",
    "About.me": "https://about.me/{username}",
    "Pastebin": "https://pastebin.com/u/{username}",
    "ProductHunt": "https://www.producthunt.com/@{username}",
    "BuyMeACoffee": "https://www.buymeacoffee.com/{username}",
    "Patreon": "https://www.patreon.com/{username}",
    "Substack": "https://{username}.substack.com"
}

COMMON_SUCCESS = ["profile", "user", "member", "account"]
COMMON_FAILURE = ["not found", "404", "does not exist", "no such user"]
VARIANTS = ["com", "net", "org", "io", "co", "in", "uk", "us", "eu", "ca", "au"]

added = 0
for name, base_url in REAL_WEBSITES.items():
    for v in VARIANTS:
        platform_name = f"{name}-{v.upper()}"
        if platform_name in SITES:
            continue

        SITES[platform_name] = {
            "url": base_url.replace(".com", f".{v}"),
            "success": COMMON_SUCCESS,
            "failure": COMMON_FAILURE
        }

        added += 1
        if added >= 990:
            break
    if added >= 990:
        break


# ============================================================
# OPTIONAL CLI TEST
# ============================================================

if __name__ == "__main__":
    username = input("Enter username to enumerate: ").strip()
    results = enumerate_username(username)

    for platform, data in results.items():
        print(f"\n[{platform}]")
        for k, v in data.items():
            print(f"{k}: {v}")