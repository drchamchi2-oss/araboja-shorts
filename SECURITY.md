# Security Policy

## Supported Versions

This project is early-stage. Security fixes target the default branch.

| Version | Supported |
| ------- | --------- |
| main    | Yes       |

## Reporting A Vulnerability

Please do not open a public issue for suspected security vulnerabilities.

Use GitHub's private vulnerability reporting or open a private advisory if available for this repository:

```text
https://github.com/drchamchi2-oss/shorts_test/security/advisories/new
```

A useful report includes:

- A short description of the issue.
- Steps to reproduce.
- Impact and affected commit or version.
- Suggested mitigation if known.

## Scope

Only test code and behavior in this repository and only in environments you own or are authorized to test. Do not probe third-party systems, API providers, or media sources without permission.

## Secrets

Never commit API keys, `.env` files, generated credentials, cookies, private logs, private datasets, or proprietary media assets. If a secret is accidentally committed, rotate it immediately before opening a public issue or pull request.
