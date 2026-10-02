# Personal portfolio and studio scope

Updated October 2, 2026.

Alexander’s personal portfolio covers his broader body of work. Its `/projects`
index separates confirmed client work, personal AI research, other applications,
design/publishing, and earlier GitHub work. Selected work remains on the homepage.

The user identified Joneva and Miriam’s Corner as client projects. Joneva includes
its public website, Portal / HR Manager, and Wayfare. Their brand ownership is
credited to the clients. Their presence in Codehub does not establish delivery
through EdenTV. They therefore belong in the personal client-work section, with
a link from the studio rather than studio product cards.

EdenTV remains a creative studio website for software, media, and documentation.
Existing featured applications are not relabeled as studio-owned without further
evidence. Founder experiments are explicitly identified and not presented as
released products. Support and policy documents remain available.

Current source corrections: ParkMemory Hub uses CloudKit; the Joneva Portal’s
retired payroll features are excluded; AutoResearch includes specialist, tool,
and memory experiments with unresolved reliability limits; Lumina is a
framework-independent design-system package, separate from the personal website.

The portfolio project index also includes PayNow and SplitCanvas. Duplicate
PulseTrackr checkouts and the autobiz alias are not separate projects. The
real-estate experiment is attributed to AutoBiz. Earlier GitHub projects are
listed separately from current local projects.

Release checks: portfolio lint, TypeScript and production build; studio document
tests and HTML checks; responsive browser checks; push and exact remote SHA
verification before deployment; live content and link checks afterward.

## iOS document and routing update — October 2, 2026

Only the four featured iOS apps receive the standardized four-document set:
PulseTrackr, ParkMemory Hub, JxL Scheduler, and Kasapa. Existing 11 documents
retain their review dates and public addresses. Added JxL terms and four Kasapa
pages from the local-first implementation, README, and relationship/persistence
contracts. Kasapa is a prototype; no App Store approval, remote delivery,
moderation service, or server-side deletion is claimed.

`app_documents.py` owns app/document identities. `build_documents.py` rebuilds
additions, cards, legal indexes, metadata, and the 16-document search index.
Existing iOS policy bodies are preserved. New overview pages connect each app
to its documents. Other projects receive an overview/package link rather than
manufactured policies. No client-owned terms are created.

Internal links and search results use canonical extensionless paths. `_redirects`
provides six short URLs; root `404.html` prevents Cloudflare's SPA fallback from
returning the homepage for unknown routes. Existing `.html` URLs remain valid.

The 26 Python checks cover document completeness, links and anchors, search
extraction, card actions, overview links, and static redirect targets. Live HTTP
checks remain necessary to verify deployed response codes and redirects.
