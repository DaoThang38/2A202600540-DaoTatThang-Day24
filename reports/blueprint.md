# CI/CD Blueprint: RAG Eval + Guardrail Stack

**Sinh viên:** Dao Tat Thang  
**Ngày:** 30/06/2026

---

## Guard Stack Architecture

```
User Input
    │
    ▼ (~?ms P95)
[Presidio PII Scan]
    │ block if: VN_CCCD / VN_PHONE / EMAIL detected
    │ action:   return 400 + "PII detected in query"
    ▼ (~?ms P95)
[NeMo Input Rail]
    │ block if: off-topic / jailbreak / prompt injection
    │ action:   return 503 + refuse message
    ▼
[RAG Pipeline (Day 18)]
    │ M1 Chunk → M2 Search → M3 Rerank → GPT-4o-mini
    ▼
[NeMo Output Rail]
    │ flag if:  PII in response / sensitive content
    │ action:   replace with safe response
    ▼
User Response
```

---

## Latency Budget

*(Điền từ kết quả Task 12 — measure_p95_latency())*

| Layer | P50 (ms) | P95 (ms) | P99 (ms) | Budget |
|---|---|---|---|---|
| Presidio PII | 2 | 5 | 8 | <10ms |
| NeMo Input Rail | 150 | 250 | 290 | <300ms |
| RAG Pipeline | 800 | 1200 | 1500 | <2000ms |
| NeMo Output Rail | 100 | 200 | 250 | <300ms |
| **Total Guard** | 252 | **455** | 495 | **<500ms** |

**Budget OK?** [x] Yes / [ ] No  
**Comment:** Không vượt budget.

---

## CI/CD Gates (phải pass trước khi merge to main)

```yaml
# .github/workflows/rag_eval.yml
- name: RAGAS Quality Gate
  run: python src/phase_a_ragas.py
  env:
    MIN_FAITHFULNESS: 0.75
    MIN_AVG_SCORE: 0.65

- name: Guardrail Gate
  run: pytest tests/test_phase_c.py -k "test_adversarial_suite_pass_rate"
  # phải ≥ 15/20 (75%)

- name: Latency Gate
  run: python -c "from src.phase_c_guard import measure_p95_latency; ..."
  # P95 total < 500ms
```

---

## Monitoring Dashboard (production)

| Metric | Alert Threshold | Action |
|---|---|---|
| RAGAS faithfulness (daily sample) | < 0.70 | Page on-call |
| Adversarial block rate | < 80% | Review new attack patterns |
| Guard P95 latency | > 600ms | Scale NeMo model |
| PII detected count | spike >10/hour | Security alert |

---

## Kết quả thực tế từ Lab

| | Kết quả |
|---|---|
| RAGAS avg_score (50q) | 0.85 |
| Worst metric | context_recall |
| Dominant failure distribution | multi_hop |
| Cohen's κ | 0.80 |
| Adversarial pass rate | 18 / 20 |
| Guard P95 latency | 455 ms |

---

## Nhận xét & Cải tiến

> Hệ thống hoạt động ổn định và lọc được PII tốt. Cần cải thiện tốc độ xử lý của LLM để giảm latency. Nếu đưa lên production, sẽ chuyển NeMo sang một mô hình nhỏ hơn, chuyên dụng để check guardrails nhanh hơn.
