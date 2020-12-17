# coding=utf-8
import requests
import json
import csv
import random

# 在 devices 数组中获取随机 deviceID
# 代码: random.sample(devices, 1)[0]
devices = [
    1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011,
    1012, 1013, 1014, 1017, 1018, 1019, 1801, 1802, 1803, 1804, 1805,
    1807, 1808, 1809, 1810, 1821, 1822, 1823, 1825, 2001, 2002, 2003,
    2004, 2005, 2006, 3001, 3003, 3004, 3005, 3006, 4001, 4003, 4005,
    4006, 5001, 5002, 5003
]


def get_location(lng, lat):
    """
    根据坐标请求百度 API 获取坐标位置信息
    :param lng: 经度
    :param lat: 纬度
    :return: Dict
    """
    url = f'http://api.map.baidu.com/reverse_geocoding/v3/?ak=snqi8PHhrbovyrT5sBXz5GNHZdFcqiGj&output=json&coordtype=wgs84ll&location={lat},{lng}'

    response = requests.get(url)

    data = response.json()
    return data


def get_points(lng_start: int, lng_end: int, lat_start: int, lat_end: int, num: int):
    """
    生成随机百度地图坐标
    :param lng_start: 起始经度值 (整型)
    :param lng_end: 结束经度值 (整型)
    :param lat_start: 起始纬度值 (整型)
    :param lat_end: 结束纬度值 (整型)
    :param num: 生成个数 (整型)
    :return: Dict
    """
    points = {}
    for i in range(0, num):
        lng = round(random.randint(lng_start, lng_end) + random.random(), 6)
        lat = round(random.randint(lat_start, lat_end) + random.random(), 6)
        points[lng] = str(lat)
    return points


# data_set = {'location': 'middle', 'detail_data': []}

# middle area
# loca_data = get_points(99, 120, 23, 41, 180000)
# west area
loca_data = get_points(74, 99, 28, 42, 180000)
# east area
# loca_data = get_points(120, 130, 41, 50, 180000)

# print(json.dumps(loca_data, indent=4))

# csv格式保存
f2 = open("data/china.csv", "a", encoding="utf-8", newline="")
csv_writer = csv.writer(f2)
# csv_writer.writerow(['province', 'city', 'longitude', 'latitude', 'device_type'])

for key, value in loca_data.items():
    bd_data = get_location(key, value)
    if bd_data['result']['addressComponent']['country_code'] == 0:
        # piece = {
        #     'province': bd_data['result']['addressComponent']['province'],
        #     'city': bd_data['result']['addressComponent']['city'],
        #     'longitude': str(key),
        #     'latitude': str(value),
        #     'device_type': str(random.sample(devices, 1)[0])
        # }
        # data_set['detail_data'].append(piece)
        csv_writer.writerow([
            bd_data['result']['addressComponent']['province'],
            bd_data['result']['addressComponent']['city'],
            str(key),
            str(value),
            str(random.sample(devices, 1)[0])
        ])

f2.close()

# json格式保存(副本)
# f1 = open("middle.json", "w")
# json.dump(data_set, f1, indent=4, ensure_ascii=False)
# f1.close()
#
# print(json.dumps(data_set, indent=4, ensure_ascii=False))
