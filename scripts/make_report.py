"""
Generate bilingual Vi/En PDF method report.
Output: docs/report/method_report.pdf
Requires: pip install reportlab
"""
from __future__ import annotations
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def build_report(output_path: str = "docs/report/method_report.pdf"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story: list = []

    def h1(text: str) -> None:
        story.append(Paragraph(text, styles["Heading1"]))
        story.append(Spacer(1, 12))

    def h2(text: str) -> None:
        story.append(Paragraph(text, styles["Heading2"]))
        story.append(Spacer(1, 8))

    def p(text: str) -> None:
        story.append(Paragraph(text, styles["Normal"]))
        story.append(Spacer(1, 8))

    h1("Vietnamese MCQA System -- HackAIthon 2026 Bang C")
    h1("He thong Tra loi Trac nghiem Tieng Viet")

    h2("1. Problem / Bai toan")
    p(
        "EN: Build a Vietnamese MCQA system using small open-source LLMs "
        "(Qwen3.5 <=9B or Gemma-4). Input: CSV/JSON with qid, question, choices. "
        "Output: pred.csv with qid, answer (A-K)."
    )
    p(
        "VI: Xay dung he thong MCQA Tieng Viet dung LLM nho nguon mo. "
        "Dau vao: CSV/JSON. Dau ra: pred.csv voi cot qid, answer (A-K)."
    )

    h2("2. Core Approach / Phuong phap chinh")
    p(
        "EN: Constrained likelihood scoring. For each question, one forward pass "
        "through the LLM. Extract logits at the last token position for labels "
        "A, B, ..., K. Argmax = answer. No free-text generation => zero format "
        "errors, 1 token latency."
    )
    p(
        "VI: Tinh diem log-xac suat co rang buoc. Moi cau hoi chi can 1 forward "
        "pass. Lay logits vi tri cuoi cho nhan A..K. Argmax = dap an. Khong sinh "
        "van ban tu do."
    )

    h2("3. Architecture / Kien truc")
    p(
        "src/config.py -- Config dataclass, ENV overrides | "
        "src/io_utils.py -- auto-detect CSV/JSON, normalise choices | "
        "src/prompt.py -- Vi template, middle-truncation | "
        "src/backends/ -- StubBackend (test), HFBackend (CPU), VLLMBackend (GPU), "
        "UnsloBackend (Unsloth 4-bit) | "
        "src/scorer.py -- score_batch | src/run.py -- Docker entrypoint"
    )

    h2("4. Optimization / Toi uu")
    p(
        "EN: AWQ 4-bit quantization (vLLM) or BnB 4-bit (Unsloth), "
        "batch inference, middle-truncation for long passages "
        "(keep question stem at end), context budget 8000 chars."
    )
    p(
        "VI: Luong hoa AWQ 4-bit (vLLM) hoac BnB 4-bit (Unsloth), "
        "suy luan theo lo, cat doan giua van ban dai, ngan sach 8000 ky tu."
    )

    h2("5. Results / Ket qua")
    p("(Update after benchmarking -- to be filled in before submission)")

    doc.build(story)
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    build_report()
