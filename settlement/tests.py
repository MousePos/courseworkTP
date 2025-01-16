from django.test import TestCase
from unittest.mock import patch
from .models import Settlement
from django.db.models import Avg, Min, Max, Sum
from .views import AverageAggregation, MaxAggregation, MinAggregation, SumAggregation, CalcAvg, CalcAvgC
import json


# Create your tests here.
class AggregationViewTests(TestCase):

    def test_name_length_validation(self):
        settlement = Settlement(name='A' * 50, type='B' * 30, budget=1000, population=500, head='Ivan')
        try:
            settlement.full_clean()  # Проверяет валидность модели
        except Exception as e:
            self.fail(f"Validation failed: {e}")

        settlement.name = 'A' * 51  # Длина превышает max_length
        settlement.type = 'B' * 51
        with self.assertRaises(Exception):
            settlement.full_clean()
   
    @patch('settlement.models.Settlement.objects.aggregate')
    def test_average_aggregation(self, mock_aggregate):
        mock_aggregate.side_effect = [
            {'budget__avg': 1000},
            {'population__avg': 500}
        ]
        response = self.client.get('/aggregate/avg/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Средний бюджет')
        self.assertContains(response, 'Среднее население')

    @patch('settlement.models.Settlement.objects.aggregate')
    def test_max_aggregation(self, mock_aggregate):
        mock_aggregate.side_effect = [
            {'budget__max': 2000},
            {'population__max': 800}
        ]
        response = self.client.get('/aggregate/max/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Максимальный бюджет')
        self.assertContains(response, 'Максимальное население')

    @patch('settlement.models.Settlement.objects.aggregate')
    def test_min_aggregation(self, mock_aggregate):
        mock_aggregate.side_effect = [
            {'budget__min': 300},
            {'population__min': 100}
        ]
        response = self.client.get('/aggregate/min/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Минимальный бюджет')
        self.assertContains(response, 'Минимальное население')

    @patch('settlement.models.Settlement.objects.aggregate')
    def test_sum_aggregation(self, mock_aggregate):
        mock_aggregate.side_effect = [
            {'budget__sum': 5000},
            {'population__sum': 1500}
        ]
        response = self.client.get('/aggregate/sum/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Суммарный бюджет')
        self.assertContains(response, 'Суммарное население')


    def test_aggregation_with_json(self):
        # Пример JSON-данных
        with open('settlement/data.json', 'r') as file:
            json_data = json.load(file)

        # Загрузка данных в модель
        for entry in json_data:
            Settlement.objects.create(
                name=entry["name"],
                type=entry["type"],
                budget=entry["budget"],
                population=entry["population"],
                head=entry["head"]
            )

        # Проверка средней агрегации через AverageAggregation
        strategy = AverageAggregation()
        result = strategy.aggregate()

        self.assertEqual(result["avg_budget"]["budget__avg"], 1500)  # (1000 + 2000 + 1500) / 3
        self.assertEqual(result["avg_population"]["population__avg"], 533.3333333333334)  # (500 + 800 + 300) / 3

        
        strategy = MaxAggregation()
        result = strategy.aggregate()

        self.assertEqual(result["max_budget"]["budget__max"], 2000)  # (1000 + 2000 + 1500) / 3
        self.assertEqual(result["max_population"]["population__max"], 800)  # (500 + 800 + 300) / 3

        strategy = MinAggregation()
        result = strategy.aggregate()

        self.assertEqual(result["min_budget"]["budget__min"], 1000)  # (1000 + 2000 + 1500) / 3
        self.assertEqual(result["min_population"]["population__min"], 300)  # (500 + 800 + 300) / 3

        strategy = SumAggregation()
        result = strategy.aggregate()

        self.assertEqual(result["sum_budget"]["budget__sum"], 4500)  # (1000 + 2000 + 1500) / 3
        self.assertEqual(result["sum_population"]["population__sum"], 1600)  # (500 + 800 + 300) / 3

class CalculationTests(TestCase):

    def setUp(self):
        # Создаем тестовые данные
        Settlement.objects.create(budget=100, population=500)
        Settlement.objects.create(budget=200, population=1000)
        Settlement.objects.create(budget=300, population=1500)
        Settlement.objects.create(budget=400, population=2000)

    def test_calc_avg(self):
        data = list(Settlement.objects.all().values('budget', 'population'))
        context = CalcAvg()
        avg_result = context.calculate(data)
        self.assertEqual(avg_result[0], 250.0)  # average of budget
        self.assertEqual(avg_result[1], 1250.0)  # average of population

    def test_calc_avg_c(self):
        data = list(Settlement.objects.all().values('budget', 'population'))
        context = CalcAvgC()
        avg_clear_result = context.calculate(data)
        self.assertEqual(avg_clear_result[0], 250.0)  # average of budget after trimming
        self.assertEqual(avg_clear_result[1], 1250.0)  # average of population after trimming