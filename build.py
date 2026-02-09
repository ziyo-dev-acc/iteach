import os, json, re
from pathlib import Path

import requests
import pydyf
from weasyprint import HTML

PROVIDER = os.getenv("PROVIDER", "openai").lower()

SUBJECTS_FILE = "subjects.txt"
BOOK_HTML = "book.html"
BOOK_PDF = "Destination C1 and C2 @destination_b1_b2_c1.pdf"

# -------------------- LLM --------------------

def call_github_models(prompt: str) -> str:
    key = os.getenv("GITHUB_TOKEN")
    if not key:
        raise SystemExit("Set GITHUB_TOKEN")

    url = "https://models.inference.ai.azure.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4.1",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    r = requests.post(url, headers=headers, json=payload, timeout=180)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def llm(prompt: str) -> str:
    return call_github_models(prompt)


def strip_code_fences(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\n?", "", s)
        s = re.sub(r"\n?```$", "", s)
    return s.strip()


def strip_trailing_commas(s: str) -> str:
    # Remove trailing commas before ] or } to tolerate minor JSON issues.
    return re.sub(r",\s*([\]\}])", r"\1", s)


def load(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def save(path: str, content: str):
    Path(path).write_text(content, encoding="utf-8")


def fill(template: str, mapping: dict) -> str:
    out = template
    for k, v in mapping.items():
        out = out.replace("{{" + k + "}}", v)
    return out


def html_li(items):
    return "\n".join(f"<li>{x}</li>" for x in items)


def html_tr(rows):
    out = []
    for r in rows:
        tds = "".join(f"<td>{c}</td>" for c in r)
        out.append(f"<tr>{tds}</tr>")
    return "\n".join(out)


# -------------------- Templates --------------------

def build_grammar_unit(data: dict) -> str:
    tpl = load("grammar_unit.html")
    m = {
        "unit_number": str(data["unit_number"]),
        "unit_title": data["unit_title"],
        "level": data["level"],
        "heading1": data["heading1"],
        "table1_header_1": data["table1_header_1"],
        "table1_header_2": data["table1_header_2"],
        "table1_rows": html_tr(data["table1_rows"]),
        "note1": data["note1"],
        "heading2": data["heading2"],
        "para2": data["para2"],
        "list2_items": html_li(data["list2_items"]),
        "box1": data["box1"],

        "heading3": data["heading3"],
        "table2_header_1": data["table2_header_1"],
        "table2_header_2": data["table2_header_2"],
        "table2_rows": html_tr(data["table2_rows"]),
        "note2": data["note2"],
        "heading4": data["heading4"],
        "para4": data["para4"],
        "list4_items": html_li(data["list4_items"]),
        "box2": data["box2"],

        "taskA_title": data["taskA_title"],
        "taskA_items": html_li(data["taskA_items"]),
        "taskA_mark_note": data["taskA_mark_note"],
        "taskB_title": data["taskB_title"],
        "taskB_items": html_li(data["taskB_items"]),
        "taskB_mark_note": data["taskB_mark_note"],
        "taskC_title": data["taskC_title"],
        "taskC_items": html_li(data["taskC_items"]),
        "taskC_mark_note": data["taskC_mark_note"],

        "taskD_title": data["taskD_title"],
        "taskD_items": html_li(data["taskD_items"]),
        "taskD_mark_note": data["taskD_mark_note"],
        "taskE_title": data["taskE_title"],
        "taskE_items": html_li(data["taskE_items"]),
        "taskE_mark_note": data["taskE_mark_note"],
        "taskF_title": data["taskF_title"],
        "taskF_items": html_li(data["taskF_items"]),
        "taskF_mark_note": data["taskF_mark_note"],

        "total_mark": str(data["total_mark"]),
        "max_mark": str(data["max_mark"]),
    }
    return fill(tpl, m)


def build_vocab_unit(data: dict) -> str:
    tpl = load("vocab_unit.html")
    m = {
        "unit_number": str(data["unit_number"]),
        "unit_title": data["unit_title"],
        "level": data["level"],

        "topic1_title": data["topic1_title"],
        "topic1_rows": html_tr(data["topic1_rows"]),
        "topic2_title": data["topic2_title"],
        "topic2_rows": html_tr(data["topic2_rows"]),
        "verbs_heading": data["verbs_heading"],
        "verbs_rows": html_tr(data["verbs_rows"]),
        "vocab_box": data["vocab_box"],

        "taskA_title": data["taskA_title"],
        "taskA_wordbox": data["taskA_wordbox"],
        "taskA_items": html_li(data["taskA_items"]),
        "taskA_mark_note": data["taskA_mark_note"],
        "taskB_title": data["taskB_title"],
        "taskB_wordbox": data["taskB_wordbox"],
        "taskB_items": html_li(data["taskB_items"]),
        "taskB_mark_note": data["taskB_mark_note"],
        "taskC_title": data["taskC_title"],
        "taskC_items": html_li(data["taskC_items"]),
        "taskC_mark_note": data["taskC_mark_note"],

        "taskD_title": data["taskD_title"],
        "taskD_items": html_li(data["taskD_items"]),
        "taskD_mark_note": data["taskD_mark_note"],
        "taskE_title": data["taskE_title"],
        "taskE_items": html_li(data["taskE_items"]),
        "taskE_mark_note": data["taskE_mark_note"],
        "taskF_title": data["taskF_title"],
        "taskF_items": html_li(data["taskF_items"]),
        "taskF_mark_note": data["taskF_mark_note"],

        "total_mark": str(data["total_mark"]),
        "max_mark": str(data["max_mark"]),
    }
    return fill(tpl, m)


def build_mini_review(data: dict) -> str:
    tpl = load("review_1page.html")
    m = {
        "review_number": str(data["review_number"]),
        "unit_range": data["unit_range"],
        "sectionA_title": data["sectionA_title"],
        "sectionA_items": html_li(data["sectionA_items"]),
        "sectionB_title": data["sectionB_title"],
        "sectionB_items": html_li(data["sectionB_items"]),
        "sectionC_title": data["sectionC_title"],
        "sectionC_items": html_li(data["sectionC_items"]),
        "sectionD_title": data["sectionD_title"],
        "sectionD_items": html_li(data["sectionD_items"]),
        "sectionE_title": data["sectionE_title"],
        "sectionE_items": html_li(data["sectionE_items"]),
        "total_mark": str(data["total_mark"]),
    }
    return fill(tpl, m)


def build_big_review(data: dict) -> str:
    tpl = load("final_review_3page.html")
    m = {
        "unit_range": data["unit_range"],
        "final_p1_items": html_li(data["final_p1_items"]),
        "final_p2_items": html_li(data["final_p2_items"]),
        "final_p3_items": html_li(data["final_p3_items"]),
        "total_mark": str(data["total_mark"]),
    }
    return fill(tpl, m)


# -------------------- PDF compatibility --------------------

def ensure_pydyf_transform():
    if hasattr(pydyf.Stream, "transform"):
        return

    def _transform(self, a=1, b=0, c=0, d=1, e=0, f=0):
        # pydyf < 0.13 lacks Stream.transform; use the cm operator via set_matrix.
        self.set_matrix(a, b, c, d, e, f)

    pydyf.Stream.transform = _transform


def ensure_pydyf_text_matrix():
    if hasattr(pydyf.Stream, "text_matrix"):
        return

    def _text_matrix(self, a=1, b=0, c=0, d=1, e=0, f=0):
        # Map WeasyPrint's expected text_matrix to pydyf's set_text_matrix.
        self.set_text_matrix(a, b, c, d, e, f)

    pydyf.Stream.text_matrix = _text_matrix


# -------------------- Subjects --------------------

def parse_subjects(path: str):
    p = Path(path)
    if not p.exists():
        raise SystemExit(
            "subjects.txt not found. Expected format per line:\n"
            "level | unit_title | grammar_focus | vocab_topics (comma separated)"
        )
    lines = p.read_text(encoding="utf-8").splitlines()
    subjects = []
    for i, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [x.strip() for x in line.split("|")]
        if len(parts) < 4:
            raise SystemExit(f"Bad line {i}: expected 4 fields separated by |")
        level, unit_title, grammar_focus, vocab_topics = parts[:4]
        topics = [t.strip() for t in vocab_topics.split(",") if t.strip()]
        subjects.append({
            "level": level,
            "unit_title": unit_title,
            "grammar_focus": grammar_focus,
            "vocab_topics": topics,
        })
    if not subjects:
        raise SystemExit("subjects.txt has no valid lines")
    return subjects


# -------------------- Prompts --------------------

def level_sentence_rule(level: str) -> str:
    level = level.upper()
    if level == "A1":
        return "Max 10 words per sentence."
    if level == "A2":
        return "Max 12 words per sentence."
    if level == "B1":
        return "Max 14 words per sentence."
    if level == "B2":
        return "Max 16 words per sentence."
    if level == "C1":
        return "Max 18 words per sentence."
    if level == "C2":
        return "Max 20 words per sentence."
    return "Keep sentences concise and level-appropriate."


def grammar_prompt(unit, unit_number: int):
    level = unit["level"]
    vocab_topics = ", ".join(unit["vocab_topics"])
    rule = level_sentence_rule(level)

    return f"""
You are a senior German teacher and book writer (18+ years experience).
Create content STRICTLY for level {level}.
{rule}
Adult-neutral tone. No childish tone.
No grammar above the level.
Follow Destination-style logic: clear rules, controlled practice, and a professional workbook style.

UNIT META:
level: "{level}"
unit_number: {unit_number}
unit_title: "{unit['unit_title']}"
grammar_focus: "{unit['grammar_focus']}"
vocab_context: "{vocab_topics}"

OUTPUT FORMAT:
Return ONLY valid JSON. No comments. No markdown.

TASK:
Generate data for ONE Grammar Unit.
- Page 1: explanation + short examples.
- Pages 2-3: 90-120 total exercise items across A-F.

JSON SCHEMA (fill all fields):
{json.dumps({
  "level": level,
  "unit_number": unit_number,
  "unit_title": unit["unit_title"],
  "heading1": "",
  "table1_header_1": "",
  "table1_header_2": "",
  "table1_rows": [["", ""], ["", ""], ["", ""]],
  "note1": "",
  "heading2": "",
  "para2": "",
  "list2_items": ["", "", ""],
  "box1": "",
  "heading3": "",
  "table2_header_1": "",
  "table2_header_2": "",
  "table2_rows": [["", ""], ["", ""], ["", ""]],
  "note2": "",
  "heading4": "",
  "para4": "",
  "list4_items": ["", "", ""],
  "box2": "",
  "taskA_title": "",
  "taskA_items": ["" for _ in range(15)],
  "taskA_mark_note": "1 Punkt pro Satz",
  "taskB_title": "",
  "taskB_items": ["" for _ in range(15)],
  "taskB_mark_note": "1 Punkt pro Satz",
  "taskC_title": "",
  "taskC_items": ["" for _ in range(15)],
  "taskC_mark_note": "1 Punkt pro Satz",
  "taskD_title": "",
  "taskD_items": ["" for _ in range(15)],
  "taskD_mark_note": "1 Punkt pro Satz",
  "taskE_title": "",
  "taskE_items": ["" for _ in range(15)],
  "taskE_mark_note": "1 Punkt pro Satz",
  "taskF_title": "",
  "taskF_items": ["" for _ in range(15)],
  "taskF_mark_note": "1 Punkt pro Satz",
  "total_mark": 90,
  "max_mark": 90
}, ensure_ascii=False, indent=2)}
""".strip()


def vocab_prompt(unit, unit_number: int):
    level = unit["level"]
    topics = unit["vocab_topics"]
    topic1 = topics[0] if topics else "Thema 1"
    topic2 = topics[1] if len(topics) > 1 else (topics[0] if topics else "Thema 2")
    rule = level_sentence_rule(level)

    return f"""
You are a senior German teacher and book writer (18+ years experience).
Create content STRICTLY for level {level}.
{rule}
Adult-neutral tone. No childish tone.
No vocabulary above the level.
Follow Destination-style logic: clear lists, controlled practice, and professional workbook layout.

UNIT META:
level: "{level}"
unit_number: {unit_number}
unit_title: "{unit['unit_title']}"
main_topics: "{', '.join(topics)}"

OUTPUT FORMAT:
Return ONLY valid JSON. No comments. No markdown.

TASK:
Generate data for ONE Vocabulary Unit.
- Page 1: explanation (core vocabulary lists + short notes).
- Pages 2-3: 90-120 total exercise items across A-F.

JSON SCHEMA (fill all fields):
{json.dumps({
  "level": level,
  "unit_number": unit_number,
  "unit_title": unit["unit_title"],
  "topic1_title": topic1,
  "topic1_rows": [["", "", ""] for _ in range(8)],
  "topic2_title": topic2,
  "topic2_rows": [["", "", ""] for _ in range(8)],
  "verbs_heading": "Wichtige Verben",
  "verbs_rows": [["", ""] for _ in range(6)],
  "vocab_box": "",
  "taskA_title": "",
  "taskA_wordbox": "",
  "taskA_items": ["" for _ in range(15)],
  "taskA_mark_note": "1 Punkt pro Satz",
  "taskB_title": "",
  "taskB_wordbox": "",
  "taskB_items": ["" for _ in range(15)],
  "taskB_mark_note": "1 Punkt pro Satz",
  "taskC_title": "",
  "taskC_items": ["" for _ in range(15)],
  "taskC_mark_note": "1 Punkt pro Satz",
  "taskD_title": "",
  "taskD_items": ["" for _ in range(15)],
  "taskD_mark_note": "1 Punkt pro Satz",
  "taskE_title": "",
  "taskE_items": ["" for _ in range(15)],
  "taskE_mark_note": "1 Punkt pro Satz",
  "taskF_title": "",
  "taskF_items": ["" for _ in range(15)],
  "taskF_mark_note": "1 Punkt pro Satz",
  "total_mark": 90,
  "max_mark": 90
}, ensure_ascii=False, indent=2)}
""".strip()


def mini_review_prompt(review_number: int, unit_range: str, units):
    level = units[-1]["level"]
    rule = level_sentence_rule(level)
    topics = ", ".join(sorted({t for u in units for t in u["vocab_topics"]}))
    grammar = ", ".join(sorted({u["grammar_focus"] for u in units}))

    return f"""
You are a senior German teacher and book writer (18+ years experience).
Create content STRICTLY for level {level}.
{rule}
Adult-neutral tone. No childish tone.
Focus on review for the last two units.
Topics: {topics}
Grammar: {grammar}

OUTPUT FORMAT:
Return ONLY valid JSON. No comments. No markdown.

TASK:
Generate data for ONE mini review page (50 tasks total).

JSON SCHEMA (fill all fields):
{json.dumps({
  "review_number": review_number,
  "unit_range": unit_range,
  "sectionA_title": "",
  "sectionA_items": ["" for _ in range(10)],
  "sectionB_title": "",
  "sectionB_items": ["" for _ in range(10)],
  "sectionC_title": "",
  "sectionC_items": ["" for _ in range(10)],
  "sectionD_title": "",
  "sectionD_items": ["" for _ in range(10)],
  "sectionE_title": "",
  "sectionE_items": ["" for _ in range(10)],
  "total_mark": 50
}, ensure_ascii=False, indent=2)}
""".strip()


def big_review_prompt(unit_range: str, units):
    level = units[-1]["level"]
    rule = level_sentence_rule(level)
    topics = ", ".join(sorted({t for u in units for t in u["vocab_topics"]}))
    grammar = ", ".join(sorted({u["grammar_focus"] for u in units}))

    return f"""
You are a senior German teacher and book writer (18+ years experience).
Create content STRICTLY for level {level}.
{rule}
Adult-neutral tone. No childish tone.
Comprehensive final review for the full book.
Topics: {topics}
Grammar: {grammar}

OUTPUT FORMAT:
Return ONLY valid JSON. No comments. No markdown.

TASK:
Generate data for ONE final review (3 pages, 150 tasks total).

JSON SCHEMA (fill all fields):
{json.dumps({
  "unit_range": unit_range,
  "final_p1_items": ["" for _ in range(50)],
  "final_p2_items": ["" for _ in range(50)],
  "final_p3_items": ["" for _ in range(50)],
  "total_mark": 150
}, ensure_ascii=False, indent=2)}
""".strip()


# -------------------- HTML assembly --------------------

def extract_pages(html: str):
    return re.findall(r"<section class=\"page\">.*?</section>", html, re.S)


def assemble_book(pages):
    head = """
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>German Book</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
""".strip()
    tail = "\n</body>\n</html>\n"
    body = "\n".join(pages)
    return head + "\n" + body + tail


# -------------------- Main --------------------

def main():
    subjects = parse_subjects(SUBJECTS_FILE)

    default_name = BOOK_PDF
    user_name = input(f"Output PDF name [{default_name}]: ").strip()
    output_pdf = user_name if user_name else default_name
    if not output_pdf.lower().endswith(".pdf"):
        output_pdf += ".pdf"

    total_units = len(subjects)
    total_mini_reviews = total_units // 2
    total_steps = total_units * 2 + total_mini_reviews + 1  # +1 for big review
    completed = 0

    def step(msg: str):
        nonlocal completed
        completed += 1
        pct = int((completed / total_steps) * 100)
        print(f"[{pct:3d}%] {msg}")

    pages = []
    unit_number = 1
    review_number = 1

    for idx, unit in enumerate(subjects, 1):
        # 1) Vocabulary unit
        step(f"Vocabulary Unit {unit_number}: generating...")
        v_prompt = vocab_prompt(unit, unit_number)
        v_raw = strip_code_fences(llm(v_prompt))
        v_data = json.loads(strip_trailing_commas(v_raw))
        v_html = build_vocab_unit(v_data)
        pages.extend(extract_pages(v_html))

        # 2) Grammar unit
        step(f"Grammar Unit {unit_number}: generating...")
        g_prompt = grammar_prompt(unit, unit_number)
        g_raw = strip_code_fences(llm(g_prompt))
        g_data = json.loads(strip_trailing_commas(g_raw))
        g_html = build_grammar_unit(g_data)
        pages.extend(extract_pages(g_html))

        # Mini review after every 2 units (Variant A)
        if idx % 2 == 0:
            unit_range = f"Units {idx-1}–{idx}"
            step(f"Mini Review {review_number} ({unit_range}): generating...")
            m_prompt = mini_review_prompt(review_number, unit_range, subjects[idx-2:idx])
            m_raw = strip_code_fences(llm(m_prompt))
            m_data = json.loads(strip_trailing_commas(m_raw))
            m_html = build_mini_review(m_data)
            pages.extend(extract_pages(m_html))
            review_number += 1

        unit_number += 1

    # Big review for the whole book
    unit_range = f"Units 1–{len(subjects)}"
    step(f"Final Review ({unit_range}): generating...")
    b_prompt = big_review_prompt(unit_range, subjects)
    b_raw = strip_code_fences(llm(b_prompt))
    b_data = json.loads(strip_trailing_commas(b_raw))
    b_html = build_big_review(b_data)
    pages.extend(extract_pages(b_html))

    # Assemble and render
    book_html = assemble_book(pages)
    save(BOOK_HTML, book_html)

    ensure_pydyf_transform()
    ensure_pydyf_text_matrix()
    print("[99%] Rendering PDF...")
    HTML(filename=BOOK_HTML).write_pdf(output_pdf)
    print(f"[100%] Done: {output_pdf}")


if __name__ == "__main__":
    main()
