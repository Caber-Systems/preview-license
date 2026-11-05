# Caber Community Preview Edition: Capabilities and Limits

## 1. Community Preview Edition Capabilities and Hard Limits

The Community Preview Edition provides the full Caber runtime governance, OBO identity propagation, document scanning and indexing, and `CaberUserConsole` observability experience for non-commercial evaluation and local development, subject to three hard-coded capacity limits (`PREVIEW_LIMITS` in PyCaber `crates/sys_config/src/limits.rs`):

| Dimension | Preview Limit | Approaching Warning (80%) | Enforcement Behavior When Reached (100%) |
| :--- | :--- | :--- | :--- |
| **Events** (`limits.events`) | **20,000 events** | 16,000 events (`"approaching"`) | Refuses new event writes to `objEventsTable` (`csi_agg_events`), freezes GSS promotions, and suspends `pycaber` SDK interception. |
| **Distinct Customer Objects** (`limits.objects`) | **500 distinct customer objects** | 400 objects (`"approaching"`) | Refuses new customer object admissions to `objScanTable` (`csi_objects_map`, `object.use_hash == false`), freezes customer storage writes (`StorageError::WriteProtected`), while allowing API/tool payload scans (`object.use_hash == true`) up to the 20,000 event ceiling. |
| **Concurrent SDK Instances** (`limits.sdk_instances`) | **5 active instances** | 4 active instances (`"approaching"`) | Refuses additional `/v1/sdk/register` requests (`accepted: false`, `reason: "preview_max_sdk_instances_reached"`). A refused or suspended SDK process stays suspended for the life of the process. |

### Monotonic Anti-Circumvention Tracking

- **Zero-Latency In-Memory Latching**: Both `events` and `objects` limits are tracked in memory on every `CoordinatorWriter` batch and reconciled monotonically against OpenSearch (`/_count`) and stream sequence high-water marks.
- **Customer Objects vs. API Payloads in `objScanTable`**: `objScanTable` (`csi_objects_map`) stores scan records for both customer S3/VersityGW documents (`object.use_hash: false`) and API/tool payload scans (`object.use_hash: true`, stored in `gss⋊⋉<bucket>/ATAP/<sha256>`). Only customer objects (`object.use_hash == false`) count against `PREVIEW_OBJECT_LIMIT = 500`.
- **Anti-Delete-and-Add (`seen_object_ids`)**: The `objects` ceiling tracks cumulative distinct canonical customer object IDs (`seen_object_ids`) as well as the monotonic OpenSearch customer object count. Deleting documents from a customer S3 bucket (for example VersityGW) or deleting records from OpenSearch and uploading new documents does **not** decrement the object count.
- **Fail-Closed Health Probing**: If OpenSearch `/_count` probes fail consecutively, the ceiling fails closed (`state: "reached"`) until connectivity is restored.
- **Boot-time re-derivation**: `caber-core` holds no count on disk. On every boot it counts `csi_agg_events` and the customer objects in `csi_objects_map` and starts its monotonic counters from there, which is why restarting or recreating the container does not reset anything, and why the supported resets in section 2 work: they remove the stored data the counts are derived from. Those resets are not circumvention; they are the documented way to start over.

---

## 2. Monitoring Limits and Resetting

### Monitoring in `CaberUserConsole` and CLI

- **Select Deployment Screen**: Displays the **Community Preview Edition** notice card with the `20,000 events`, `500 objects`, and `5 concurrent SDK instances` limits, the **Preview License & Terms** modal, and the link to the limits and reset page.
- **Top Status Banner and Toast Alerts (`PreviewLimitsBanner`)**:
  - Turns **amber** (`"approaching"`) when any dimension reaches 80 percent of capacity.
  - Turns **red** (`"reached"`) and displays reset instructions when any dimension hits 100 percent.
- **Admin Home Attention Strip**: Surfaces warning and danger attention items for `events`, `objects`, and `sdk_instances` linking directly to `/admin/platform`.
- **CLI Prerequisite Check**: Run `./demo.py check <demo>` to query `/v1/status` and inspect current preview limit state from the terminal.
- **Where the reset text comes from**: the `reset_instructions` string in the `limits` block of `/v1/status` is `PREVIEW_LIMITS.reset_instructions` in PyCaber `crates/sys_config/src/limits.rs`. It names both procedures below. The console and `demo.py check` print it verbatim.

### Resetting a CaberDemos demo

```bash
./demo.py down <demo>
./demo.py up <demo>
```

