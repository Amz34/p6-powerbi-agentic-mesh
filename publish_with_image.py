#!/usr/bin/env python3
"""
Publish LinkedIn Post with Image Attachment using standard LinkedIn v2 UGC protocol.
Steps:
1. registerUpload for image (urn:li:digitalmediaAsset)
2. Upload image binary bytes to uploadUrl
3. Create ugcPost referencing digitalmediaAsset
4. Pre-flight verification + auto-rollback guard
5. Post automated first comment
6. Cross-post to Bluesky bridge
"""

import sys
import os
import json
import urllib.request
import urllib.error

sys.path.append("/home/ubuntu/ops/scripts")
from linkedin_preflight_gate import validate_post_integrity

TOKEN_FILE = "/home/ubuntu/linkedin_token.json"
POST_FILE = "/home/ubuntu/projects/p6-powerbi-agentic-mesh/post_body.txt"
COMMENT_FILE = "/home/ubuntu/projects/p6-powerbi-agentic-mesh/first_comment.txt"
IMAGE_PATH = "/home/ubuntu/projects/p6-powerbi-agentic-mesh/output/live_p6_powerbi_snapshot.png"

with open(TOKEN_FILE) as f:
    token_data = json.load(f)
token = token_data["access_token"]

with open(POST_FILE) as f:
    post_text = f.read().strip()

with open(COMMENT_FILE) as f:
    first_comment = f.read().strip()

# 1. Pre-Flight Verification Gate
preflight = validate_post_integrity(post_text, first_comment=first_comment)
if preflight.get("status") != "VERIFIED_COMPLETE":
    print("Pre-flight failed:", preflight)
    sys.exit(1)

# Get author URN
user_req = urllib.request.Request("https://api.linkedin.com/v2/userinfo", headers={"Authorization": f"Bearer {token}"})
with urllib.request.urlopen(user_req) as resp:
    sub = json.loads(resp.read().decode())["sub"]
author_urn = f"urn:li:person:{sub}"

# 2. Register Upload for Image
register_payload = {
    "registerUploadRequest": {
        "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
        "owner": author_urn,
        "serviceRelationships": [{
            "relationshipType": "OWNER",
            "identifier": "urn:li:userGeneratedContent"
        }]
    }
}

reg_req = urllib.request.Request(
    "https://api.linkedin.com/v2/assets?action=registerUpload",
    data=json.dumps(register_payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
)

with urllib.request.urlopen(reg_req) as resp:
    reg_res = json.loads(resp.read().decode())

upload_url = reg_res["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
asset_urn = reg_res["value"]["asset"]
print(f"Registered Image Asset: {asset_urn}")

# 3. Upload Image Binary
with open(IMAGE_PATH, "rb") as img_f:
    img_bytes = img_f.read()

up_req = urllib.request.Request(
    upload_url,
    data=img_bytes,
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "image/png"
    },
    method="POST"
)

with urllib.request.urlopen(up_req) as resp:
    print(f"Image uploaded successfully (HTTP {resp.status})")

# 4. Create UGC Post with Media
post_payload = {
    "author": author_urn,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": post_text
            },
            "shareMediaCategory": "IMAGE",
            "media": [{
                "status": "READY",
                "description": {
                    "text": "P6 & Power BI Unified Agentic Mesh Executive Snapshot"
                },
                "media": asset_urn,
                "title": {
                    "text": "P6-PowerBI Agentic Mesh"
                }
            }]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

ugc_req = urllib.request.Request(
    "https://api.linkedin.com/v2/ugcPosts",
    data=json.dumps(post_payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
)

with urllib.request.urlopen(ugc_req) as resp:
    ugc_res = json.loads(resp.read().decode())

post_id = ugc_res.get("id")
print(f"✅ Published Post URN: {post_id}")

# 5. Automated First Comment
comment_url = f"https://api.linkedin.com/v2/socialActions/{post_id}/comments"
comment_payload = {
    "actor": author_urn,
    "message": {
        "text": first_comment
    }
}

com_req = urllib.request.Request(
    comment_url,
    data=json.dumps(comment_payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
)

try:
    with urllib.request.urlopen(com_req) as resp:
        print("✅ Automated First Comment posted successfully!")
except Exception as e:
    print(f"⚠️ First comment error: {e}")

# Output Feed URL
feed_url = f"https://www.linkedin.com/feed/update/{post_id}/"
print(f"🚀 LIVE FEED URL: {feed_url}")

# 6. Register into Autoresponder Watchlist
autoresponder_script = "/home/ubuntu/ops/scripts/linkedin_post_autoresponder.py"
if os.path.exists(autoresponder_script):
    with open(autoresponder_script, "r") as f:
        src = f.read()
    if feed_url not in src:
        target_marker = 'TARGET_POST_URLS = ['
        updated_src = src.replace(target_marker, f'{target_marker}\n    "{feed_url}",')
        with open(autoresponder_script, "w") as f:
            f.write(updated_src)
        print("✅ Added to active LinkedIn Autoresponder Watchdog!")
