package server

import (
	"sync"
	"time"

	"github.com/knorquist-enterprise-cloud-testing/copilot-demo-project/go/pkg/models"
)

type MetricCollector struct {
	mu      sync.RWMutex
	metrics []models.Metric
	maxSize int
}

func NewMetricCollector(maxSize int) *MetricCollector {
	return &MetricCollector{
		metrics: make([]models.Metric, 0, maxSize),
		maxSize: maxSize,
	}
}

func (c *MetricCollector) Add(m models.Metric) {
	c.mu.Lock()
	defer c.mu.Unlock()

	if len(c.metrics) >= c.maxSize {
		c.metrics = c.metrics[1:]
	}
	c.metrics = append(c.metrics, m)
}

func (c *MetricCollector) GetAll() []models.Metric {
	c.mu.RLock()
	defer c.mu.RUnlock()

	result := make([]models.Metric, len(c.metrics))
	copy(result, c.metrics)
	return result
}

func (c *MetricCollector) GetSince(since time.Time) []models.Metric {
	c.mu.RLock()
	defer c.mu.RUnlock()

	var result []models.Metric
	for _, m := range c.metrics {
		if m.Timestamp.After(since) {
			result = append(result, m)
		}
	}
	return result
}

func (c *MetricCollector) Count() int {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return len(c.metrics)
}
