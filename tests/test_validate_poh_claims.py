import pytest
from tools.validate_poh_claims import validate_registry

def test_valid_empty_registry():
    data = {"schema_version": 1, "participants": []}
    validate_registry(data)

def test_valid_participant():
    data = {
        "schema_version": 1,
        "participants": [
            {
                "github": "alice",
                "claims": [
                    {"provider": "github", "url": "https://github.com/alice"},
                    {"provider": "orcid", "url": "https://orcid.org/0000-0001-2345-6789"}
                ],
                "status": "candidate"
            }
        ]
    }
    validate_registry(data)

def test_missing_github_claim():
    data = {
        "schema_version": 1,
        "participants": [
            {
                "github": "alice",
                "claims": [
                    {"provider": "linkedin", "url": "https://linkedin.com/in/alice"}
                ],
                "status": "candidate"
            }
        ]
    }
    with pytest.raises(ValueError, match="must include a GitHub claim"):
        validate_registry(data)

def test_duplicate_participant():
    entry = {
        "github": "bob",
        "claims": [{"provider": "github", "url": "https://github.com/bob"}],
        "status": "candidate"
    }
    data = {"schema_version": 1, "participants": [entry, entry]}
    with pytest.raises(ValueError, match="Duplicate entry"):
        validate_registry(data)