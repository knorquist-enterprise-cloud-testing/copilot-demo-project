"""Metrics aggregation and analysis module."""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class MetricPoint:
    name: str
    value: float
    timestamp: datetime
    tags: dict[str, str] = field(default_factory=dict)


@dataclass
class AggregatedMetric:
    name: str
    count: int
    total: float
    min_value: float
    max_value: float
    avg_value: float


def aggregate_metrics(points: list[MetricPoint]) -> dict[str, AggregatedMetric]:
    """Aggregate metric points by name."""
    groups: dict[str, list[float]] = {}
    for point in points:
        groups.setdefault(point.name, []).append(point.value)

    result = {}
    for name, values in groups.items():
        result[name] = AggregatedMetric(
            name=name,
            count=len(values),
            total=sum(values),
            min_value=min(values),
            max_value=max(values),
            avg_value=sum(values) / len(values),
        )
    return result


def filter_by_time_range(
    points: list[MetricPoint],
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
) -> list[MetricPoint]:
    """Filter metric points to a specific time range."""
    filtered = points
    if start:
        filtered = [p for p in filtered if p.timestamp >= start]
    if end:
        filtered = [p for p in filtered if p.timestamp <= end]
    return filtered


def calculate_rate(points: list[MetricPoint], window: timedelta) -> float:
    """Calculate the rate of metric points per window."""
    if len(points) < 2:
        return 0.0
    sorted_points = sorted(points, key=lambda p: p.timestamp)
    total_time = (sorted_points[-1].timestamp - sorted_points[0].timestamp).total_seconds()
    if total_time == 0:
        return 0.0
    return len(points) / (total_time / window.total_seconds())
