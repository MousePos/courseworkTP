from django.urls import path
from .views import home, aggregate_view, calculate_view

urlpatterns = [
    path('home/', home),  # Главная страница
    path('aggregate/<str:aggregation_type>/', aggregate_view, name='aggregate_view'),  
    path('calculate/', calculate_view, name='calculate'),
    # Общий маршрут для агрегации (avg, max, min, sum)
]
