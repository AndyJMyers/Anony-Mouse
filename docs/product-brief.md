# Anony Mouse — initial product brief

## Proposition

A deliberately simple, discreet adult dating service with a sexual focus. A description of who you are, a description of what you want, a public image that need not be identifiable, and private messaging. Proposed price: £25 once, with no further membership fees.

## Agreed essentials

- Pseudonymous profiles and optional identifying images.
- No validation of users' identity claims; patrons assess those claims themselves.
- Private text and image exchanges.
- Ordinary messages and attachments expire 14 days after sending.
- Up to 100 keepsake messages per user.
- Privacy aimed at avoiding unnecessary public disclosure, rather than claiming invisibility to service providers or authorities.

## Map discovery UI

Enter a partial postcode (outward code), such as GU2, and explore potential matches on a map. Match markers pulse gently and show short, patron-authored hints about what they seek or offer. Selecting a marker opens a profile and a message-request action.

Use district-level approximate placement, with an explicit explanation that markers are illustrative locations, not homes or live positions. Do not request GPS access or store exact addresses for this flow. Avoid implying somebody is online merely because their marker pulses. Provide a list view and reduced-motion option. Hints are controlled by the patron; do not infer or expose private sexual preferences beyond what they choose to publish.

## Motivation

The primary goal is the fun of making the project. Commercial success and notoriety are optional bonuses. Keep the pilot simple and spending bounded.

## Suggested launch scope

- Adult age range and broad location rather than exact address or public coordinates.
- Message requests, acceptance, blocking and reporting.
- Strip image metadata; compress uploads and limit attachment sizes.
- Discreet notifications with message previews disabled by default.
- Account deletion and a clear explanation of retention.
- Text and still images initially; video and voice would add complexity.

These are implementation proposals, not yet final decisions.

## Decisions before implementation

- Adults-only access and age assurance, considered separately from identity verification.
- Account access and recovery without exposing email or phone details to patrons.
- Whether saving a received message requires the sender's consent, and how withdrawal works.
- Whether the 100 keepsakes include both text and images, and the maximum size of each.
- Precise retention for backups, reported content and deleted accounts.
- Private image access controls and the level of message encryption.
- Geographic launch area, platform and payment route.
- Operational handling of reports and account problems.

## Pilot economics

100 paying patrons at £25 produce £2,500 in gross one-off receipts, before payment fees and any applicable deductions. This is a runway, not monthly recurring revenue.

The proposed £100 experiment budget should be treated as an initial infrastructure spending cap with a defined stop/review point. It does not cap development time, support labour or all costs of launching an adult dating service.

Expected engagement of one or two hours a day is the founder's hypothesis, to be tested. Time online affects concurrent connections; message counts, image uploads and downloads determine other usage costs.

Short retention bounds accumulated storage. It does not eliminate delivery costs or maintenance. Track active users, peak concurrent sessions, messages, images, reports, spending and new paid memberships during the pilot.
