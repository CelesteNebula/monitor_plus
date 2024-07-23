from flask import Blueprint, jsonify
from service.classify import car_count, person_count, total_jam, motorbike_count, bicycle_count, bus_count, \
    tmp_car_count, tmp_person_count

data_route = Blueprint('data_route', __name__)


@data_route.route('/car_chart', methods=['GET'])
def get_car_chart_data():
    # 获取四个视频线程一次模型处理后的除人以外的数量
    print('car: ', tmp_car_count)
    return jsonify({'carNum': tmp_car_count})


@data_route.route('/person_chart', methods=['GET'])
def get_person_chart_data():
    # 获取四个视频线程一次模型处理后的人数
    print('person: ', [tmp_person_count[i] for i in range(4)])
    return jsonify({'personNum': [tmp_person_count[i] for i in range(4)]})


@data_route.route('/car', methods=['GET'])
def get_car_data():
    car_data = [car_count[i] + bicycle_count[i] + bus_count[i] + motorbike_count[i] for i in range(4)]
    print('car: ', car_data)
    return jsonify({'carNum': car_data})


@data_route.route('/person', methods=['GET'])
def get_person_data():
    print('person: ', [person_count[i] for i in range(4)])
    return jsonify({'personNum': [person_count[i] for i in range(4)]})


@data_route.route('/pie', methods=['GET'])
def get_pie_data():
    # 获取四个视频线程从始至终经过模型处理后的五种类别的数量
    return jsonify({
        'personNum': sum(person_count),
        'bicycleNum': sum(bicycle_count),
        'busNum': sum(bus_count),
        'motorNum': sum(motorbike_count),
        'carNum': sum(car_count),
    })


@data_route.route('/jam', methods=['GET'])
def get_jam_data():
    # 获取四个视频线程一次模型处理后的五种类别的全部数量
    jam_data = [
        car_count[i] + person_count[i] + bicycle_count[i] + bus_count[i] + motorbike_count[i]
        for i in range(4)
    ]
    return jsonify({f'video{i + 1}': jam_data[i] for i in range(4)})
