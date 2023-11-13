import matplotlib
matplotlib.use("TkAgg") 
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from tabulate import tabulate

API_BASE_URL = 'https://environment.data.gov.uk/flood-monitoring/id'


def get_stations():
    api_url = f'{API_BASE_URL}/stations'
    response = requests.get(api_url)
    data = response.json(encoding='utf-8')
    return data['items']


def select_station(stations):
    print("Select a station:")
    for i, station in enumerate(stations, start=1):
        print(f"{i}. {station['label']} ({station['stationReference']})")

    while True:
        try:
            choice = int(input("Enter the number of the station: "))
            if 1 <= choice <= len(stations):
                return stations[choice - 1]['stationReference']
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_station_data(station_id):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)

    start_time_str = start_time.strftime('%Y-%m-%d')
    end_time_str = end_time.strftime('%Y-%m-%d')
    api_url = f'{API_BASE_URL}/stations/{station_id}/readings?_sorted&startdate={start_time_str}&enddate={end_time_str}'

    response = requests.get(api_url)
    data = response.json(encoding='utf-8')

    measure_values = [
        (item['@id'], item['dateTime'], item['value'])
        for item in data['items']
    ]

    timestamps = [item[1] for item in measure_values]
    values = [item[2] for item in measure_values]

    return timestamps, values


def plot_line_graph(timestamps, values):
    datetime_timestamps = [datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ') for ts in timestamps]

    plt.plot(datetime_timestamps, values, marker='o')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Station Readings over the Last 24 Hours')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def display_table(timestamps, values):
    data = list(zip(timestamps, values))
    headers = ["Timestamp", "Value"]
    table = tabulate(data, headers, tablefmt="grid")
    print(table)


if __name__ == "__main__":
    stations = get_stations()
    if not stations:
        print("No stations found.")
    else:
        station_id = select_station(stations)
        timestamps, values = get_station_data(station_id)
        plot_line_graph(timestamps, values)
        display_table(timestamps, values)

