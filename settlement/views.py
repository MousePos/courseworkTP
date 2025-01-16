from django.shortcuts import render
from .models import Settlement
from django.db.models import Avg, Min, Max, Sum
from typing import Protocol, Any, List, Dict
from abc import ABC, abstractmethod


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

class Calc(ABC):
    @abstractmethod
    def calculate(self, values: List[float]) -> float:
        pass


class CalcAvg(Calc):
    def calculate(self, data: List[Dict]) -> float:
        if not data:
            return 0.0
        budgets = [entry['budget'] for entry in data]
        populations = [entry['population'] for entry in data]
        b = sum(budgets) / len(budgets)
        p = sum(populations) / len(populations)
        return b, p
    

class CalcAvgC(Calc):
    def calculate(self, data: List[Dict]) -> float:
        if not data or len(data) < 3:
            return 0.0
        budgets = sorted(entry['budget'] for entry in data)
        populations = [entry['population'] for entry in data]
        trimmed_budgets = budgets[1:-1]
        trimmed_populations = populations[1:-1]
        b = sum(trimmed_budgets) / len(trimmed_budgets)
        p = sum(trimmed_populations) / len(trimmed_populations)
        return b, p

class CalculationContext:
    def __init__(self, strategy: Calc):
        self.strategy = strategy

    def set_strategy(self, strategy: Calc):
        self.strategy = strategy

    def execute(self, data: List[Dict]) -> float:
        return self.strategy.calculate(data)
    
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

def calcAvg(request):
    return render(request)

def get_budget_data(data):
    budget = data[0]
    return budget

def get_population_data(data):
    population = data[1]
    return population


def calculate_view(request):
    # Извлекаем данные из базы
    settlements = Settlement.objects.all().values('budget', 'population')
    data = list(settlements)

    context = CalculationContext(CalcAvg())
    avg_result = context.execute(data)
    avg_result_budget = get_budget_data(avg_result)
    avg_result_population = get_population_data(avg_result)
    # Среднее без учета экстремальных значений
    context.set_strategy(CalcAvgC())
    avg_clear_result = context.execute(data)
    avg_result_budget_clear = get_budget_data(avg_clear_result)
    avg_result_population_clear = get_population_data(avg_clear_result)


    return render(request, 'settlement/calculations.html', {
        'avg_result_budget': avg_result_budget,
        'avg_result_population': avg_result_population,
        'avg_result_budget_clear': avg_result_budget_clear,
        'avg_result_population_clear': avg_result_population_clear
    })
