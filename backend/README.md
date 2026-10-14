# Local backend foundation

This Python API is for fictional adult test accounts on your own computer. The member lounge connects to it locally; it is not connected to the public GitHub Pages demo and is not a public production service.

## Implemented and tested

- Persistent pseudonymous accounts; scrypt password hashes, opaque sessions and CSRF tokens.
- A separate chosen profile name and private login handle; no email or phone required in this development model.
- A one-use recovery code, rotated on recovery; old sessions are revoked.
- Editable profiles, hiding, and distance-based discovery using imported **outward postcode centres**.
- Conversation requests and acceptance before text messaging.
- Access checks preventing a third account from reading or saving another conversation.
- Server-side encryption at rest for profile descriptions, text messages and report evidence. **Not end-to-end encryption**; the server holds the key.
- Blocking, reporting (including after blocking), and account deletion.
- One calendar month of trial access, using UTC and clipping month-end anniversaries.
- Text messages expire after 14 days. Only the individual patron who saves an expired message can read their keepsake; saving does not retain it in the other person's inbox. Limit: 100 per patron.

## Run locally

From the repository root, use Python 3.11 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export ANONY_MOUSE_DATA_KEY="$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')"
python -m backend.server --seed-test-districts
```

Keep the same data key if reusing the database; losing it makes encrypted data unreadable. The key is supplied through the environment, not committed. Put persistent runtime state outside the repository. Never use this developer key setup for public deployment.

The server listens only at `http://127.0.0.1:8080`; it serves the website and JSON API from the same origin. Open **http://127.0.0.1:8080/members.html** for the connected member lounge. Cookies and CSRF remain on this origin; no cross-origin API URL is accepted. The public Pages copy of the lounge is disabled. `--seed-test-districts` imports three deliberately approximate fixtures: GU2, GU1 and SW1A. Nationwide district lookup coverage is still required, through a small outward-code table or cached district lookups. No full postcode/address database is needed. These fixture coordinates must not be presented as production geography.

Tests:

```bash
python -m unittest discover -s tests -v
```

Cleanup:

```bash
python -m backend.server --purge
```

Reads also run expiry cleanup, but a real service needs a scheduled cleanup task. Report evidence has a separate **development-only 90-day rule**. Production report retention and backup expiry are unresolved. Account deletion removes shared conversation data and keepsakes via cascading deletion; independently retained report evidence is anonymised and follows its own expiry. These semantics need product review before real use.

## Try the connected lounge

1. Start the server with `--seed-test-districts`, then open `/members.html` at the loopback address above.
2. Choose **Come on in**, enter invented adult details, then start the test month. Save the one-time recovery code.
3. Open a separate browser profile or a private window for a second invented account. Ordinary tabs share a session cookie.
4. Search GU2 or GU1, send a hello, and accept it from the second account's Conversations view.
5. Exchange text, save/remove keepsakes and refresh or reload to confirm persistence. The open Conversations view polls every 10 seconds while visible.
6. Edit/hide profiles, block, submit a local test report, recover access, or delete an account using the corresponding controls.

No public signup, payments, image uploads or full district coverage is enabled. Reports remain local test records, without a monitored support inbox. No real personal or sexual data should be entered.

## API

All POST requests require `Content-Type: application/json`. Authenticated mutations also require the `X-CSRF-Token` returned by login. Sessions use an HttpOnly, SameSite=Strict cookie. No CORS is enabled.

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/api/districts` | GET | Imported district centres for the local schematic map |
| `/api/health` | GET | Confirms development mode |
| `/api/register` | POST | login, password (12+ characters), alias, bio, wants, district, age_range, adult=true, consent=true |
| `/api/login` | POST | login, password; returns CSRF token and cookie |
| `/api/recover` | POST | login, recovery_code, new password |
| `/api/session` | GET | Own profile, trial status and CSRF token |
| `/api/logout` | POST | Revoke current session |
| `/api/profile` | GET / POST | Read or edit own profile |
| `/api/discover` | POST | district, radius_km (1–200) |
| `/api/conversations` | GET / POST | List conversations or request one with target account ID |
| `/api/conversations/{id}/accept` | POST | Recipient accepts |
| `/api/conversations/{id}/messages` | GET / POST | Read or send body text |
| `/api/keepsakes` | GET | Own saved messages |
| `/api/keepsakes/{id}` | POST / DELETE | Save or remove a keepsake |
| `/api/block` | POST | Block target account ID |
| `/api/report` | POST | target, reason, optional message_id |
| `/api/account` | DELETE | Delete current account |

## Still required

Production hosting, age assurance, provider checkout/webhooks, paid entitlement, image upload/access control/metadata stripping, national postcode data, production UI deployment, moderation tools, durable rate limits, a production HTTP server, TLS, Secure cookies, encryption-key management/rotation, backup/recovery and operating procedures.

An `adult=true` flag is only a fictional-test assertion. It is **not** production age assurance. There is no payment or age-verification override endpoint. Attempting to initialise the service in production mode fails closed. The development HTTP server must not be exposed through a reverse proxy or port forwarding.
