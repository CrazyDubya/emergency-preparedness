# V1 vs V2 Document Comparison (Pre–V3 Refactor)

**Purpose:** Record which docs were identical, which differed, and how they were combined into V3.

## Summary

| Document | V1 (disaster/) | V2 (claude-disaster/) | Result for V3 |
|----------|----------------|------------------------|---------------|
| README.md | Same | Same | Single copy; V3 README merged with README_ENHANCED content |
| CONTRIBUTING.md | Same | Same | Single copy in docs/ |
| VERSION_1_RELEASE.md | Same | Same | Single copy in docs/ |
| VERSION_2_ARCHITECTURE.md | Same | Same | Single copy in docs/ |
| stress_test_analysis.md | Same | Same | Single copy in docs/ |
| scenario_planning_top10.md | Same | Same | Single copy in docs/ |
| scenario_based_planning.md | Same | Same | Single copy in docs/ |
| family_preparedness_checklist.md | Same | Same | Single copy in docs/ |
| disaster_kit_research.md | Same | Same | Single copy in docs/ |
| disaster_analysis_report.md | Same | Same | Single copy in docs/ |
| deep_dive_health_risks.md | Same | Same | Single copy in docs/ |
| README_ENHANCED.md | — | V2 only | Content merged into main V3 README (CLI, API, GUI, backup, profiles) |

**Conclusion:** V1 and V2 documentation were **identical** for all shared files. No conflicting edits. V2 added README_ENHANCED (v3.0 features). V3 keeps one set of docs and combines README + README_ENHANCED into a single README.

## Knowledge Base Comparison

| Location | V1 | V2 | V3 |
|----------|----|----|-----|
| Base KB (water, medicine, security, etc.) | disaster_knowledge_base/ | disaster_knowledge_base/ (same content) | knowledge_base/ (merged) |
| winter_storm_preparedness.md | ✓ (root of KB) | Missing | ✓ Added from V1 |
| home_repair/frozen_pipes_guide.pdf | ✓ | Missing | ✓ Added from V1 |
| modern_threats/ (cyber, EMP, nuclear) | — | v2_knowledge_base/ | ✓ Under knowledge_base/ |
| long_term_sustainability/ | — | v2_knowledge_base/ | ✓ Under knowledge_base/ |

V3 uses a **single `knowledge_base/`** directory containing all guides (traditional + modern threats + long-term sustainability) plus the two V1-only assets.

**Detailed KB comparison and refactor review:** See **`docs/KNOWLEDGE_BASE_REVIEW.md`** for file-by-file inventory (disaster vs claude-disaster), same/different/combine verdict, what V3 did, and recommendations for future improvements.
