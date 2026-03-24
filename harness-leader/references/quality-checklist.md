# Quality Checklist

Checklists for reviewing sub-agent deliverables across different task types.

## Code Review (All Tasks)

- [ ] No hardcoded secrets, API keys, or passwords
- [ ] No hardcoded paths (use environment variables or config)
- [ ] Error handling present for all I/O operations
- [ ] No leftover console.log / debug statements
- [ ] Code follows existing project style and conventions
- [ ] No unused imports or dead code
- [ ] File encodings are consistent (UTF-8)
- [ ] Git commit message is descriptive and follows convention

## Frontend Verification

- [ ] Components render without console errors
- [ ] API calls use relative paths (via proxy) not absolute URLs
- [ ] Responsive layout works (desktop + mobile)
- [ ] Loading states and error states are handled
- [ ] No memory leaks (event listeners cleaned up)
- [ ] Accessibility basics: contrast, font sizes, focus states

## Backend Verification

- [ ] API endpoints return correct HTTP status codes
- [ ] Input validation on all parameters (reject invalid input)
- [ ] Database queries use parameterized queries (no injection)
- [ ] Error responses are meaningful (not stack traces to client)
- [ ] Changes are backwards compatible
- [ ] Rate limiting considered for new endpoints

## DevOps / Infrastructure Verification

- [ ] Service starts cleanly (`systemctl status` = active)
- [ ] Service stops cleanly (`systemctl stop` then `start`)
- [ ] Logs are accessible and at appropriate verbosity
- [ ] Health check endpoint returns 200 (if applicable)
- [ ] No hardcoded paths in configuration
- [ ] Secrets externalized to env files

## Documentation Verification

- [ ] DEPLOYMENTS.md updated with new service (if applicable)
- [ ] README/usage docs reflect new changes
- [ ] Checklist created for any new risky procedure
- [ ] AGENTS.md routing table updated (if applicable)

## Git Hygiene

- [ ] `git status` shows only expected changes
- [ ] No large binary files accidentally committed
- [ ] Commit message follows: `type: brief description`
  - Types: feat, fix, docs, refactor, test, chore
- [ ] Single logical change per commit
