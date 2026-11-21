"""Structural - Adapter: make the legacy XML reporter usable by the JSON dashboard.

Statement: https://courses.dallard.tech/sys_design/structural_pattern/
Run: python3 adapter_report.py
"""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


# Legacy reporting system (can't modify - external library)
class LegacyReportGenerator:
    def generate_report(self, data: dict) -> str:
        """Returns XML format - old system"""
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml


# New analytics dashboard expects JSON
class AnalyticsDashboard:
    def display(self, json_data: str) -> None:
        data = json.loads(json_data)
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")


# The interface the client (dashboard code) expects
class ReportGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        """Return the report as a JSON string."""


class LegacyReportAdapter(ReportGeneratorInterface):
    """Wraps LegacyReportGenerator and converts its XML output to JSON."""

    def __init__(self, legacy: LegacyReportGenerator) -> None:
        self._legacy = legacy

    def generate(self, data: dict) -> str:
        xml_report = self._legacy.generate_report(data)
        return self._xml_to_json(xml_report)

    @staticmethod
    def _xml_to_json(xml_report: str) -> str:
        # Real conversion from the XML string - no "cheating" with the original dict
        root = ET.fromstring(xml_report)
        result = {child.tag: LegacyReportAdapter._parse_value(child.text or "")
                  for child in root}
        return json.dumps(result)

    @staticmethod
    def _parse_value(text: str) -> int | float | str:
        # XML loses types (everything is text), so restore numbers
        for cast in (int, float):
            try:
                return cast(text)
            except ValueError:
                pass
        return text


# Business code no longer knows anything about XML
def show_report(generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard,
                data: dict) -> None:
    dashboard.display(generator.generate(data))


if __name__ == "__main__":
    report_generator = LegacyReportAdapter(LegacyReportGenerator())
    dashboard = AnalyticsDashboard()

    show_report(report_generator, dashboard,
                {"total_sales": 150000, "orders": 1234, "avg_order": 121.55})
    show_report(report_generator, dashboard,
                {"total_items": 5000, "low_stock": 45, "out_of_stock": 12})
