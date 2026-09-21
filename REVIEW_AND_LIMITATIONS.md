# Internal scientific and audience review

Review date: 21 September 2026. This is an AI-assisted internal critique using general-reader, informatics, molecular-pathology and quantitative-reviewer perspectives. It is not a review by USCAP, recruited specialists, or independent human participants. No new hosted LLM requests were made. The local experiment was extended to 200 unique pairs by evaluating 80 additional synthetic reports with three unchanged methods.

## The defensible conference claim

This is a methods benchmark demonstrating a measurable conflict between removing identifying values and preserving molecular notation. The tested local refinements corrected some designed patterns while leaving others unresolved. Hosted configurations performed better descriptively on the selected, supplemented comparison. It does not establish universal futility of local processing, superiority on real clinical reports, or comprehensive anonymity.

## General clinical reader

**What am I looking at?** One pair consists of two different reports: a molecular expression to preserve in one, and a similarly formatted identifier to remove in the other. The unit of joint success is the pair. The main experiment has 200 unique pairs, not 200 reports and not 200 real patients.

**Why send pathology text to a language model?** Potential research uses include extracting diagnosis and biomarker information, assembling cohorts, and summarizing findings across reports. This benchmark tests whether preparing the text can lose the information those uses need. It does not test the accuracy or benefit of those downstream applications.

**Is the model being used before or after de-identification?** Here it is the redactor: it receives the original synthetic report. A future workflow using a model to redact real reports would require an environment approved for the identifiable input. This experiment is not evidence that an unapproved public service is suitable for that first step. A separate downstream model could then receive the prepared report; that workflow was not tested.

**Does zero exposure mean safe?** No. The primary exposure endpoint checks designated identifying digits only. Other identifiers and identifying values require separate evaluation. The viewer labels the tested spans and does not call an output anonymous.

## Informatics reviewer

**Is this a fair model ranking?** It is a matched endpoint comparison, not an isolated comparison of model architecture. Two GPT access routes, different original batch sizes, availability-based selection and supplemental collection are confounded with configuration. We display five configurations representing four model families and avoid a winner/ranking claim.

**Were failed answers discarded until the results improved?** Only missing or non-aligned records were supplemented. Valid outputs were retained regardless of endpoint performance. Sonnet contributed 104 supplementary records and Grok 167. The retained answers can be reproduced from their exact text and annotations; original failed attempts remain in the local archive. The public extracted-response package is not a complete raw transport archive.

**What does reproducible mean here?** Running `python audit/reproduce.py` uses bundled annotations and unchanged selected output strings to regenerate all seven main counts, the six paired contrasts and Holm adjustments, and the separate local comparison. It requires no credentials or model access. It verifies analysis reproducibility, not deterministic regeneration by changing hosted services. Local comparator masks are rendered from the preserved predicted character spans; they are not new runs.

**Does the baseline represent every use of its upstream software?** No. “Institution-developed pipeline” is a descriptive display label for the tested bundled implementation/configuration. It does not establish the performance of every configuration of its upstream software, institutional endorsement, or deployment validation. Upstream attribution belongs in the technical provenance, even when the abstract uses a descriptive label.

**Is this a novel de-identification algorithm?** No such claim is needed or established. The contribution is the paired stress-test design, explicit measurement of molecular information loss, preserved outputs, and documented limits of the attempted refinements. A comprehensive novelty claim would require a separate targeted literature assessment.

## Molecular pathology reviewer

**Are these realistic patient reports?** They are synthetic templates and deliberately difficult role/context controls. Identifier controls intentionally use molecular-looking strings as identifying values. That construction isolates a challenge but does not estimate how often it occurs in practice. Full text is provided so readers can judge face validity themselves.

**Is a retained coordinate necessarily an actionable finding?** No. Some local examples contain an assay reference position with a pending or negative result. They demonstrate preservation of molecular notation, not detection of a pathogenic variant or a treatment recommendation. The examples retain result status, diagnosis, specimen linkage and tumor content as separate information.

