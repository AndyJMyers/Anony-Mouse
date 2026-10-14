# Anony-Mouses — priorities and TODO

Reviewed 14 October 2026.

## Goal

Keep the established atmosphere: **adult, playful and a little louche**. Build a small real adult dating service behind the prototype, then launch nationally with distinctive creative and tailored outreach. Making it is part of the pleasure; revenue and notoriety are possible bonuses.

## Already done

- [x] Public GitHub repository and live HTTPS GitHub Pages concept preview.
- [x] Technicolor mouse artwork and coherent responsive visual design.
- [x] Fictional postcode map, pulsing markers, profile hints and map/list views.
- [x] Demo details-to-payment journey, scripted chat and session-only keepsakes.
- [x] Agreed direction: launch month free, then £25 for a year, with £25 annual renewals.
- [x] National launch ambition and core brand language captured.

These are completed design/concept tasks. The preview does not yet provide real accounts, geographical search, messaging, membership or payment.

## Implementation status — 14 October 2026

- [x] Preview pricing changed to one free calendar month from signup, then £25/year with manual renewal; core brand line added.
- [x] Hosting/payment/age/privacy foundation review and provider enquiry brief prepared: [review](docs/foundation-review.md).
- [x] Hosting growth paths and specific local-backend limits reviewed: [hosting and growth](docs/hosting-and-growth.md).
- [ ] Before real users: PostgreSQL persistence, pagination/indexed discovery, shared rate limits and portable private media storage.
- [ ] Rehearse a second app instance, data migration/restore and representative burst-load tests; obtain actual provider quotes and acceptance.
- [x] Local persistent account, district-discovery and private text-message core built: [backend](backend/README.md).
- [x] Twelve tests pass, covering the two-account flow and access/retention boundaries.
- [ ] Suitable production host and payment account approved; age assurance integrated.
- [ ] Polished live UI connected to backend; district lookup coverage and secure image handling added.
- [ ] Production retention, payment entitlement/webhooks and operational testing completed.

The local API is deliberately not deployed publicly and is not wired into the GitHub Pages mockup. The fixture postcode data and adult checkbox are for fictional testing only. The first end-to-end **API** milestone is tested; the real-user website milestone remains open.

## Ordered priorities

| Order | Priority | Work | Completion evidence |
| --- | --- | --- | --- |
| 1 | Now | Align the public preview with one free month, then £25/year; add the core brand line. Preserve its visual character. | Website, checkout demo and README agree on pricing and trial terms. |
| 2 | Before backend commitment | Confirm a hosting and payment route suitable for the actual adult dating service and intended user-uploaded content. Define 18+ access, reporting duties and privacy approach using current authoritative guidance. | Providers accept the described business/content; implementation choices, baseline monthly costs and launch obligations documented. |
| 3 | First working milestone | Accounts, login/recovery, editable profiles, public image and real outward-postcode discovery with approximate map placement. | Two test adults can sign in separately, edit their profiles and discover each other without exposing contact details or precise location. |
| 4 | First working milestone | Private message requests, text and image messaging, block/report, upload limits and image metadata removal. Decide encryption before storing real exchanges. | The two test adults can exchange messages; a third account cannot read them; blocking and reporting work. |
| 5 | Before taking users | Implement 14-day expiry, 100 keepsakes, account deletion and disclosed backup/reported-content retention. | Time-controlled checks demonstrate expiry, keepsake limits, removal and deletion behavior including attachments. |
| 6 | Before paid launch | Trial entitlement, payment-provider checkout, verified payment events, one-year access and renewal. Preserve one page of details then one entrance/payment page. | Test payments grant the correct access; duplicates cannot grant it twice; trial end, expiry and renewal behave predictably. |
| 7 | Before campaign | Operational trial across desktop and phones; spending alerts, capacity check, recovery exercise and report handling. | A small private test cohort completes the core journey; spending and support work are visible and manageable. This is testing, not a geographically limited marketing launch. |
| 8 | In parallel, release after readiness | Prepare national campaign: influencer/creator press kit, student publication/union copy, podcast/journalist pitches and distinct MP-office copy. Build a reviewed contact list and appropriate sending process. | Finished creative and tailored copy, checked recipients and campaign delivery plan; no unreviewed mass send. |
| 9 | Launch and learn | Launch nationally; monitor signup, activity, conversations, trial conversion, renewals, reports and costs. | Decisions use observed results, while keeping public anonymity claims honest. |

## Decisions to settle

- [ ] Trial: proposed default is a full month from each signup, rather than one shared calendar launch window. Confirm exact duration and billing language.
- [ ] Renewal: proposed default is an explicit £25 purchase each year, without automatic charging.
- [ ] What remains available after a trial or membership expires: profile visibility, old conversations, keepsake access and deletion.
- [ ] Whether a sender can withdraw a message/image saved by another patron; explain that downloaded copies/screenshots cannot be recalled.
- [ ] Keep actual identity claims unverified, while choosing workable adults-only access and account recovery.
- [ ] Filters and matching: interests, age ranges, distance and mutual preferences; keep the initial controls small.
- [ ] Public hints must be patron-authored and approved by them; never infer or expose private preferences.
- [ ] A £100 initial infrastructure experiment cap and a clear review point; do not treat it as a cap on development/support labour or all launch expenses.

## Keep for later

- Native mobile apps, video/voice calls, elaborate recommendation systems and paid boosts.
- Additional artwork before core behavior works; the present artwork already establishes the brand.

## Next development objective

Resolve production provider/content/age-assurance choices, then connect the polished interface to the tested core: **two accounts → discover → request a conversation → exchange a private message**. Add private images and real district lookup coverage before live-user testing.

GitHub Pages remains the static concept showcase. Real membership, sensitive exchanges and payment require suitable production hosting and backend services.

## Connected lounge milestone — 14 October 2026

- [x] Same-origin local member UI: two-page registration/trial, login and recovery-code handoff.
- [x] Profile editing/hiding, district discovery with schematic pulsing markers, requests/acceptance, private text, 100 keepsakes, block/report and deletion.
- [x] Local server serves an explicit asset allowlist; source/runtime files remain inaccessible.
- [x] HTTP integration checks exercise separate session cookies and exclude a third patron.
- [x] anonymouses.com configured and verified in GitHub Pages, with HTTPS enforcement.
- [ ] Production host and PostgreSQL migration, provider approval and age assurance.
- [ ] Private image attachments and metadata removal, national district coverage, payment integration and live-user readiness checks.

The local interface uses fictional adult accounts. The Pages showcase does not call the backend or open public registration.
