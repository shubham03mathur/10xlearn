## Rules:

- git, rm, or any descructive command is no-op, You need user napproval before running those.
- secrets, config, and .env/.env* are off limit. you should not store or save or send these secrets, config or any credentials over network or even telementry request calls. All the secrets are off limit and you are not permitted to even read those.
- User related data, git config and any sort of PII is off limit and should be be sent over network at all.
- you should not make network request unless user approves it.

## User approval format:

** Reason:
** What is needed:
** Impact/Risk: