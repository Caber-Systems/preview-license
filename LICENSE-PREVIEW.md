# Caber Community Preview Edition License Notice

Version 1.1, November 4, 2026. This notice applies to the preview build it ships with.
Copyright (c) 2026 Caber Systems, Inc. All rights reserved.

## The short version

You can run this preview in your own environment to evaluate Caber. It is free, it has
hard limits that are enforced in code, and it comes with no warranty. You do not have to
click "accept": if you use the preview, this notice is the only permission you have to do
so, and the rules in sections 2 and 3 are conditions of that permission. Break one and the
permission ends. The sections below are the operative text; this summary is only a guide.

Want to do something this notice does not allow? Ask: support@caber.com.

## 1. What you can do

Caber Systems grants you a free, non-exclusive, non-transferable, non-sublicensable license
to install, run, test, and demonstrate the Community Preview Edition ("the Preview") in
environments you control, for the purpose of evaluating Caber.

Evaluation includes, for example:

- Running it on your laptop or in a lab or staging environment.
- A proof of concept inside your company to decide whether to buy Caber.
- Demonstrating it to your team, your management, or at a meetup or conference.
- Writing or recording about your experience with it, including benchmarks. If you
  publish numbers, we would appreciate a heads-up so we can check the configuration
  with you first.

Code you write against the documented Caber SDK and APIs is yours. Data you feed the
Preview, and the events, graphs, policies, and reports it produces from your data, are
yours.

## 2. What you can't do

Each item below is a condition of the license in section 1, not just a promise you make.
If you do any of them, you are outside the license and your use of the Preview is
unlicensed under copyright law.

- **No production or commercial deployment.** Don't run live traffic or real customer data
  through it, don't offer it to others as a service, and don't embed it in a product.
- **No redistribution.** Don't share, mirror, or repackage the container images, wheels, or
  binaries. Point colleagues at the download instead.
- **No tampering with the limits.** Don't remove, alter, disable, or work around the preview
  limits or the license and integrity checks that enforce them (section 3). The reset
  procedures Caber documents are not tampering; they are the supported way to start over.
- **No reverse engineering, by hand or by AI.** Don't decompile, disassemble, or otherwise
  reverse engineer the Preview, and don't extract its embedded scripts, ontologies, or
  model artifacts. This applies equally when a tool does the work for you: don't feed the
  Preview's binaries, compiled extensions, embedded assets, disassembly, memory dumps, or
  captures of its SDK protocol and tokens into a language model, coding agent, or other
  automated analysis system, whether as a prompt, as context, or as training data, in
  order to analyze, reconstruct, re-implement, or describe how it works. This condition
  applies except to the limited extent applicable law expressly overrides it.
- **No cloning.** Don't use the Preview, its embedded assets, or its output to train or
  fine-tune a model, or as source material to build a product that substitutes for Caber.
- **Keep the notices.** Don't remove this notice or Caber's copyright notices.

What is fine: using an AI coding assistant to write or debug your own integration against
the documented SDK and APIs, including pasting in error messages the Preview emits.

## 3. Preview limits and how they are enforced

The Preview enforces these limits in code. They are not honor-system settings.

| Limit | Value | When reached |
| --- | --- | --- |
| Events | 20,000 | New events are no longer recorded and the SDK stops intercepting and governing traffic. Your application keeps running. The console keeps working for data already collected. |
| Distinct customer objects | 500 | New documents from your object sources are no longer admitted. The SDK stops intercepting and governing traffic. |
| Concurrent SDK instances | 5 | Additional SDK processes are refused and run ungoverned. |

The console warns at 80 percent. To start over, reset the deployment: for a CaberDemos
demo, run `demo.py down <demo>` then `demo.py up <demo>`; for a stack you composed
yourself, run `docker compose exec caber-core caber-core reset` and then
`docker compose restart caber-core`. In both cases, restart any of your own applications
that load the SDK afterwards. Deleting documents does not lower the object count.
Details: https://github.com/Caber-Systems/preview-license/blob/v1.1/PREVIEW_LIMITS.md

**Anti-circumvention notice (17 U.S.C. § 1201).** Access to the Caber runtime, SDK
interception pipeline, and governance engines is controlled by cryptographic measures:
time-bound HMAC-SHA256 capability tokens issued at SDK registration and heartbeat, and
integrity digests on embedded assets. These are technological protection measures under
the Digital Millennium Copyright Act. Intercepting, spoofing, extracting keys from,
patching, or otherwise circumventing them, whether by hand or with automated or AI
tooling, is prohibited by that statute independently of this license.

## 4. Your data and privacy

The Preview runs entirely in your environment. It does not send events, documents,
telemetry, or usage data to Caber.

## 5. Feedback

We would like to hear what works and what does not. If you send us bug reports,
suggestions, or other feedback, you give Caber permission to use it for any purpose
without obligation to you. Don't send us anything confidential.

## 6. No warranty, no liability

This is pre-release software. It can have bugs, it can change or break between builds,
and it is not suitable for regulated or production data. The Preview is not security
hardened: it exists to show what Caber's governance does, not to represent the security
posture of the commercial product, so keep it off untrusted networks and don't read scan
results against it as findings about Caber.

TO THE EXTENT PERMITTED BY LAW, THE PREVIEW IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY
KIND, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE, AND NON-INFRINGEMENT. CABER SYSTEMS WILL NOT BE LIABLE FOR ANY DAMAGES
ARISING FROM YOUR USE OF THE PREVIEW, INCLUDING DIRECT, INDIRECT, INCIDENTAL, SPECIAL, OR
CONSEQUENTIAL DAMAGES, EVEN IF ADVISED OF THEIR POSSIBILITY.

Some jurisdictions do not allow some of these exclusions. Where that is the case, they
apply to the fullest extent the law allows, and Caber's total liability is limited to the
amount you paid for the Preview, which is zero.

## 7. When the license ends

The license ends automatically if you breach a condition in section 2 or 3. When it ends,
stop using the Preview and delete your copies. Sections 4 through 8 survive.

Caber may discontinue the preview program or publish a new build under a new notice.
That does not change the terms for a build you already have. The notice shipped with a
build is the one that governs it.

## 8. Other terms

- **Trademarks.** This notice grants no rights to the Caber name, logos, or other
  trademarks, other than to say truthfully that you are evaluating Caber.
- **Third-party software.** The Preview includes open-source and third-party components
  under their own licenses. See the third-party notices shipped with the build.
- **Governing law.** California law governs this notice, without regard to
  conflict-of-law rules. The copyright and DMCA provisions are matters of United States
  federal law.
- **Severability and waiver.** If any part of this notice is unenforceable, the rest
  still applies. Caber not enforcing a term is not a waiver of it.

## 9. Contact

Licensing questions, commercial pilots, or anything not covered here: support@caber.com.
