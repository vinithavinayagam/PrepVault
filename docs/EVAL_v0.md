# PrepVault - Week 3 Evaluation (v0)

**Evaluation date:** 2026-11-04

## Summary

| Metric | Result |
|---|---:|
| Questions tested | 10 |
| Passed | 6 |
| Partial | 2 |
| Failed | 0 |
| Correct abstentions | 2 |

## Question Results

### Q1 - Data structure, interface and representation

- **Tenant:** `demo_college`
- **Question:** What is a data structure, and what is the difference between an interface and a representation?
- **Expected source:** MIT DSA Lecture 2
- **Result:** PASS
- **HTTP status:** 200
- **Answer correctness:** Correct
- **Citation:** Page 1
- **Notes:** Correctly defines a data structure and explains interface versus representation.

### Q2 - Linked list structure

- **Tenant:** `demo_college`
- **Question:** How does a linked list store elements, and how are its nodes connected?
- **Expected source:** MIT DSA Lecture 2
- **Result:** PASS
- **HTTP status:** 200
- **Answer correctness:** Correct
- **Citation:** Page 3
- **Notes:** Explains that each node contains `node.item` and `node.next`, and that the next pointer connects nodes.

### Q3 - Amortized analysis

- **Tenant:** `demo_college`
- **Question:** How does amortized analysis work, and why is dynamic-array insertion amortized O(1)?
- **Expected source:** MIT DSA Lecture 2
- **Result:** PASS
- **HTTP status:** 200
- **Answer correctness:** Correct
- **Citations:** Pages 3 and 4
- **Multi-page retrieval:** PASS
- **Notes:** Explains amortized cost, extra capacity, infrequent resizing, and amortized O(1) insertion.

### Q4 - Stack principle

- **Tenant:** `psvpec`
- **Question:** What is a stack, and which principle does it follow?
- **Expected source:** College-specific materials
- **Result:** CORRECT ABSTENTION
- **HTTP status:** 200
- **Answer correctness:** Safe abstention
- **Notes:** The API could not find the answer. The tenant-scoped keyword check found no matching stack or LIFO chunks for `psvpec`. This test also checks tenant isolation.

### Q5 - Linked list structure

- **Tenant:** `psvpec`
- **Question:** What is a linked list, and how are its nodes connected?
- **Expected source:** College-specific materials
- **Result:** CORRECT ABSTENTION
- **HTTP status:** 200
- **Answer correctness:** Safe abstention
- **Notes:** The API could not find the answer. The tenant-scoped keyword check found no matching linked-list or node.next chunks for `psvpec`. Similar material exists in `demo_college`, but must not be exposed to another tenant.

### Q6 - Get and set operations

- **Tenant:** `demo_college`
- **Question:** What are the get and set operations in a data structure?
- **Expected source:** MIT DSA Lecture 2
- **Result:** PASS
- **HTTP status:** 200
- **Answer correctness:** Correct
- **Citation:** Page 1
- **Notes:** Correctly explains that get returns the item at an index and set replaces the item at an index.

### Q7 - Sequence operations

- **Tenant:** `demo_college`
- **Question:** What operations does a sequence data structure support?
- **Expected source:** MIT DSA Lecture 2
- **Result:** PASS
- **HTTP status:** 200
- **Answer correctness:** Correct
- **Citation:** Page 1
- **Notes:** Correctly covers container, static, and dynamic operations, including build, len, get, set, insert, and delete.

### Q8 - Static array versus dynamic array

- **Tenant:** `demo_college`
- **Question:** What is the difference between a static array and a dynamic array?
- **Expected source:** MIT DSA Lecture 2
- **Result:** PARTIAL
- **HTTP status:** 200
- **Answer correctness:** Partially correct
- **Citations:** Pages 2, 3, and 4
- **Notes:** Correctly explains extra capacity and amortized append performance. However, it incorrectly states that set_at(i, x) takes O(n). Setting an element at a known index takes O(1) for both static and dynamic arrays.

### Q9 - Insertion at the beginning

- **Tenant:** `demo_college`
- **Question:** Why does inserting an element at the beginning of an array take O(n) time?
- **Expected source:** MIT DSA Lecture 2
- **Result:** PARTIAL
- **HTTP status:** 200
- **Answer correctness:** Incomplete
- **Retrieved citations:** Pages 2, 3, and 4
- **Notes:** The API abstained even though it retrieved potentially relevant pages. Investigate retrieval quality and answer generation. Verify that the source explains the shifting of existing elements before deciding whether the answer should pass.

### Q10 - Amortized append

- **Tenant:** `demo_college`
- **Question:** What is amortized time complexity, and why is appending to a dynamic array amortized O(1)?
- **Expected source:** MIT DSA Lecture 2
- **Result:** PASS
- **HTTP status:** 200
- **Answer correctness:** Correct
- **Citations:** Pages 3 and 4
- **Multi-page retrieval:** PASS
- **Notes:** Correctly explains the cost of resizing, extra capacity, and why append is amortized O(1).

## Evaluation criteria

- **Correctness:** Does the answer accurately address the question?
- **Citation relevance:** Do the cited PDF pages support the answer?
- **Multi-page coverage:** Does the answer use multiple relevant pages when needed?
- **Tenant isolation:** Does each college retrieve only its own material?
- **Abstention:** Does the system avoid inventing information not present in the dataset?

**Note:** HTTP success alone does not count as an evaluation pass. Q3 and Q10 test closely related concepts and should not be treated as fully independent coverage.