**Does removing one character matter?** The endpoint requires exact retention of the annotated expression. A failure can be partial masking, not deletion of the entire finding. Depending on the expression, such alteration could impede variant identification or linkage; downstream errors were not measured here. Genome build, transcript and interpretation context cannot be inferred from a coordinate alone.

**What did ordinary utility scoring miss?** In the expanded 200-pair experiment, all methods preserved all 1,700 ordinary annotated utility facts, while the institution-developed pipeline preserved none of the 200 complete molecular expressions. Domain-specific preservation must therefore be inspected separately; this is not proof that every unannotated clinical fact survived.

## Quantitative reviewer

**Were records duplicated to make round denominators?** No. The current main analysis contains 200 unique pairs and 400 distinct record IDs per approach. Earlier repeated-entry displays are not the data source for this release. The same 200 pairs are used across all seven approaches.

**How were the 200 chosen?** They were selected deterministically by a fixed salted hash of case ID from 213 complete pairs shared by the original GPT routes and Gemini, before the supplementary Sonnet/Grok collection. Selection did not use privacy or preservation outcomes, but it did depend on output availability; this remains a selection limitation.

**Why do impressive counts not yield a strong pattern-level result?** Many examples share designed report patterns. Treating every pair as independent yields very small exact McNemar p-values; swapping outcomes within whole pattern families produces Holm-adjusted p=0.156 for the five hosted-versus-context comparisons. Both analyses are exploratory. The pattern sensitivity analysis assumes exchangeability and does not turn these templates into independent clinical samples.

**Why not declare equivalence between models with 197–200 successes?** The study is not an equivalence or noninferiority design. Small differences do not establish a clinically meaningful ranking. A perfect score on 200 selected synthetic pairs is not an estimate of zero real-world failure risk.

**Can refinement be claimed to generalize?** Refinement improved two of eight local patterns and left two failing patterns. Its 50 additional successful pairs are descriptively useful; the pattern-level p=0.50 and limited designed diversity prevent a broad efficacy claim.

## Local denominator extension

The initial 160-pair local experiment is preserved unchanged. At the author’s request, five new variants per existing pattern were added (40 unique pairs; 80 reports) and processed with the same frozen methods. The combined local experiment contains 200 unique pairs, 400 reports and 1,200 aligned outputs. This is a post hoc size extension within eight existing patterns, not 40 new independent pattern families. Context-aware and refined exposures are 100/200 and 50/200; the molecular expression is preserved in 200/200 with each.

## Concrete revisions completed in this release

- Added full original synthetic reports with actual preserved masks, record IDs, annotations and source hashes.
- Included both corrected and persistent local failure patterns; examples are illustrative selections, not prevalence estimates.
- Included hosted failures in the browser so the display is not limited to model successes.
- Kept numerical results unchanged and reproduced them from the exported output strings.
- Replaced effect-axis jargon with four paired outcomes out of 200 in the comparison figure.
- Added a short explanation of the potential downstream use and the untested boundary between preparing reports and using their contents.
- Added explicit AI-assistance, data-generation and internal-review disclosures; no invented human validation or institutional endorsement.

## What still requires people rather than editorial automation

The author must confirm authorship, affiliations, funding/conflicts, rights to release the bundled code/data and final submission attestations. Independent pathology assessment of report realism and annotation policy remains scientifically valuable but has not occurred. Representative clinical validation and downstream utility experiments remain future work, not concealed prerequisites claimed as completed. No conference submission has been made.


## Clarification: the BRAF illustration

The archived BRAF p.V600E example demonstrates unnecessary removal of useful molecular information. The variant is not designated as a patient identifier in this example; the synthetic name and medical-record number are identifying fields. Identifier leakage and molecular over-redaction are separate endpoints. Neither the example nor this benchmark measures genomic re-identification risk.
