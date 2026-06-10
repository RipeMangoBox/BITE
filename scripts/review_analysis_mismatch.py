import csv
import os
from typing import Dict, List, Tuple, Optional


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER_ANALYSIS_DIR = os.path.join(ROOT_DIR, "obsidian-vault/analysis")
LOG_PATH = os.path.join(ROOT_DIR, "obsidian-vault/paper_list.csv")
REPORT_PATH = os.path.join(ROOT_DIR, "obsidian-vault/batches/reports/analysis_mismatch_report.txt")


class AnalysisFile:
    def __init__(self, path: str, title: str, content: str, has_abstract: bool,
                 has_method_section: bool, has_experiment_section: bool,
                 has_local_reading: bool, has_metrics_table: bool,
                 has_pdf_ref: bool):
        self.path = path
        self.title = title
        self.content = content
        self.has_abstract = has_abstract
        self.has_method_section = has_method_section
        self.has_experiment_section = has_experiment_section
        self.has_local_reading = has_local_reading
        self.has_metrics_table = has_metrics_table
        self.has_pdf_ref = has_pdf_ref

    @property
    def is_emergent_style_basic_ok(self) -> bool:
        structural_ok = (
            self.has_abstract
            and self.has_method_section
            and self.has_experiment_section
            and self.has_local_reading
        )
        depth_ok = self.has_metrics_table
        meta_ok = self.has_pdf_ref
        return structural_ok and depth_ok and meta_ok


def parse_frontmatter_and_body(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    front = {}
    body_lines: List[str] = []
    in_front = True
    for idx, line in enumerate(lines[1:], start=1):
        if in_front and line.strip() == "---":
            body_lines = lines[idx + 1 :]
            break
        if in_front:
            if ":" in line:
                key, value = line.split(":", 1)
                front[key.strip()] = value.strip()
        else:
            body_lines.append(line)

    if not body_lines:
        return front, text
    return front, "\n".join(body_lines)


def build_analysis_index() -> Dict[str, AnalysisFile]:
    index: Dict[str, AnalysisFile] = {}
    for root, _dirs, files in os.walk(PAPER_ANALYSIS_DIR):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            if fname == "README.md":
                continue
            path = os.path.join(root, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
            except UnicodeDecodeError:
                continue

            front, body = parse_frontmatter_and_body(text)
            raw_title = front.get("title")
            if raw_title:
                title = raw_title.strip().strip('"').strip("'")
            else:
                title = ""
                for line in body.splitlines():
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
                if not title:
                    continue

            lower_body = body.lower()

            has_abstract = "[!abstract" in lower_body
            has_method_section = any(
                marker in body
                for marker in ("## 整体框架", "## 核心模块与公式推导", "## 核心创新")
            )
            has_experiment_section = "## 实验与分析" in body
            has_local_reading = "local reading" in lower_body or "## 原文 PDF" in body

            has_metrics_table = False
            for line in body.splitlines():
                if "|" in line and any(tok in line.lower() for tok in ["fid", "%", "accuracy", "top-1", "top-3"]):
                    has_metrics_table = True
                    break

            has_pdf_ref = any(
                ln.strip().startswith("pdf_ref:")
                for ln in text.splitlines()
            )

            index[title] = AnalysisFile(
                path=path,
                title=title,
                content=text,
                has_abstract=has_abstract,
                has_method_section=has_method_section,
                has_experiment_section=has_experiment_section,
                has_local_reading=has_local_reading,
                has_metrics_table=has_metrics_table,
                has_pdf_ref=has_pdf_ref,
            )
    return index


def load_log_rows() -> List[List[str]]:
    with open(LOG_PATH, "r", encoding="utf-8", newline="") as f:
        return [row for row in csv.reader(f)]


def save_log_rows(rows: List[List[str]]) -> None:
    with open(LOG_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def split_head_tail(title: str) -> Tuple[str, str]:
    if ":" in title:
        head, tail = title.split(":", 1)
        return head.strip(), tail.strip()
    return title.strip(), ""


def find_analysis_for_title(log_title: str, index: Dict[str, AnalysisFile]) -> Optional[AnalysisFile]:
    if log_title in index:
        return index[log_title]

    for t, af in index.items():
        if t.lower() == log_title.lower():
            return af

    log_head, log_tail = split_head_tail(log_title)
    log_tail_lower = log_tail.lower()
    for t, af in index.items():
        af_head, af_tail = split_head_tail(t)
        if not log_tail and not af_tail:
            continue
        af_tail_lower = af_tail.lower()
        if log_tail_lower and af_tail_lower:
            if log_tail_lower == af_tail_lower or log_tail_lower in af_tail_lower or af_tail_lower in log_tail_lower:
                return af

    for t, af in index.items():
        t_lower = t.lower()
        lt_lower = log_title.lower()
        if lt_lower in t_lower or t_lower in lt_lower:
            return af

    return None


def describe_mismatch(af: Optional[AnalysisFile]) -> str:
    if af is None:
        return "no_markdown: 未在 obsidian-vault/analysis 目录下找到对应标题的 emergentmind 分析 .md 文件。"

    missing = []
    if not af.has_abstract:
        missing.append("Abstract / [!abstract] 区块")
    if not af.has_method_section:
        missing.append("现代方法/框架语义章节")
    if not af.has_experiment_section:
        missing.append("实验与分析章节")
    if not af.has_local_reading:
        missing.append("Local Reading / 本地 PDF 引用部分")
    if not af.has_metrics_table:
        missing.append("包含具体指标的实验表格或数值")
    if not af.has_pdf_ref:
        missing.append("frontmatter 中的 pdf_ref 字段")

    if not missing:
        return "ok: 结构与技术深度均符合当前 ResearchFlow 分析模板，之前标记为 analysis_mismatch 属于误判。"

    return "structure_or_depth: 缺失以下 ResearchFlow 分析要素：" + "；".join(missing)


def review_all_analysis_mismatch() -> None:
    index = build_analysis_index()
    rows = load_log_rows()

    data_start = 1 if rows and rows[0] and rows[0][0] == "state" else 0

    report_rows: List[str] = []
    report_rows.append("# analysis_mismatch 复查报告")
    report_rows.append("")
    report_rows.append(f"根目录: {ROOT_DIR}")
    report_rows.append(f"日志文件: {LOG_PATH}")
    report_rows.append("")
    report_rows.append("| Status(before) | Status(after) | Title | Reason |")
    report_rows.append("| --- | --- | --- | --- |")

    for i in range(data_start, len(rows)):
        row = (rows[i] + [""] * 8)[:8]
        status, title = row[0], row[2]
        if status != "analysis_mismatch":
            continue

        af = find_analysis_for_title(title, index)
        reason = describe_mismatch(af)

        if af is not None and af.is_emergent_style_basic_ok:
            new_status = "checked"
            row[0] = new_status
            rows[i] = row
        else:
            new_status = status

        report_rows.append(f"| {status} | {new_status} | {title} | {reason} |")

    save_log_rows(rows)

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(report_rows) + "\n")

    print("=== analysis_mismatch review completed ===")
    print(f"- Updated log: {LOG_PATH}")
    print(f"- Report: {REPORT_PATH}")


if __name__ == "__main__":
    review_all_analysis_mismatch()
