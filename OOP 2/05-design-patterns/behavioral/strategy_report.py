"""Behavioral - Strategy: multi-format report generator.

Statement: https://courses.dallard.tech/sys_design/behavioral_pattern/
Run: python3 strategy_report.py

Problems with the original code:
1. Adding a format (XML, Markdown) means editing generate_report AND save_report
   -> violates the Open/Closed Principle.
2. The if/elif chain on format_type is duplicated in two methods.
3. One class does everything (formatting + file extensions + saving) -> violates
   Single Responsibility; formats can't be tested on their own.
4. The format is a string passed on every call, so typos fail silently
   ("Unknown format") and switching at runtime is clumsy.
5. Wrong extensions: an "excel" report is plain text saved as .xlsx.
"""
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path


# Strategy interface: the contract every format follows
class ReportFormatStrategy(ABC):
    extension: str = ".txt"

    @abstractmethod
    def format(self, data: list[dict]) -> str: ...


# Concrete strategies: one class per format
class PDFFormatStrategy(ReportFormatStrategy):
    extension = ".pdf.txt"   # text mock-up of a PDF, so don't pretend it's a real .pdf

    def format(self, data: list[dict]) -> str:
        lines = ["PDF REPORT", "=" * 50]
        lines += [f"| {item['name']:20} | {item['value']:10} |" for item in data]
        lines += ["=" * 50, "End of PDF Report"]
        return "\n".join(lines)


class ExcelFormatStrategy(ReportFormatStrategy):
    extension = ".tsv"       # tab-separated, opens in Excel

    def format(self, data: list[dict]) -> str:
        lines = ["EXCEL REPORT", "-" * 50, "Name\tValue"]
        lines += [f"{item['name']}\t{item['value']}" for item in data]
        lines.append("-" * 50)
        return "\n".join(lines) + "\n"


class CSVFormatStrategy(ReportFormatStrategy):
    extension = ".csv"

    def format(self, data: list[dict]) -> str:
        return "name,value\n" + "".join(f"{i['name']},{i['value']}\n" for i in data)


class JSONFormatStrategy(ReportFormatStrategy):
    extension = ".json"

    def format(self, data: list[dict]) -> str:
        return json.dumps(data, indent=2)


# Context: knows nothing about formats, delegates to the current strategy
class ReportGenerator:
    def __init__(self, data: list[dict],
                 strategy: ReportFormatStrategy | None = None) -> None:
        self.data = data
        self._strategy = strategy or CSVFormatStrategy()

    def set_strategy(self, strategy: ReportFormatStrategy) -> None:
        self._strategy = strategy

    def generate_report(self) -> str:
        return self._strategy.format(self.data)

    def save_report(self, filename: str) -> Path:
        path = Path(filename + self._strategy.extension)
        path.write_text(self.generate_report(), encoding="utf-8")
        return path


# Final test: HTML added WITHOUT touching any existing class
class HTMLFormatStrategy(ReportFormatStrategy):
    extension = ".html"

    def format(self, data: list[dict]) -> str:
        rows = "\n".join(f"    <tr><td>{i['name']}</td><td>{i['value']}</td></tr>" for i in data)
        return ("<table>\n    <tr><th>Name</th><th>Value</th></tr>\n"
                f"{rows}\n</table>")


if __name__ == "__main__":
    data = [
        {"name": "Sales Q1", "value": 15000},
        {"name": "Sales Q2", "value": 18000},
        {"name": "Sales Q3", "value": 22000},
        {"name": "Sales Q4", "value": 25000},
    ]
    generator = ReportGenerator(data)

    for title, strategy in [("PDF", PDFFormatStrategy()), ("EXCEL", ExcelFormatStrategy()),
                            ("CSV", CSVFormatStrategy()), ("JSON", JSONFormatStrategy()),
                            ("HTML (NEW!)", HTMLFormatStrategy())]:
        print(f"=== {title} FORMAT ===")
        generator.set_strategy(strategy)       # switched at runtime
        print(generator.generate_report())
        print("\n" + "=" * 60 + "\n")

    generator.set_strategy(CSVFormatStrategy())
    print("saved:", generator.save_report("sales_report"))
