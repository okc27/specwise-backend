from django.urls import path
from .views import classify_query ,question_details , hardware_recommendation

urlpatterns = [
    path('classify-query/', classify_query, name='classify_query'),
    path('question_details/', question_details, name='question_details'),
    path('hardware_recommendation/', hardware_recommendation, name='hardware_recommendation'),
]
