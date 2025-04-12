# machinery/urls.py
from django.urls import path

app_name = 'machinery'

'''
All routes for machines defined here.
    - Web routes:
        Currently empty as this app only has API routes
    - API routes:
        Now moved to machinery/api/urls.py and included at the project level
'''

# Web URLs (currently empty as this app only has API routes)
urlpatterns = [
    # No URLs needed here as the API routes are included at the project level
]
