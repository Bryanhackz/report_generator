# Security Policy

## Supported Versions
Currently, only the latest `main` branch is supported.

## Scope
This is a command-line interface (CLI) tool designed to run in a trusted local environment or cron job. It is not exposed to the public internet. The primary security concerns are the safe handling of SMTP credentials via environment variables (`.env`) and the prevention of SQL injection in local SQLite queries.

## Reporting a Vulnerability
Please do not report security vulnerabilities through public GitHub issues. Send an email to **br4yangil006@gmail.com**. You should receive a response within 48 hours.

Please include:
- Type of issue (e.g., SQL injection, credential leak)
- Full paths of source file(s) related to the issue
- Step-by-step instructions to reproduce the issue
- Impact of the issue
