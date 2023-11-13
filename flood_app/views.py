import requests
from datetime import datetime
from django.shortcuts import render
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
from flood_monitor.settings import BASE_DIR

def home(request):
    api_url = 'https://environment.data.gov.uk/flood-monitoring/id/stations'
    response = requests.get(api_url)
    data = response.json(encoding='utf-8')
    measure_values = [(item['@id'], item['label'], item['stationReference']) for item in data['items']]
    return render(request, 'index.html', {'measure_values': measure_values})

def get_station_details(request):
    station_id = request.GET.get("station")
    if not station_id:       
        return render(request, 'index.html', {'error_message': 'Station ID is missing'})

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)

    start_time_str = start_time.strftime('%Y-%m-%d')
    end_time_str = end_time.strftime('%Y-%m-%d')
    api_url = f'https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id}/readings?_sorted&startdate={start_time_str}&enddate={end_time_str}'
    response = requests.get(api_url)
    data = response.json(encoding='utf-8')
 
    measure_values = [
    (
        item['@id'],
        item['dateTime'],
        item['value']
    )
    for item in data['items'] 
    ]

    timestamps = [item[1] for item in measure_values]
    values = [item[2] for item in measure_values]
   
    img_base64 = plot_line_graph(timestamps, values,filename='graph.png')

    return render(request, 'graph.html', {'data': data['items'], 'graph_image': img_base64})



def plot_line_graph(timestamps, values,filename=None):
  
    datetime_timestamps = [datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ') for ts in timestamps]
   
    plt.plot(datetime_timestamps, values, marker='o')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Station Readings over the Last 24 Hours')
    plt.xticks(rotation=45)
    plt.tight_layout()

    if filename:
        static_path = os.path.join('static', filename)
        full_path = os.path.join(BASE_DIR, static_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        if os.path.exists(full_path):
            os.remove(full_path)

        plt.savefig(full_path)
        plt.clf()
        return static_path
        
    else:
        plt.show()
