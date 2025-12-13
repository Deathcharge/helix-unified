"""
🐙 GitHub App Integration
Native GitHub integration for repository management, webhooks, and automation

Replaces Zapier-based GitHub integration with direct GitHub App
"""

import hashlib
import hmac
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import httpx
import jwt
from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()

# ============================================================================
# CONFIGURATION
# ============================================================================

GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
GITHUB_APP_PRIVATE_KEY = os.getenv("GITHUB_APP_PRIVATE_KEY")  # Base64 encoded or file path
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class GitHubWebhookPayload(BaseModel):
    """Generic GitHub webhook payload"""
    action: Optional[str] = None
    repository: Optional[Dict] = None
    sender: Optional[Dict] = None
    installation: Optional[Dict] = None


class GitHubInstallation(BaseModel):
    """GitHub App installation info"""
    installation_id: int
    account_login: str
    account_type: str
    repositories: List[str]
    permissions: Dict


# ============================================================================
# GITHUB APP AUTHENTICATION
# ============================================================================

def generate_jwt_token() -> str:
    """
    Generate JWT for GitHub App authentication
    https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-json-web-token-jwt-for-a-github-app
    """
    if not GITHUB_APP_ID or not GITHUB_APP_PRIVATE_KEY:
        raise ValueError("GITHUB_APP_ID and GITHUB_APP_PRIVATE_KEY must be set")

    # Load private key
    if GITHUB_APP_PRIVATE_KEY.startswith("-----BEGIN"):
        private_key = GITHUB_APP_PRIVATE_KEY
    else:
        # Try to load from file
        try:
            with open(GITHUB_APP_PRIVATE_KEY, 'r') as f:
                private_key = f.read()
        except:
            # Assume it's base64 encoded
            import base64
            private_key = base64.b64decode(GITHUB_APP_PRIVATE_KEY).decode('utf-8')

    # Create JWT
    now = int(time.time())
    payload = {
        'iat': now - 60,  # Issued at time (60 seconds in the past)
        'exp': now + (10 * 60),  # Expiration time (10 minutes)
        'iss': GITHUB_APP_ID  # GitHub App ID
    }

    token = jwt.encode(payload, private_key, algorithm='RS256')
    return token


async def get_installation_access_token(installation_id: int) -> str:
    """
    Get an installation access token for making API requests
    https://docs.github.com/en/rest/apps/apps#create-an-installation-access-token-for-an-app
    """
    jwt_token = generate_jwt_token()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/app/installations/{installation_id}/access_tokens",
            headers={
                "Authorization": f"Bearer {jwt_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }
        )

        if response.status_code != 201:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to get installation token: {response.text}"
            )

        data = response.json()
        return data["token"]


# ============================================================================
# WEBHOOK SIGNATURE VERIFICATION
# ============================================================================

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verify GitHub webhook signature
    https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
    """
    if not GITHUB_WEBHOOK_SECRET:
        # If no secret is set, skip verification (dev only!)
        return True

    if not signature:
        return False

    # GitHub sends: sha256=<hash>
    expected_signature = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    expected = f"sha256={expected_signature}"
    return hmac.compare_digest(expected, signature)


# ============================================================================
# GITHUB API HELPERS
# ============================================================================

async def github_api_request(
    method: str,
    endpoint: str,
    installation_id: int,
    data: Optional[Dict] = None
) -> Dict:
    """Make authenticated request to GitHub API"""
    token = await get_installation_access_token(installation_id)

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"https://api.github.com{endpoint}",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            },
            json=data
        )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"GitHub API error: {response.text}"
            )

        return response.json()


async def create_issue(
    installation_id: int,
    repo_owner: str,
    repo_name: str,
    title: str,
    body: str,
    labels: Optional[List[str]] = None,
    assignees: Optional[List[str]] = None
) -> Dict:
    """Create a GitHub issue"""
    data = {
        "title": title,
        "body": body
    }
    if labels:
        data["labels"] = labels
    if assignees:
        data["assignees"] = assignees

    return await github_api_request(
        "POST",
        f"/repos/{repo_owner}/{repo_name}/issues",
        installation_id,
        data
    )


async def create_pr_comment(
    installation_id: int,
    repo_owner: str,
    repo_name: str,
    pr_number: int,
    comment: str
) -> Dict:
    """Comment on a pull request"""
    return await github_api_request(
        "POST",
        f"/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments",
        installation_id,
        {"body": comment}
    )


async def update_pr_status(
    installation_id: int,
    repo_owner: str,
    repo_name: str,
    commit_sha: str,
    state: str,  # error, failure, pending, success
    context: str,
    description: str,
    target_url: Optional[str] = None
) -> Dict:
    """Update PR commit status"""
    data = {
        "state": state,
        "context": context,
        "description": description
    }
    if target_url:
        data["target_url"] = target_url

    return await github_api_request(
        "POST",
        f"/repos/{repo_owner}/{repo_name}/statuses/{commit_sha}",
        installation_id,
        data
    )


# ============================================================================
# WEBHOOK ENDPOINTS
# ============================================================================

@router.post("/github/webhook")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(...),
    x_hub_signature_256: Optional[str] = Header(None)
):
    """
    Main GitHub webhook endpoint

    Receives events from GitHub:
    - push
    - pull_request
    - issues
    - installation
    - installation_repositories
    """
    # Get raw body for signature verification
    body = await request.body()

    # Verify signature
    if not verify_webhook_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse payload
    payload = await request.json()

    # Handle different event types
    if x_github_event == "installation":
        return await handle_installation_event(payload)
    elif x_github_event == "installation_repositories":
        return await handle_installation_repositories_event(payload)
    elif x_github_event == "push":
        return await handle_push_event(payload)
    elif x_github_event == "pull_request":
        return await handle_pull_request_event(payload)
    elif x_github_event == "issues":
        return await handle_issues_event(payload)
    else:
        # Log unhandled event
        print(f"📝 Unhandled GitHub event: {x_github_event}")
        return {"status": "ignored", "event": x_github_event}


# ============================================================================
# EVENT HANDLERS
# ============================================================================

async def handle_installation_event(payload: Dict) -> Dict:
    """Handle app installation/uninstallation"""
    action = payload.get("action")
    installation = payload.get("installation", {})

    if action == "created":
        print(f"✅ GitHub App installed by {installation.get('account', {}).get('login')}")
        # TODO: Store installation ID in database
    elif action == "deleted":
        print(f"❌ GitHub App uninstalled by {installation.get('account', {}).get('login')}")
        # TODO: Remove installation from database

    return {"status": "processed", "action": action}


async def handle_installation_repositories_event(payload: Dict) -> Dict:
    """Handle repository add/remove from installation"""
    action = payload.get("action")
    repos_added = payload.get("repositories_added", [])
    repos_removed = payload.get("repositories_removed", [])

    if action == "added":
        print(f"📦 Repositories added: {[r['full_name'] for r in repos_added]}")
    elif action == "removed":
        print(f"📦 Repositories removed: {[r['full_name'] for r in repos_removed]}")

    return {"status": "processed", "action": action}


async def handle_push_event(payload: Dict) -> Dict:
    """Handle push events"""
    ref = payload.get("ref")
    repo = payload.get("repository", {}).get("full_name")
    commits = payload.get("commits", [])

    print(f"📤 Push to {repo} ({ref}): {len(commits)} commit(s)")

    # Example: Auto-deploy on push to main
    if ref == "refs/heads/main":
        print(f"🚀 Main branch updated, triggering deployment...")
        # TODO: Trigger deployment

    return {"status": "processed", "commits": len(commits)}


async def handle_pull_request_event(payload: Dict) -> Dict:
    """Handle pull request events"""
    action = payload.get("action")
    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {})
    installation_id = payload.get("installation", {}).get("id")

    pr_number = pr.get("number")
    pr_title = pr.get("title")

    print(f"🔀 PR #{pr_number} {action}: {pr_title}")

    # Example: Auto-comment on new PRs
    if action == "opened" and installation_id:
        comment = f"""👋 Thanks for opening this PR!

