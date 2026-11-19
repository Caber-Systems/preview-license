# Caber Community Preview Edition License

Version 1.2, November 12, 2026. This license applies to the Community Preview build it accompanies.

Copyright (c) 2026 Caber Systems, Inc. All rights reserved.

## At a glance

The Community Preview is free to try, whether you’re curious about what Caber can do or evaluating it for your team. Run it locally or in staging, build an internal proof of concept, use an AI coding assistant with the documented SDK and APIs, or publish your results. No separate acceptance step is required.

Run the Preview only on non-production infrastructure with non-production data. The Preview enforces limits on events, distinct customer objects, and concurrent SDK instances. When a limit is reached, your application can keep running without SDK interception or governance. Section 3 explains what happens at each limit and how to reset the Preview.

The sections below govern your use. For a commercial pilot or another use outside these terms, contact support@caber.com.

## 1. What you can do

Caber Systems, Inc. (Caber) grants you a free, non-exclusive, non-transferable, non-sublicensable license to install, run, test, and demonstrate the Community Preview Edition (the Preview) in environments you control for the purpose of evaluating Caber.

Evaluation includes personal exploration and learning as well as internal proofs of concept and purchase evaluations. You may run the Preview on your laptop or in a lab or staging environment and demonstrate it to your team, management, or at a meetup or conference. You may write or record your experience and publish benchmarks without prior approval. If you publish numbers, we welcome a heads-up so we can help check the configuration.

You may use an AI coding assistant to build or debug your own integration against the documented SDK and APIs, including by sharing Preview error messages, subject to the restrictions on internal materials in section 2.

Code you write against the documented SDK and APIs, data you provide, and events, graphs, policies, and reports the Preview generates from your data are yours. You may use those outputs for unrelated model training and fine-tuning under section 2.

## 2. Evaluation boundaries

These conditions define the scope of the license. Section 7 explains when the license ends.

- **Use only non-production infrastructure and data.** Do not install or run the Preview on production infrastructure or connect it to production systems. Do not process production data, including copies of production data, live traffic, or real customer data. Do not deploy the Preview commercially, offer it to others as a service, or embed it in a product.
- **Redistribution.** You may share Caber’s official download link. Do not redistribute, mirror, or repackage the Preview’s container images, wheels, or binaries.
- **Use the documented reset procedures.** Do not remove, alter, disable, or bypass the Preview limits or the license and integrity checks that enforce them. The resets in section 3 are permitted.
- **Protect proprietary internals.** Except to the limited extent applicable law expressly overrides this condition, do not decompile, disassemble, or otherwise reverse engineer the Preview or extract its embedded scripts, ontologies, or model artifacts. This includes submitting Preview binaries, compiled extensions, embedded assets, disassembly, memory dumps, or captures of its SDK protocol or tokens to a language model, coding agent, or other automated analysis system as prompts, context, or training data to analyze, reconstruct, reimplement, or describe its internals. Sections 1 and 4 describe permitted integration work and security testing.
- **Protect against replication.** Do not use the Preview or its embedded assets to train or fine-tune a model. Do not use the Preview, its embedded assets, or its outputs as source material to build a product or train a model to replicate Caber’s core runtime interception, governance, or provenance capabilities as a replacement for Caber. You may train or fine-tune models for other purposes on outputs generated from your data, provided those outputs do not include Caber’s embedded assets or proprietary internal materials. Ordinary integration development and benchmark publication remain permitted under section 1.
- **Preserve the notices.** Keep this license and Caber’s copyright notices intact.

## 3. Preview limits and resets

The Preview enforces these limits in code.

| Limit | Value | When reached |
| --- | --- | --- |
| Events | 20,000 | The Preview stops recording new events. The SDK stops intercepting and governing traffic. Your application keeps running, and the console remains available for data already collected. |
| Distinct customer objects | 500 | The Preview stops admitting new documents from your object sources. The SDK stops intercepting and governing traffic. |
| Concurrent SDK instances | 5 | The Preview refuses additional SDK instances. Their applications run without SDK interception or governance. |

The console warns at 80 percent. To start over:

- For a CaberDemos demo, run `demo.py down <demo>`, then `demo.py up <demo>`.
- For a stack you composed yourself, run `docker compose exec caber-core caber-core reset`, then `docker compose restart caber-core`.

After either reset, restart applications that load the SDK. Deleting documents does not lower the object count. See the [Preview limits reference](https://github.com/Caber-Systems/preview-license/blob/v1.2/PREVIEW_LIMITS.md).

Caber uses cryptographic controls to enforce access and integrity, including time-bound capability tokens and digests for embedded assets. Caber reserves its rights under applicable law, including 17 U.S.C. § 1201 where it applies. The license condition against bypassing the controls is in section 2.

## 4. Your data, privacy, and security testing

The Preview runs entirely in your environment. It does not send events, documents, telemetry, or usage data to Caber.

Caber authorizes good-faith vulnerability scanning of your own isolated, non-production Preview deployment and testing through documented interfaces within that deployment. Use only non-production systems and data you control or have permission to test, subject to section 2. This authorization does not extend to Caber-operated systems, other deployments, bypassing Preview controls, or extracting proprietary internals. Any rights available under applicable law remain available.

You may report suspected vulnerabilities privately to support@caber.com. Include the Preview build and enough detail to reproduce the issue. Keep customer data, credentials, and other confidential material out of the report.

## 5. Feedback

Feedback is welcome. If you send Caber bug reports, suggestions, or other feedback, you give Caber permission to use it for any purpose without obligation to you. Please keep confidential information out of feedback.

## 6. Preview readiness, warranty, and liability

The Preview is pre-release software for controlled evaluation on non-production infrastructure with non-production data. It can contain bugs and change or break between builds. It has not been security hardened and is unsuitable for regulated data. Keep it off untrusted networks. Interpret security findings in the context of the Preview build tested.

To the extent permitted by law, Caber has no obligation to provide support, maintenance, updates, patches, or fixes for the Preview, or to acknowledge, investigate, respond to, or remediate any reported bug or security issue.

TO THE EXTENT PERMITTED BY LAW, THE PREVIEW IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. CABER WILL NOT BE LIABLE FOR ANY DAMAGES ARISING FROM YOUR USE OF THE PREVIEW, INCLUDING DIRECT, INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES, EVEN IF ADVISED OF THEIR POSSIBILITY.

Where applicable law limits these exclusions, they apply to the fullest extent the law allows. To the extent permitted by law, Caber’s total liability is limited to the amount you paid for the Preview, which is zero.

## 7. When the license ends

The license ends automatically if you breach a condition in section 2.

When the license ends, stop using the Preview and delete your copies. Sections 4 through 8 survive, except that the security testing authorization in section 4 ends with the license.

Caber may discontinue the Preview program or publish a new build under different terms. The license shipped with your build continues to govern that build.

## 8. Other terms

- **Trademarks.** This license grants no rights to Caber’s name, logos, or other trademarks, except to state truthfully that you are evaluating Caber.
- **Third-party software.** Open-source and other third-party components are governed by their own licenses. See the third-party notices shipped with the build.
- **Governing law.** California law governs this license without regard to conflict-of-law rules. United States federal law governs federal copyright and DMCA matters.
- **Severability and waiver.** If any part of this license is unenforceable, the rest continues to apply. Caber’s failure to enforce a term does not waive it.

## 9. Contact

For licensing questions, commercial pilots, or other requests, contact support@caber.com.
