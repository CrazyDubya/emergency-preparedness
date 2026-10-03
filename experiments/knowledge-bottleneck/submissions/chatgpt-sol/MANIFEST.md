# Submission Manifest — ChatGPT / GPT-5.6 Sol

## Identity

- Participant: ChatGPT
- Model: GPT-5.6 Sol
- Date: 2026-09-14
- Repository: `CrazyDubya/emergency-preparedness`
- Experiment seed branch: `experiment/knowledge-bottleneck-seed`
- Experiment seed commit: `2d95e9546a7c6b61277bee766f5108b9f5767e8b`
- Submission branch: `experiment/kb-chatgpt-held`
- Artifact-freeze commit: `f49bb31a8d87ee3914eecde603b083788652f8bd`

## Frozen artifacts

| Artifact | Limit | Exact UTF-8 bytes | Utilization | Unused | Git blob SHA |
|---|---:|---:|---:|---:|---|
| `1k.txt` | 1,024 | 1,024 | 100.000% | 0 | `12f61f64917585f103700a5aad33893ce1be1361` |
| `100k.txt` | 102,400 | 102,384 | 99.984% | 16 | `45246be87bbe7c329415c37ce9e0b1436faf488e` |
| `1m.txt` | 1,048,576 | 1,043,112 | 99.479% | 5,464 | `8bec14acaec43908d669d77798d7cb2766ada6b5` |

The constrained artifacts were frozen before `COMMENTARY.md` and this manifest were written. They should not be changed during first-wave blind collection.

## Construction method

### `1k.txt`

Written directly as an independent 1 KiB optimization. No post-hoc source packing. It was intentionally driven to exactly 1,024 UTF-8 bytes.

### `100k.txt`

Written first as an independent synthesized operating manual, not as a summary of `1m.txt`. The synthesized version did not consume enough of the budget to create meaningful byte pressure. A deterministic source packer then let selected, lower-priority repository material compete for the remaining capacity. Paragraphs were normalized to portable ASCII, web URLs were removed, duplicate paragraphs were rejected, and only complete paragraphs fitting under the ceiling were retained.

### `1m.txt`

Written first as an independent synthesized field/recovery library, not as an expansion of `100k.txt`. After the human-facing synthesized/source corpus still left substantial capacity, additional readable repository source material was admitted by explicit category priority. Executable preparedness source code was permitted only as the last tier, after human-facing prose had already consumed most of the budget.

The packer is preserved at:

`experiments/knowledge-bottleneck/submissions/chatgpt-sol/build_artifacts.py`

The isolated workflow used only for this submission is:

`.github/workflows/kb-chatgpt-pack.yml`

The packer verifies each artifact remains valid UTF-8 and does not exceed its byte ceiling.

## Tools used

- GPT-5.6 Sol for selection, synthesis, prioritization and commentary.
- Connected GitHub tools to inspect the repository and write the isolated submission branch.
- GitHub Actions / Python 3.12 for deterministic normalization, paragraph deduplication, source packing and byte-count verification.
- No general web search was used to construct the artifacts.
- No other participant submission was inspected.

## Source discipline

The repository was treated as the primary source corpus, not as automatically authoritative. Where repository material appeared stale, overly precise, product-specific, or unsafe when detached from context, the synthesized operating layers generalized or corrected it. Packed source material is explicitly marked as a lower-level reference layer; current local/professional guidance and the conservative operating layer take precedence when conflicts arise.

## Blindness / independence declaration

I did **not** inspect, search, fetch, compare against, or infer from any other participant's knowledge-bottleneck artifacts, commentary, branch, or evaluation. I did not inspect the comparison branch. The only experiment-control material read was the canonical seed prompt/protocol/handoff material.

The three constrained artifacts were independently optimized by budget before comparison with other submissions.

## Submission status

**FROZEN — ready for first-wave comparison after the other blind submissions are collected.**