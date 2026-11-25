# Lux winter questionnaire service

The survey and password-protected results UI live under `/zero-to-launch/lux-scholar/` on arenaschool.org. The main site's two API rewrites route to this separate Vercel project (`arena-lux-private-service`). Deploy changes to this directory with `vercel deploy --prod --cwd services/lux-api`; this project is not connected to GitHub auto-deployment.

Student answers are saved as separate JSON records in a **private** Vercel Blob store before submission succeeds. They are never committed to Git, served as static files, or included in build logs. Slack notifications are secondary. The results API requires an eight-hour signed, HttpOnly, Secure session cookie; both API and page responses exclude caching/indexing. All answer text is rendered using textContent, including names. CSV exports escape spreadsheet formula prefixes.

Production environment variables:

- `LUX_BLOB_READ_WRITE_TOKEN`: private store access, also used by the digest workflow.
- `LUX_RESULTS_PASSWORD_HASH`: `salt:scrypt(password, salt, 32).hex`.
- `LUX_SESSION_SECRET`: random server-side signing secret; rotate with the password to invalidate existing sessions.
- `ARENA_SLACK_BOT_TOKEN`: optional notification delivery using the existing enrollment channel.

The GitHub workflow `lux-digest.yml` runs daily at 09:00 UTC and sends every third day measured from 2026-11-25. It reads private records at runtime and DMs the configured recipient through JJOps. It requires the storage secret above plus `JJOPS_SLACK_BOT_TOKEN` and `JJOPS_USER_ID` as GitHub Actions secrets. No data is saved in artifacts or logs. GitHub scheduled tasks can be delayed and, in public repositories, disabled after 60 days of repository inactivity. Disable the workflow when reporting is no longer needed.

`npm run test:lux` at the repository root covers access control, session expiry, language switching, skip logic, selection limits, safe answer rendering, and digest cadence. Verify both API rewrites after deployment. Never put a password, storage credential, or student answer in a public source file.

Counts are submissions and distinct self-reported names, not verified unique students. Nonrespondent tracking requires a cohort roster. The results page exports all records for offline comparison.
