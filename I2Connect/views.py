# I2Connect/views.py

from django.shortcuts import render
from Sensors.traffic_data import get_simulated_traffic_data


def traffic_view(request):
    # Get simulated traffic data
    traffic_data = get_simulated_traffic_data()

    # Pass the data to the template
    return render(request, 'I2Connect/traffic_template.html', {'traffic_data': traffic_data})
