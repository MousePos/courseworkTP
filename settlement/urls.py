from django.urls import path
from .views import home, aggregate_view

urlpatterns = [
    path('home/', home, name='home'),  # Главная страница
    path('aggregate/<str:aggregation_type>/', aggregate_view, name='aggregate_view'),  
    # Общий маршрут для агрегации (avg, max, min, sum)
]
