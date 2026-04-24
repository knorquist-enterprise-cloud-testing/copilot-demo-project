package models

import "time"

type Metric struct {
	ID        string            `json:"id"`
	Name      string            `json:"name"`
	Value     float64           `json:"value"`
	Timestamp time.Time         `json:"timestamp"`
	Tags      map[string]string `json:"tags,omitempty"`
}

type AggregatedMetric struct {
	Name     string  `json:"name"`
	Count    int     `json:"count"`
	Total    float64 `json:"total"`
	Average  float64 `json:"average"`
	MinValue float64 `json:"min_value"`
	MaxValue float64 `json:"max_value"`
}

func Aggregate(metrics []Metric) map[string]AggregatedMetric {
	groups := make(map[string][]float64)
	for _, m := range metrics {
		groups[m.Name] = append(groups[m.Name], m.Value)
	}

	result := make(map[string]AggregatedMetric)
	for name, values := range groups {
		var total, minVal, maxVal float64
		minVal = values[0]
		maxVal = values[0]
		for _, v := range values {
			total += v
			if v < minVal {
				minVal = v
			}
			if v > maxVal {
				maxVal = v
			}
		}
		result[name] = AggregatedMetric{
			Name:     name,
			Count:    len(values),
			Total:    total,
			Average:  total / float64(len(values)),
			MinValue: minVal,
			MaxValue: maxVal,
		}
	}
	return result
}
