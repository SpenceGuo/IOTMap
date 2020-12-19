import requests
import json
import csv
import random

from config import *


# 设置传感器设备的种类
devices_type_num = 10


def get_location(lng, lat):
    """
    根据坐标请求百度 API 获取坐标位置信息
    :param lng: 经度
    :param lat: 纬度
    :return: Dict
    """
    url = f'http://api.map.baidu.com/reverse_geocoding/v3/?ak={baiduAPI_ak}&output=json&coordtype=wgs84ll&location={lat},{lng}'

    response = requests.get(url)

    data = response.json()
    return data


def get_points(lng_start: int, lng_end: int, lat_start: int, lat_end: int, num: int):
    """
    随机生成百度地图坐标
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


def main():
    global devices_type_num

    # China's territory in baiduMap
    location_data = get_points(73, 135, 14, 53, 1000000)

    # csv格式保存
    f2 = open("data/china.csv", "a", encoding="utf-8", newline="")
    csv_writer = csv.writer(f2)
    # csv_writer.writerow(['province', 'city', 'district', 'longitude', 'latitude', 'device_type'])

    for key, value in location_data.items():
        bd_data = get_location(key, value)
        if bd_data['result']['addressComponent']['country_code'] == 0:
            csv_writer.writerow([
                bd_data['result']['addressComponent']['province'],
                bd_data['result']['addressComponent']['city'],
                bd_data['result']['addressComponent']['district'],
                str(key),
                str(value),
                str(random.randint(1, devices_type_num))
            ])
    f2.close()


if __name__ == '__main__':
    main()
