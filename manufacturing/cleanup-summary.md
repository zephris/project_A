# Project consolidation

Removed 2,634 stale files (804.1 MiB recorded) from superseded manufacturing releases, historical order/production outputs, backups, preview dependencies, intermediate simulation runs and one-time patch/consolidation scripts. Exact deleted paths/counts are in cleanup-manifest-2026-10-07.json. The initial dependency deletion restriction was resolved after explicit user approval.

Retained active KiCad sources, configured libraries, models, vendor provenance/licenses, current manufacturing package with final DFM evidence, mechanical design principles/candidates, reproducible CAD dependencies/generators, and the 14-case SPICE generator/runner with latest runs and corner evidence. Choc V1 mechanical candidates remain reference material pending V2 fit validation; they are not approved V2 plates.

C41 assigned C29936; BOM/CPL match 112 designators. Removed the stale assembly note. Complete ZIP rebuilt and checksum supplied. Fresh DRC has zero unconnected items; 70 library notices/two source silk overlaps remain. File hashes and ZIP integrity verified. Online assembly matching/preview was not rerun.

Package regeneration: python manufacturing/package_current.py. SPICE consistency: python spice/run_suite.py --check. The special silk generator remains under stage2_work/dfm_resolution_2026-10-06; it uses an auxiliary board for silk only. Never use that board for copper/mask/drills/placement export.
