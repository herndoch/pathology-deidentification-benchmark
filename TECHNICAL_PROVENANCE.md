# Technical provenance

## Baseline attribution

The figure label **institution-developed pipeline** refers to the bundled Philter implementation used by this project, with the project's frozen adapter/configuration. It is not an institution-wide validation or a claim that this study invented the upstream system.

Upstream citation: Norgeot B, Muenzen K, Peterson TA, et al. *Protected Health Information filter (Philter): accurately and securely de-identifying free-text clinical notes.* npj Digital Medicine. 2020;3:57. [doi:10.1038/s41746-020-0258-y](https://doi.org/10.1038/s41746-020-0258-y). The upstream source is under the BSD 3-Clause license. The abstract uses a descriptive label; this supplement retains attribution. The upstream paper's clinical-note findings and this synthetic molecular stress test are different evaluations.

This release includes frozen selected masks and their annotations; it does not redistribute the full upstream installation or claim that the output audit re-executes that installation. The local source archive retains the adapter, method code, dependencies and freezes. The public `methods/` directory contains the project's text-rule implementations for inspection and the adapter source; it is an archival source snapshot, not a turnkey installation.

## Collection labels

| Display | Recorded runtime selection | Route / original batch size |
|---|---|---|
| GPT: enterprise interface | GPT-5.6 Sol, Extra High | ChatGPT Enterprise browser; 16 reports |
| GPT: developer-tool access | `gpt-5.6-sol-xhigh` | Developer-tool runner; 64 reports |
| Claude Sonnet | `claude-sonnet-5-thinking-xhigh` | Developer-tool runner; 64 reports |
| Gemini | `gemini-3.1-pro` | Developer-tool runner; 64 reports |
| Grok | `cursor-grok-4.6-xhigh` | Developer-tool runner; 64 reports |

These are recorded interface/runtime labels, not independently attested provider model-weight identifiers. The non-Enterprise runner was Cursor. Access route and model effects are not separable. A UI label is not evidence of a direct private provider API or a pinned model snapshot.

Supplemental collection retained the original task prompt and source report text. Sonnet supplied 104 supplemental selected records and Grok 167, using smaller batches for unresolved delivery/alignment failures. Valid endpoint failures were retained. The three final Grok requests were individual reports and returned alignable masks without manual editing.

## File and record provenance

`data/provenance.json` maps each selected main output to its original or supplemental response label and source-file SHA-256. Source labels are relative identifiers, not live chat URLs or local user paths. Hosted masks retain their exact extracted strings. For local comparators, asterisks are rendered from the saved predicted spans against the original text, preserving line endings.

`data/main/gold.json` contains the 400 selected reports and annotations. `data/local/gold.json` contains the 400 separate local reports and annotations, with the original evaluation batch labels and new extension labels. The original 160 pairs were retained and 40 new pairs added using the frozen generator and methods. `data/local/extension_freeze.json` records the extension; `data/local/statistics.json` records its exploratory refinement contrast. Exact character spans distinguish tested identifying digits from molecular expressions. Gold annotations and report generation were AI-assisted; their independent human validation is not claimed.

The scorer file is copied byte-for-byte from the frozen project scorer. The separate `audit/reproduce.py` script recomputes outcomes and paired tests and verifies the release manifest. It does not read private source folders or call any online service.

## Scope of sharing

This is a synthetic research artifact. No clinical exports, credentials, passwords, user-account paths, browser conversation URLs, assistant transport logs or private handoffs are included. The complete original collection archive, including failed attempts, remains local. The release therefore supports selected-output and statistical auditing, not a complete public audit of every orchestration event.

No reuse license for the project's original materials is asserted here pending author review; upstream software rights remain with their owners. Attribution and human responsibility are preserved. A software DOI, formal repository release, author list and ORCIDs have not been invented.
