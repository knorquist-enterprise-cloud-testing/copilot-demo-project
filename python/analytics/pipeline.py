"""Data pipeline for processing raw metric events."""
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Iterator

from .metrics import MetricPoint


@dataclass
class PipelineStage:
    name: str
    transform: Callable[[list[MetricPoint]], list[MetricPoint]]


class Pipeline:
    def __init__(self) -> None:
        self.stages: list[PipelineStage] = []

    def add_stage(self, name: str, transform: Callable[[list[MetricPoint]], list[MetricPoint]]) -> "Pipeline":
        self.stages.append(PipelineStage(name=name, transform=transform))
        return self

    def execute(self, data: list[MetricPoint]) -> list[MetricPoint]:
        result = data
        for stage in self.stages:
            result = stage.transform(result)
        return result


def deduplicate(points: list[MetricPoint]) -> list[MetricPoint]:
    seen: set[tuple[str, str]] = set()
    result = []
    for p in points:
        key = (p.name, p.timestamp.isoformat())
        if key not in seen:
            seen.add(key)
            result.append(p)
    return result


def remove_outliers(points: list[MetricPoint], threshold: float = 3.0) -> list[MetricPoint]:
    if not points:
        return points
    values = [p.value for p in points]
    mean = sum(values) / len(values)
    std = (sum((v - mean) ** 2 for v in values) / len(values)) ** 0.5
    if std == 0:
        return points
    return [p for p in points if abs(p.value - mean) / std <= threshold]
