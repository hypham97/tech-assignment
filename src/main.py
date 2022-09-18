from ast import literal_eval
from dataclasses import dataclass
from typing import List, Optional, Tuple
import sys
import io

@dataclass
class Point:
    x: float
    y: float
    
    def get_distance(self, point: 'Point'):
        return ((self.x - point.x)**2 + (self.y - point.y)**2)**.5

@dataclass
class LinkStation(Point):
    
    reach: float

    def get_power(self, device: 'Device') -> float:
        distance = self.get_distance(device)
        return (self.reach - distance)**2 if distance < self.reach else 0

@dataclass
class Device(Point):
    def get_best_station(self, link_stations: List[LinkStation]) -> Tuple[Optional[LinkStation], int]:
        best_station = None
        best_power = 0

        for station in link_stations:
            power = station.get_power(self)

            if power > best_power:
                best_station = station
                best_power = power

        return best_station, best_power

def found_best_station(link_stations: List[LinkStation], devices: List[Device]):
    for device in devices:
        station, power = device.get_best_station(link_stations)
        if station is None:
            print('No link station within reach for point {},{}'.format(device.x, device.y))
        else:
            print('Best link station for point {},{} is {},{} with power {}'.format(device.x, device.y, station.x, station.y, power))

def sample_data():
    link_stations = [
        LinkStation(x=0, y=0, reach=10),
        LinkStation(x=20, y=20, reach=5),
        LinkStation(x=10, y=0, reach=12)
    ]

    devices = [
        Device(x=0, y=0),
        Device(x=100, y=100),
        Device(x=15, y=10),
        Device(x=18, y=18)
    ]
    
    found_best_station(link_stations, devices)

def user_input_data(prompt: str) -> List[Tuple]:
    while (True):
        try:
            data = literal_eval(input(prompt))

            if type(data) is list and type(data[0]) is tuple:
                return data
            
            elif type(data) is tuple:
                return [data]
            
            raise ValueError

        except Exception:
            print("Wrong type of data. Try again! Examples: (1,2,3), (4,5,6)")

def capture_out(func: callable) -> str:
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    func()

    output = new_stdout.getvalue()
    return output

def main():
    link_stations: List[LinkStation] = []
    link_stations_params = user_input_data("Link stations (x, y, reach): ")
    for params in link_stations_params:
        link_stations.append(LinkStation(*params))
    
    devices: List[Device] = []
    devices_params = user_input_data("Devices (x, y): ")
    for params in devices_params:
        devices.append(Device(*params))
    
    found_best_station(link_stations, devices)

def cloud_function(request) -> dict:
    params = request.get_json()

    if 'sample' in params and params.get('sample') is True:
        output = capture_out(sample_data)
        
        return {'statusCode': 200, 'body': output}
    
    elif 'link-stations' in params and 'devices' in params:
        link_stations: List[LinkStation] = []
        devices: List[Device] = []

        for s in params.get('link-stations'):
            link_stations.append(LinkStation(s['x'],s['y'],s['reach']))
        for d in params.get('devices'):
            devices.append(Device(d['x'],d['y']))

        output = capture_out(lambda: found_best_station(link_stations, devices))
        
        return {'statusCode': 200, 'body': output}

    return {'statusCode': 400, 'body': 'Bad request'}

if __name__ == '__main__':
    sample = input("Use sample data? (y/n): ") == 'y'

    if sample:
        sample_data()
    else:
        main()
