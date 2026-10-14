![Anony-Mouses — Technicolor mice flirting in a glamorous jazz club](assets/anony-mouses-masthead.png)

# Anony-Mouses

A super simple dating app for adults seeking flirtation, sex and connection.

**A little about you. A little about what you want. See who answers.**

£10 per calendar month, paid up front, with explicit manual renewal and no public free trial. A possible day pass has a £1/day ceiling but is not implemented. The concept preview demonstrates this proposed business model; it does not create memberships or take payments.

## The idea

- Describe who you are and what you want.
- Choose a pseudonym and a profile image; the image need not identify you.
- Enter a partial postcode such as GU2; explore gently pulsing potential matches and patron-written hints on a map.
- Browse profiles and exchange private messages and images.
- Messages and attachments automatically expire after two weeks unless saved as keepsakes.
- Each patron may retain up to 100 keepsake messages.
- No verification of patrons' identity claims. Caveat emptor.

Discretion from the neighbours is the aim. Patrons control what they disclose, but other people may recognise them or copy what they receive. Identity claims are unverified; absolute anonymity is not promised.

## Project status

Interactive static concept preview: fictional postcode matches, mood filters, surprise introductions, optional opening lines, scripted chat, session-only keepsakes and a two-step signup demo. No real accounts, payment collection or production messaging service yet.

Open `index.html` to explore the design. GitHub Pages publishes the project from the root of `main`. The commercial service will require suitable backend hosting; GitHub Pages is not the paid-service host.

The prototype uses no analytics or browser storage. Form details, selected pictures and keepsakes remain in page memory and disappear on reload. A stylesheet requests optional Google Fonts; no form contents are sent to Google.

See [the product brief](docs/product-brief.md) for scope and [the prioritised TODO list](TODO.md) for implementation and national launch planning.

## Development foundation

A separate [local backend](backend/README.md) now implements persistent accounts, district-based discovery and private text conversations. The connected member lounge at `http://127.0.0.1:8080/members.html` supports signup, sign-in, profile editing, schematic district discovery, accepted conversation requests, private text and image messages, keepsakes, blocking, local reports, recovery and deletion. Twenty-two automated tests cover the core and the HTTP journey, including cookies, access isolation and static-file boundaries. Production use is disabled; the public mockup remains fictional.

See the [foundation review](docs/foundation-review.md) for hosting, payment, age assurance and privacy findings and unresolved provider requirements.

## Provider selection and deployment

See [the provider decision and cost model](docs/provider-decision.md) and [the deployment plan](docs/deployment-plan.md). Accounts now start unpaid; an internal monthly-payment ledger is tested, but real provider verification/checkout and production deployment are pending.

## Android track

See [the Android development track](docs/android-track.md) for a shared minimal interface and delivery order. The native app will use the same account/message service; no Android build has been released yet.

## Artwork

Masthead created with AI for Anony-Mouses: a glamorous adult female mouse blowing a Monroe-style kiss to a suave adult male mouse, in saturated Technicolor.

## Ownership

Project by Andy J Myers. No open-source licence has been granted at this stage.
