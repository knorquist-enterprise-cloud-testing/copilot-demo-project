"""Report generation for Copilot usage analytics."""
import json
from pathlib import Path
from datetime import datetime
from typing import Any

from .metrics import MetricPoint, aggregate_metrics


def generate_daily_report(points: list[MetricPoint], report_date: datetime) -> dict[str, Any]:
    """Generate a daily usage report."""
    day_points = [p for p in points if p.timestamp.date() == report_date.date()]
    aggregated = aggregate_metrics(day_points)

    return {
        "date": report_date.isoformat(),
        "total_events": len(day_points),
        "metrics": {
            name: {
                "count": agg.count,
                "total": agg.total,
                "avg": round(agg.avg_value, 2),
            }
            for name, agg in aggregated.items()
        },
    }


def save_report(report: dict[str, Any], output_dir: Path) -> Path:
    """Save a report to disk as JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"report-{report['date'][:10]}.json"
    path = output_dir / filename
    path.write_text(json.dumps(report, indent=2))
    return path
