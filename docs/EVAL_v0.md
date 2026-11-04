# PrepVault — Week 3 Evaluation (v0)

**Evaluation date:** 2026-11-03

## Summary

| Metric | Result |
|---|---:|
| Questions tested | 1 |
| Passed | 1 |
| Partial | 0 |
| Failed / Abstained | 0 |

## Question Results

### Q1 — Data structure, interface and representation

- **Tenant:** `demo_college`
- **Question:** What is a data structure, and what is the difference between an interface and a representation?
- **Expected source:** MIT DSA Lecture 2
- **Result:** PASS
- **HTTP status:** success
- **Answer correctness:** Correct
- **Citation:** MIT DSA Lecture 2, page 1
- **Notes:** Correctly defines a data structure, explains that an interface specifies what operations are supported, and that a representation explains how those operations are supported.

## Evaluation criteria

- Correctness: Does the answer accurately address the question?
- Citation relevance: Do the cited PDF pages support the answer?
- Multi-page coverage: Does the answer use multiple relevant pages when needed?
- Abstention: Does the system avoid inventing information not present in the dataset?

**Note:** HTTP success alone does not count as an evaluation pass.

### Q2 — Linked list structure

- **Tenant:** `demo_college`
- **Question:** How does a linked list store elements, and how are its nodes connected?
- **Expected source:** MIT DSA Lecture 2
- **Result:** PASS
- **HTTP status:** success
- **Answer correctness:** Correct
- **Citation:** MIT DSA Lecture 2, page 3
- **Notes:** Correctly explains that each item is stored in a node containing `node.item` and `node.next`. The next pointer connects nodes in sequence.

### Q3 — Amortized Analysis

- **Tenant:** `demo_college`
- **Question:** How does amortized analysis work, and why is dynamic-array insertion amortized O(1)?
- **Expected source:** MIT DSA Lecture 2
- **Result:** PASS
- **HTTP status:** success
- **Answer correctness:** Correct
- **Citations:** MIT DSA Lecture 2, pages 3 and 4
- **Multi-page retrieval:** PASS
- **Notes:** Explains amortized cost, extra capacity in dynamic arrays, infrequent resizing, and O(1) amortized insertion.