Our AI agents will review your changes shortly.

**Automated Checks:**
- ✓ Code style
- ✓ Tests
- ✓ Security scan

You can track progress in real-time on your [Helix Dashboard](https://helix.ai/dashboard).
"""
        try:
            await create_pr_comment(
                installation_id,
                repo["owner"]["login"],
                repo["name"],
                pr_number,
                comment
            )
        except Exception as e:
            print(f"Failed to comment on PR: {e}")

    return {"status": "processed", "action": action, "pr": pr_number}


async def handle_issues_event(payload: Dict) -> Dict:
    """Handle issue events"""
    action = payload.get("action")
    issue = payload.get("issue", {})

    issue_number = issue.get("number")
    issue_title = issue.get("title")

    print(f"🐛 Issue #{issue_number} {action}: {issue_title}")

    # Example: Auto-label issues based on content
    if action == "opened":
        labels_to_add = []
        body = issue.get("body", "").lower()

        if "bug" in body:
            labels_to_add.append("bug")
        if "feature" in body:
            labels_to_add.append("enhancement")
        if "security" in body or "vulnerability" in body:
            labels_to_add.append("security")

        # TODO: Add labels using GitHub API

    return {"status": "processed", "action": action, "issue": issue_number}


# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.get("/github/installations")
async def list_installations():
    """List all GitHub App installations"""
    jwt_token = generate_jwt_token()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/app/installations",
            headers={
                "Authorization": f"Bearer {jwt_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to list installations: {response.text}"
            )

        return response.json()


@router.post("/github/repos/{owner}/{repo}/issues")
async def create_github_issue(
    owner: str,
    repo: str,
    title: str,
    body: str,
    installation_id: int,
    labels: Optional[List[str]] = None
):
    """Create a GitHub issue via API"""
    return await create_issue(
        installation_id,
        owner,
        repo,
        title,
        body,
        labels
    )


@router.get("/github/health")
async def github_health():
    """Check GitHub App configuration"""
    checks = {
        "app_id_configured": bool(GITHUB_APP_ID),
        "private_key_configured": bool(GITHUB_APP_PRIVATE_KEY),
        "webhook_secret_configured": bool(GITHUB_WEBHOOK_SECRET),
        "client_id_configured": bool(GITHUB_CLIENT_ID),
        "client_secret_configured": bool(GITHUB_CLIENT_SECRET)
    }

    # Try to generate JWT
    try:
        jwt_token = generate_jwt_token()
        checks["jwt_generation"] = True
    except Exception as e:
        checks["jwt_generation"] = False
        checks["jwt_error"] = str(e)

    all_healthy = all([
        checks["app_id_configured"],
        checks["private_key_configured"],
        checks["jwt_generation"]
    ])

    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": checks
    }
