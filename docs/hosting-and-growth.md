# Hosting and growth due diligence

Reviewed 14 October 2026. This is a researched architecture recommendation, **not** a load-tested capacity guarantee or an approved hosting contract.

## Recommendation

Keep GitHub Pages as the fictional concept showcase. For the real paid service, favour a portable application, PostgreSQL, private S3-compatible object storage and a domain we control. Start with a modest deployment on a provider that accepts the complete business/content model; add capacity and resilience as measured demand requires it.

The aim is to move or enlarge infrastructure without rewriting the product or forcing patrons to recreate their accounts. A million-account service is not a change of tariff alone. Portable components reduce the migration work; they do not remove database tuning, traffic engineering or operational responsibilities.

Do not purchase a million-user installation now. Do remove the avoidable single-machine dependencies before real users accumulate.

## What customer numbers mean

Registered customers, daily active patrons, peak simultaneous sessions, text messages, image uploads and image views are separate quantities. Provider selection and estimates need all of them. A national campaign can spike anonymous page visits and registration/password-hashing load before it produces sustained chat activity.

The following is an illustrative planning case, not a prediction:

| Assumption or derived quantity | Illustration |
| --- | --- |
| Registered accounts | 1,000,000 |
| Daily active patrons | 100,000 (assumed 10%) |
| Time online per active patron | 2 hours/day |
| Average concurrent sessions over 24 hours | About 8,333 |
| Planning peak concurrency | 25,000 (assumed 3 times average; must be measured) |
| Text messages per active patron | 50/day |
| Text message volume | 5 million/day; about 58 sends/second on average |
| Images per active patron | 5/day, averaging 500 KB each |
| Daily new image data | About 250 GB |
| 14-day ordinary image retention | About 3.5 TB, before replicas/backups/reports/keepsakes |
| Worst-case image keepsakes | 1 million patrons × 100 images × 500 KB = about 50 TB |

Retention controls steady-state storage, but not upload/delivery traffic. The 100-keepsake limit bounds count, so attachment size must also be bounded. Trial accounts, expired memberships, report evidence and backups need their own retention rules. The example excludes all those details.

Polling can dominate the workload: 10,000 open clients checking every five seconds would generate 2,000 checks/second even while few messages are sent. Use an appropriate live event delivery mechanism for active conversations, backed by durable message records; reconnecting clients must be able to catch up.

## Hosting routes compared

These are **technical candidates**, not approved vendors. Content policy fit must be confirmed separately for compute, media storage, identity/age services and payment.

| Route | Start-small benefit | Growth path | Migration cost / limitation | Verdict |
| --- | --- | --- | --- | --- |
| Portable app + PostgreSQL + private S3-compatible storage | Conventional components; can use a modest server or managed compute | More app instances, load balancer, database upgrades/read replicas where appropriate, background workers; later partitioning if measured need | Provider moves still require data transfer, key handling, reconciliation and cutover; managed database availability costs have a floor | Preferred architecture |
| AWS-style managed components: ECS/Fargate, RDS PostgreSQL, S3 | Managed service availability and defined autoscaling mechanisms | Add tasks behind a load balancer, adjust database/storage independently, request quota increases | More setup and billing dimensions; image egress and managed-service minimums require a quote/model | Strong scale-oriented shortlist, not automatic adult-content approval |
| Cloudflare-native Workers + D1/Durable Objects + R2 | Useful low-entry-cost primitives and edge delivery | Partition workload over databases/objects, use live connection primitives and object storage | Current Python/SQLite app is not a drop-in Worker. D1 has an unraisable 10 GB per-database limit and single-threaded query execution per database, so scale-out needs deliberate partitioning | Credible alternative; higher platform-specific redesign/exit cost |
| Adult-content-accepting dedicated host, conventional stack | Explicit content fit may be easier to establish | Bigger server then multiple servers/private networking; PostgreSQL and object storage remain portable | Hardware upgrades do not supply app/database autoscaling; more operations responsibility; dedicated hosting may be excessive for a tiny pilot | Policy-fit option, quote and managed-service capability required |
| GitHub Pages | Already hosts the design cheaply | CDN delivery for a static showcase | Not a backend and not the host for this paid service | Showcase only |

AWS documents ECS task autoscaling and load-balancer integration, RDS PostgreSQL, and private object access using signed S3 URLs. Cloudflare documents R2's S3 compatibility, including unsupported operations: compatibility is useful, not identical behavior. Avoid coupling the app to provider-specific object features unless needed.

NovoServe explicitly advertises legal adult-content hosting on dedicated servers. This establishes a candidate's published policy, not acceptance of Anony-Mouses or an economical starter plan. AWS/Cloudflare technical capability does not establish commercial/content approval. Ask vendors about the actual intended private-image exchanges rather than describing only an innocuous landing page.

## Current code: honest scale assessment

