# Preserving Molecular Information During Pathology Report De-identification: A Synthetic Benchmark

**Background:** Pathology reports could support report standardization, summarization, hypothesis generation and testing, and research abstraction. De-identification must remove patient identifiers while preserving molecular findings needed for these uses.

**Design:** An institution-developed pipeline and context-aware rules were compared with five frontier LLM configurations (GPT-5.6 Sol through two interfaces, Claude Sonnet 5, Gemini 3.1 Pro, and Grok 4.6) on 200 unique synthetic report pairs. Success required preserving a molecular expression in one report and removing similarly formatted identifying digits in its paired control. A separate 200-pair experiment evaluated local refinement across eight report patterns. Paired analyses accounted for repeated patterns and multiple comparisons.

**Results:** The institution-developed pipeline preserved complete molecular expressions in 0/200 reports and exposed identifying digits in 11/200 controls. Context-aware rules preserved 159/200 expressions, exposed digits in 30/200 controls, and achieved both objectives in 133/200 pairs. LLM configurations preserved 200/200 expressions and achieved both objectives in 197–200/200 pairs, with 0–3/200 controls exposing digits (adjusted p=0.16 versus context-aware rules, accounting for report patterns). Local failures included molecular over-redaction and identifiers missed across line breaks, repeated footers, parenthetical fields, and modified labels. In the separate experiment, refinement reduced exposures from 100/200 to 50/200 while preserving all 200 molecular expressions; parenthetical-field and modified-label failures persisted.

**Conclusions:** Local refinement corrected specific failures but left identifier exposure. Frontier LLM configurations performed better descriptively. This synthetic benchmark evaluates identifier removal and molecular preservation, not genomic re-identification or clinical deployment safety.


## Completed matched comparison

| Approach | Digit exposures /200 | Molecular retained /200 | Both /200 |
|---|---:|---:|---:|
| Institution-developed redaction pipeline | 11 | 0 | 0 |
| Context-aware rules | 30 | 159 | 133 |
| GPT-5.6 Sol · enterprise | 2 | 200 | 198 |
| GPT-5.6 Sol · developer-tool | 0 | 200 | 200 |
| Claude Sonnet 5 | 3 | 200 | 197 |
| Gemini 3.1 Pro | 0 | 200 | 200 |
| Grok 4.6 | 1 | 200 | 199 |


## Design and interpretation

The main comparison contains **200 unique pairs, 400 unique reports per approach**. There are no duplicated cases or weighting to round the denominator. A pair comprises a clinical report containing a molecular expression and an identity control with a similarly formatted value designated as identifying. The selected 200 pairs were fixed by salted case-ID hash from 213 pairs with usable original outputs shared by both GPT access routes and Gemini. This is a comparison conditional on availability, not a prospectively sampled clinical cohort or first-attempt delivery estimate.

The institution-developed redaction pipeline is the bundled rule-based implementation used in this benchmark; the descriptor identifies its origin, not institutional endorsement or deployment validation.

Five configurations represent GPT through two access routes, Claude Sonnet, Gemini, and Grok. The GPT enterprise arm was collected through the ChatGPT Enterprise browser interface; the other arms used a developer-tool command-line runner. Model, access route, context, and batch-size effects are not separable in this design. The two GPT configurations are not independent model families. Exact runtime labels and prompts remain in the collection metadata.

Sonnet required supplemental collection for 104 target records and Grok for 167. The original task and source text were retained. Supplemental batches contained at most 16 records, then at most four for unresolved outputs, then three individual Grok requests. Only missing/non-aligned records were retried, with no case-specific feedback. Existing valid responses were retained regardless of privacy or utility performance. All original responses and unsuccessful attempts remain preserved. The last three fresh Grok responses aligned without manual correction; no normalization or response editing was needed. Whole-array extraction from permitted response envelopes did not change redaction strings. The earlier Enterprise batches contained 16 reports and original developer-tool batches contained 64 reports.

**Endpoints.** Exposure means any retained tested variable identifying digit in an identity control. Retention means exact preservation of the complete designated molecular expression in the clinical report. Joint success requires both outcomes within the same pair. These are narrow, explicitly annotated outcomes: they are not comprehensive privacy checks. Missing, malformed or non-aligned records were never treated as safe. After supplemental collection, all 400 selected records in each of the seven approaches were alignable; availability outside this selected set is retained in the historical evidence.

**Statistics.** Two-sided exact McNemar tests evaluate paired joint success. A sensitivity analysis swaps method outcomes at the level of the 16 report-pattern families, preserving within-family dependence. Holm adjustment is applied across six post hoc comparisons separately for each testing method. The pattern-block test assumes exchangeability and does not establish independent clinical sampling. Differences and counts are primary; no model equivalence or population-level effect is claimed. The separate local experiment now has 200 pairs across eight families. Its single exploratory refinement contrast is reported separately; the original 160-pair analysis and its eight-contrast adjustment family remain archived. Neither local cohort is pooled with the main comparison.