`demo.py down` runs `docker compose down -v` (removing the OpenSearch, PostgreSQL, and VersityGW volumes and `caber-core`'s anonymous `/var/tmp` volume) and then empties the bind-mounted `/shared` directory that `down -v` cannot touch. `demo.py up` starts a fresh deployment with every counter at zero and reseeds. The demo's own application containers come back with `up`; any application of the developer's own that loads the SDK must be restarted, because the SDK's `PREVIEW_SUSPENDED` latch clears only on process exit.

### Resetting a stack composed without `demo.py`

A developer who runs Caber from their own compose file has no `demo.py down`. `caber-core` therefore carries a `reset` subcommand (PyCaber `crates/caber_core/src/reset.rs`), run inside the live container, followed by a restart:

```bash
docker compose exec caber-core caber-core reset
docker compose restart caber-core
```

Then every application process that loads the SDK is restarted. Developers should stop their applications, or stop sending traffic through them, before the reset: anything written between the reset and the restart is counted by the restarted `caber-core`.

What the subcommand does, in order:

1. **Clears every `csi_*` index in OpenSearch** with `_delete_by_query` (`refresh=true`, `conflicts=proceed`). The target list is the union of `index_names::all_physical_indices()` and `_cat/indices/csi_*`, so indices outside `DEFAULT_DB_TABLES` (for example `csi_obo_chain_facts`) are included. Mappings created by `csi-init` stay in place. If any index cannot be cleared the command stops here, before touching the filesystem, and names the index; it is safe to run again.
2. **Removes the derived tree under the GSS root** (`ResolvedTarget::volume_fs_root()`, `/shared/csi-mvp-master`): `QUARANTINE`, `COMMITTED`, `CANONICAL`, `ATAP`, and anything else there, **except `customer/`**, which holds the identity files and the governance package the deployment published. Those are configuration, not collected data, and are kept.
3. **Removes `caber-core`'s working state under the local prefix** (`resolve_local_prefix(GLOBAL.localPrefix)`): `caber_core/epoch.sqlite`, `caber_core/stream_seq.sqlite`, `sdk_registry.sqlite`, `intersector/`, `staging/`, `doc_parser_work/`, `combine_shadow/`, `raw_s3_logs/`, `cqf_gss_cache/`, `pull/`, and `decision_parity_perf.jsonl`. The API key stores (`caber_core/api_keys.sqlite`, `hub_api_keys.sqlite`) are kept so the key the developer's applications use keeps working.

What it leaves alone: the object store and the documents in it, PostgreSQL, Neo4j if one is running, and the webhook relay spool. Documents still in the customer buckets count again when the fresh deployment scans them.

`docker compose exec` is required, not `docker compose run`: `run` starts a new container with its own empty `/var/tmp`, so it would clear the wrong working directory.

In the public reference `docker-compose.yaml` every piece of Caber state (OpenSearch data, `caber-core` `/var/tmp`, `/shared`, VersityGW data, PostgreSQL data, relay spool) is on a compose-managed named volume, so `docker compose down -v` followed by `docker compose up -d` is also a complete reset. It removes more than the subcommand does: the buckets and their contents, the PostgreSQL databases, and any identity or governance configuration published inside the preview. A compose file that bind-mounts a host directory into `caber-core` (as CaberDemos does for `/shared`) must delete that directory by hand, which is what `demo.py down` does.

### What does not reset the counters

- Deleting documents from customer buckets or records from OpenSearch (section 1).
- Restarting or recreating only the `caber-core` container, or `docker compose down` without `-v`: the OpenSearch volume survives and the counts are re-derived from it within seconds of boot.
- Waiting. There is no time-based reset. The one exception is an SDK slot, which frees about 60 seconds after the process's last heartbeat; the refused process still has to be restarted.

---

## 3. Copyright, Trade Secret, and DMCA § 1201 Technological Protection Measures

The Caber Community Preview Edition is proprietary software protected by United States and international copyright laws, trade secret laws, and the Digital Millennium Copyright Act (**17 U.S.C. § 1201**). The license is a no-assent copyright license: its conditions bind whoever uses the software, and breach of a condition ends the license without any cure period. The notice text is [LICENSE-PREVIEW.md](https://github.com/Caber-Systems/preview-license/blob/v1.1/LICENSE-PREVIEW.md); this section summarises the terms that the code and the docs rely on.

1. **Evaluation-Only License Grant**:
   - Licensed for evaluation, development, testing, and demonstration. No production use and no commercial use (paid or not, internal or not).
   - No redistribution of the software or its images, wheels, or binaries.
   - No tampering with the limits or the mechanisms that enforce them. The reset procedures documented in section 2 are the supported way to start over and are expressly not tampering.
   - No reverse engineering, decompilation, disassembly, or extraction of embedded scripts, models, or ontologies, **whether by hand or by AI**: feeding the software, its binaries, its outputs, or its telemetry to a model or agent to reconstruct, approximate, or train a substitute is prohibited. Using an AI assistant to write an application that uses the Caber SDK is fine.
   - No cloning: building or training a substitute from the software or its outputs.
   - Keep the copyright and license notices intact.
   - Benchmarks and write-ups are permitted. Caber asks for a heads-up before numbers are published so the configuration can be checked, and does not require consent.
2. **DMCA 17 U.S.C. § 1201 Technological Protection Measures (`secure_connect`)**:
   - `caber-core` (`/v1/sdk/register` and `/v1/sdk/heartbeat`) issues time-bound, HMAC-SHA256 cryptographically signed capability tokens via `crates/secure_connect` (`create_secure_token` / `verify_secure_token` and `tamper_resistant::LicenseInfo`).
   - The native `pycaber_wrap` (`streaming_core`) extension verifies these tokens in compiled Rust code before permitting request/response interception or OBO governance execution. Missing, expired, or tampered tokens (for example, proxying heartbeat responses to alter `"state": "reached"`) immediately latch `PREVIEW_SUSPENDED = true`.
   - The limit counters and the write freeze (section 1) are also technological protection measures. Circumventing them, as opposed to running the documented resets, is a § 1201 matter as well as a license breach.
3. **Binary and Asset Hardening**:
   - All 27 Python document-runner scripts and ontology assets are compiled into the `caber-core` binary (`embed-python-scripts`), verified with `xxh3_64` integrity digests, and isolated from runtime directory overrides.
   - Release wheels and binaries are built with Cython native compilation (`PYCABER_COMPILE_PY=1`), LTO, and stripped symbols.
   - The preview is **not security hardened** for production exposure. The notice says so and carries no invitation to security research; the no-warranty section covers it.

Upgrade information: <https://caber.com/upgrade>.