The present local backend is a tested behavioral foundation, not a scalable production deployment:

- It uses a single local SQLite file and a standard-library development HTTP server. SQLite permits only one writer at a time; write-intensive multi-server deployments are a reason to choose a client/server database.
- Discovery fetches candidate profiles and filters distance in Python, with extra profile queries per candidate. It needs indexed district/neighbour relationships or database-side filtering and pagination, not a scan across millions of accounts.
- Rate-limit state lives inside one process. Multiple instances need a shared store or an enforced gateway layer.
- Message reads fetch a whole accessible conversation and perform expiry cleanup inline. Add pagination/indexes and scheduled bounded cleanup jobs.
- Sessions already live in the database, which is helpful; a larger deployment still needs connection pooling and efficient indexed lookups.
- One environment-held encryption key is adequate for a local test, not production key custody/rotation. A migration must preserve access to ciphertext without exporting keys carelessly.
- Image handling, live delivery, production HTTP serving, approved age/payment providers, robust backup/recovery and moderation operations are unfinished.

These are specific implementation changes. They do not require changing the mice, the user experience or public pseudonyms.

## Path from hobby to larger service

| Stage | Infrastructure direction | Evidence needed before moving on |
| --- | --- | --- |
| Concept | Static GitHub Pages, fictional data | Design and proposition clear; already live |
| First real pilot | Production HTTP app, PostgreSQL, private object storage; one region; proper backups and approved integrations | Two real test patrons complete the journey; access checks pass; backup restore succeeds; costs measured |
| Growing service | Two or more app instances where reliability/load requires them, shared limits/cache, durable background jobs, live event delivery | Same user/session works across instances; measured latency and errors stay acceptable; app-node failure does not lose durable messages |
| Large national service | Autoscaled app/live-connection capacity, database tuning/partitioning where required, media delivery controls, stronger recovery and support | Representative load and burst tests, quota headroom, incident exercises, measured cost per active patron |

Those stages are capability checkpoints, not fixed customer-count promises. One region can serve a national audience; global multi-region writes are not an initial requirement. A well-indexed relational database can serve a substantial workload, but no million-customer claim is justified without testing this application's queries, contention and traffic pattern.

## Make transition cheap now

1. Own the domain and keep normal HTTPS endpoint names, so a host change need not change links or branding. DNS redirects traffic; it does not move users, media, databases or encryption keys.
2. Introduce storage/provider interfaces and versioned schema migrations; use PostgreSQL for the real-user backend before there is a large SQLite migration to perform.
3. Keep media private, outside app disks, with stable object identifiers. Authenticate every access and use short-lived delivery credentials where appropriate. Public CDN caching is inappropriate for private exchanges.
4. Keep sessions, memberships and durable messages outside individual app instances. Treat WebSocket/event connections as replaceable and make reconnection recover missed messages.
5. Keep age-assurance and payment adapters separate. Preserve account IDs, trial dates and memberships if a provider changes. Payment portability is a separate issue: stored cards/merchant tokens may require provider cooperation; do not promise automatic transfer.
6. Make restore/export/migration a rehearsed operation rather than trusting that data can theoretically be downloaded. Include expiry/keepsake/report rules in reconciliation.

## Concrete due-diligence gates before provider selection

- Written acceptance or an authoritative service-specific policy match for the complete content/business model; age/payment requirements understood.
- Quotes for a modest pilot and the explicit illustrative workload above, separating compute, database, storage, uploads/downloads, requests, backups, support and provider fees.
- Quotas and the process/lead time for raising them; limits are not always removed by upgrading a plan.
- Full data export and media copy path; retention, deletion and backup rules survive a provider move.
- UK/EU data-region options, contractual data roles, subprocessors and incident/support arrangements assessed for the actual service.
- A working second app instance against the same database, plus representative load and backup-restore exercises.
- A planned deployment/cutover with verification and rollback, or a controlled maintenance period while the service is still small. Changing DNS by itself is insufficient.

No vendor enquiry has been sent, no account has been opened, no spend committed and no scalability benchmark performed. The architectural path is established; commercial acceptance, quotations and empirical capacity remain open.

## Sources

- SQLite concurrency and appropriate uses: https://www.sqlite.org/whentouse.html
- ECS service scaling: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-auto-scaling.html
- ECS services/load balancing: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html
- RDS PostgreSQL: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html
- Private S3 object access: https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html
- Cloudflare D1 limits: https://developers.cloudflare.com/d1/platform/limits/
- R2 compatibility: https://developers.cloudflare.com/r2/api/s3/api/
- NovoServe adult-content policy: https://novoserve.com/knowledge-base/what-is-your-policy-on-adult-content
- AWS acceptable-use policy: https://aws.amazon.com/aup/
- Cloudflare service terms: https://www.cloudflare.com/terms/ and https://www.cloudflare.com/service-specific-terms-application-services/