**Independent sources of evidence.** The expanded 200-pair local experiment comprises eight designed mechanisms with 25 pairs each. After the initial 160-pair analysis, five new variants per mechanism (40 pairs, 80 reports) were generated and evaluated with unchanged frozen methods. The original 960 outputs were retained; 240 new outputs were added. This post hoc size extension adds variants within existing patterns, not new independent pattern families. Methods were frozen before evaluation; this is not independent expert case validation. The 1,700 ordinary utility annotations cover diagnosis, specimen/linkage, result status and quantities and exclude the separately scored molecular coordinate expressions. The historical development and policy-sensitivity analyses use different cohorts and endpoints and are presented separately.

**Scope.** Task-policy rules were investigator approved. Report generation and analysis were AI-assisted, with no independent expert adjudication claimed. The benchmark measures de-identification behavior; it did not measure downstream research accuracy, clinical benefit, re-identification risk, or permission to send clinical data to a service. The local failures support limitations of the tested methods, not the impossibility of all local processing.


## Expanded local experiment: 200 unique pairs

The original 160 pairs were retained and 40 new pairs were added with frozen methods. All 1,200 outputs are aligned. Tested-digit exposures: institution-developed pipeline 0/200, context-aware rules 100/200, refined rules 50/200. Molecular expressions preserved: 0/200, 200/200 and 200/200; joint successes: 0/200, 100/200 and 150/200. All 1,700 ordinary utility facts were preserved. The sections below retain the earlier 160-pair results as history.

## Additional experimental findings

### Local development trajectory

Early context extensions recovered molecular content but increased identifying-digit exposure. Later context-aware rules improved both endpoints relative to that early extension, yet still left reproducible failures. The table below describes the original development/evaluation split, not the current 200-pair selected comparison.


| Stage | Development digit exposure | Development retention | Evaluation retention |
|---|---:|---:|---:|
| Institution-developed pipeline | 16/192 | 0/192 | 0/64 |
| Early context extension | 88/192 | 96/192 | 16/64 |
| Context-aware rules | 40/192 | 144/192 | 48/64 |


### Separate local experiment on 160 new pairs

The 320 frozen candidate documents were processed by the bundled Philter adapter with NLTK 3.9.2, then by unchanged frozen v5 and v6. All 960 outputs were valid aligned masks. Source inputs, candidate freeze, and method hashes remained unchanged. The candidate combines eight designed mechanisms; it is not an externally sourced or independently reviewed cohort.

| Method | Identity controls exposing tested digits | Clinical expressions preserved | Pairs meeting both narrow objectives |
|---|---:|---:|---:|
| Philter | 0/160 | 0/160 | 0/160 |
| v5 | 80/160 | 160/160 | 80/160 |
| v6 | 40/160 | 160/160 | 120/160 |

V5 exposures occurred in wrapped-adjacent-result, parenthetical-inline, separated-footer, and qualified-result mechanisms (20 each). V6 repaired the wrapped and footer mechanisms in this set but retained all 20 parenthetical-inline and all 20 qualified-result exposures. No method was changed after observing these results.

Broader identifying-value residuals occurred in 20/160 Philter controls, 80/160 v5 controls, and 40/160 v6 controls. These broader residuals are distinct from the tested variable digits.

All three methods retained the 1,360 separately annotated ordinary utility facts (diagnosis, specimen/linkage, result status, and quantity). This exact-text endpoint excludes the separately scored coordinate expression and does not measure semantic understanding. Its uniformly perfect result alongside Philter's 0/160 coordinate retention illustrates why generic utility measures can miss a critical molecular failure.

## Historical label/value policy sensitivity

The approved policy was implemented through explicit removal of generic labels and explanatory phrases from 256 historical coordinate-shaped identity annotations. All original spans and raw responses remain unchanged in their source locations. The revised annotation file and complete change ledger are saved separately. The same revised gold was applied to all five completed hosted arms and all five historical local comparators.

Among assessable hosted identity controls, designated-value residuals occurred in Enterprise Sol 6/256, Cursor Sol 0/256, Sonnet 0/196, Gemini 0/214, and Grok 0/161. Enterprise's six include the four previously reported tested-digit exposures and two controls retaining only the chromosome number `17`. Thus 6/256 broader value residuals must not replace or be conflated with the 4/256 narrow digit endpoint. No model's assessability or narrow endpoint changed.

These are automated, post hoc policy-sensitivity results following user approval of the task rules. They are not independent expert adjudication of each report.



## Muse collection snapshot

Muse returned 20 usable reports: 8 identifying-value controls and 12 clinical reports. Tested digits were exposed in 0/8 controls; molecular expressions were retained in 12/12 clinical reports. There were 0 complete matched pairs, so no paired success estimate is available. The next batch ended with resource_exhausted; remaining requests were held. This error does not identify the cause as account credits. Muse remains excluded from the main comparison.