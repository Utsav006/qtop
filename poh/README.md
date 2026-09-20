# Proof-of-Humanity (PoH) Registry Proof of Concept

This directory provides a lightweight proof-of-concept for contributor verification to protect against bots and sybil accounts while keeping entry frictionless.

`claims.yaml` uses a JSON-compatible YAML subset so that verification can run with Python standard library dependencies only.

## Candidate Entry Structure

Each participant declares:
- `github`: Account username
- `commit_signing`: (Optional) public key fingerprint (`SHA256:...`)
- `claims`: 1 to 5 public proof URLs (`github`, `gitlab`, `keyoxide`, `linkedin`, `matrix`, `orcid`, `website`)
- `status`: `"candidate"`, `"verified"`, or `"revoked"`

```yaml
{
  "schema_version": 1,
  "participants": [
    {
      "github": "octo-contributor",
      "commit_signing": {"fingerprints": ["SHA256:base64-fingerprint"]},
      "claims": [
        {"provider": "github", "url": "[https://github.com/octo-contributor](https://github.com/octo-contributor)"},
        {"provider": "orcid", "url": "[https://orcid.org/0000-0000-0000-0000](https://orcid.org/0000-0000-0000-0000)"},
        {"provider": "keyoxide", "url": "[https://keyoxide.org/example](https://keyoxide.org/example)"}
      ],
      "status": "candidate"
    }
  ]
}