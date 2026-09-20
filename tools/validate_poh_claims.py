#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path

ALLOWED_PROVIDERS = {"github", "gitlab", "keyoxide", "linkedin", "matrix", "orcid", "website"}
ALLOWED_STATUSES = {"candidate", "verified", "revoked"}

def validate_participant(entry):
    if not isinstance(entry, dict):
        raise ValueError("Participant entry must be a dictionary")
    
    github = entry.get("github")
    if not github or not isinstance(github, str):
        raise ValueError("Field 'github' must be a non-empty string")
    
    claims = entry.get("claims", [])
    if not isinstance(claims, list) or not (1 <= len(claims) <= 5):
        raise ValueError(f"'{github}': claims must contain between 1 and 5 entries")
    
    seen_providers = set()
    has_github_claim = False

    for claim in claims:
        provider = claim.get("provider")
        url = claim.get("url", "")

        if provider not in ALLOWED_PROVIDERS:
            raise ValueError(f"'{github}': invalid provider '{provider}'")
        if provider in seen_providers:
            raise ValueError(f"'{github}': duplicate provider '{provider}'")
        seen_providers.add(provider)

        if provider == "github":
            has_github_claim = True
            if github.lower() not in url.lower():
                raise ValueError(f"'{github}': github claim URL must match username")

    if not has_github_claim:
        raise ValueError(f"'{github}': must include a GitHub claim matching account username")

    status = entry.get("status")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"'{github}': status must be one of {ALLOWED_STATUSES}")

    signing = entry.get("commit_signing", {})
    if signing and "fingerprints" in signing:
        for fp in signing["fingerprints"]:
            if not fp.startswith("SHA256:"):
                raise ValueError(f"'{github}': signing fingerprint must start with 'SHA256:'")

def validate_registry(data):
    if data.get("schema_version") != 1:
        raise ValueError("Invalid or unsupported 'schema_version'")
    
    participants = data.get("participants", [])
    if not isinstance(participants, list):
        raise ValueError("'participants' must be a list")

    seen_github_users = set()
    for p in participants:
        validate_participant(p)
        user = p["github"].lower()
        if user in seen_github_users:
            raise ValueError(f"Duplicate entry for GitHub user '{user}'")
        seen_github_users.add(user)

def main():
    repo_root = Path(__file__).resolve().parent.parent
    claims_path = repo_root / "poh" / "claims.yaml"

    if not claims_path.exists():
        print(f"Error: {claims_path} not found.", file=sys.stderr)
        sys.exit(1)

    with open(claims_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error parsing {claims_path} as JSON/YAML subset: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        validate_registry(data)
        print("Proof-of-Humanity registry validation passed successfully.")
    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()