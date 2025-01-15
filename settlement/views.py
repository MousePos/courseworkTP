from django.shortcuts import render
from .models import Settlement
from django.db.models import Avg, Min, Max, Sum
from typing import Protocol, Any

class AggregationStrategy(Protocol):
    def aggregate(self) -> Any:
        pass

class AverageAggregation(AggregationStrategy):
    def aggregate(self):
        return {
            'avg_budget': Settlement.objects.aggregate(Avg("budget")),
            'avg_population': Settlement.objects.aggregate(Avg("population"))
        }

class MaxAggregation(AggregationStrategy):
    def aggregate(self):
        return {
            'max_budget': Settlement.objects.aggregate(Max("budget")),
            'max_population': Settlement.objects.aggregate(Max("population"))
        }

class MinAggregation(AggregationStrategy):
    def aggregate(self):
        return {
            'min_budget': Settlement.objects.aggregate(Min("budget")),
            'min_population': Settlement.objects.aggregate(Min("population"))
        }

class SumAggregation(AggregationStrategy):
    def aggregate(self):
        return {
            'sum_budget': Settlement.objects.aggregate(Sum("budget")),
            'sum_population': Settlement.objects.aggregate(Sum("population"))
        }

# GoF Pattern 2: Factory Method
class AggregationFactory:
    @staticmethod
    def get_strategy(aggregation_type: str) -> AggregationStrategy:
        strategies = {
            'avg': AverageAggregation,
            'max': MaxAggregation,
            'min': MinAggregation,
            'sum': SumAggregation
        }
        return strategies.get(aggregation_type, AverageAggregation)()

# Views
def home(request):
    return render(request, 'settlement/index.html')

def aggregate_view(request, aggregation_type):
    strategy = AggregationFactory.get_strategy(aggregation_type)
    data = strategy.aggregate()
    return render(request, f'settlement/{aggregation_type}.html', data)
