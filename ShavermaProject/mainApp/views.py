from datetime import datetime
from json import loads
from math import hypot
from threading import Thread
from time import sleep, time

import pytz
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from mainApp.eth_works import make_transaction, add_order, get_order_info, \
    get_stats, get_uncompleted_orders, change_to_delivery_status, \
    change_to_completed_status
from requests import get

shad_coords = [55.73344116437061, 37.58971106535496]
changed = False
transactions = dict()

id_to_shava = ['Шаурма Классическая культура', 'Шаурма Сырная культура',
               'Шаурма Блэк пеппер', 'Шаурма Паприка барбекю',
               'Шаурма Аля русская', 'Шаурма из мраморной говядины',
               'Шаурма в турецкой лепешке',
               'Шаурма из свиного окорока']

drones = [{
    '#': 1,
    'id': 'Коптер №1'
}, {
    '#': 2,
    'id': 'Коптер №2'
}, {
    '#': 3,
    'id': 'Коптер №3'
}]


class DroneThread(Thread):
    def __init__(self, drone, address):
        self.drone = drone
        self.address = address
        super().__init__()

    def run(self):
        global changed, drones
        sleep(10)
        change_to_completed_status(self.address, int(time()))
        changed = True
        drones.append(self.drone)


def about(request):
    return FileResponse(
        open('static/FCP.pdf', 'rb'),
        content_type='application/pdf')


def get_distance_global(lat1, lon1, lat2, lon2):
    return hypot(lat1 - lat2, lon1 - lon2) * 1.113195e5


def main(request):
    stats = get_stats()

    bg = []

    for s in stats[4]:
        bg.append(list(map(float, s.split(','))))

    data = {
        'count': stats[0],
        'delivered': stats[1],
        'mean_dist': stats[2],
        'food': stats[3],
        'geos': bg
    }

    return render(request, 'main.html', data)


def order(request):
    return render(request, 'order.html')


@csrf_exempt
def drop(request):
    return render(request, 'drop.html', {'shava_id': request.GET['shava_id']})


def calculate(rub):
    req = get(
        'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,RUB')
    return rub / loads(req.text)['RUB']


@csrf_exempt
def pay(request):
    data = dict()
    if request.method == 'GET':
        try:
            data['pgeo'] = request.GET['geo'].split(',')[0][0:5] + ' ' + \
                           request.GET['geo'].split(',')[1][0:5]
            data['geo'] = request.GET['geo']
        except:
            pass
        try:
            if request.GET['type'] == 'straight':
                data['shava_id'] = request.GET['shava_id']
                return render(request, 'pay.html', data)
            elif request.GET['type'] == 'metamask':
                data['geo'] = request.GET['geo']
                data['eth'] = int(calculate(250) * 10e17)  # сколько wei снять
                data['shava_id'] = request.GET['shava_id']
                return render(request, 'away.html', data)
            else:
                return render(request, 'redirect.html',
                              {'geo': request.GET['geo']})
        except:
            pass

        return render(request, 'redirect.html', {'geo': request.GET['geo']})
    elif request.method == 'POST':
        try:
            # Данные для оплаты напрямую
            addr = request.POST['name']
            key = request.POST['key']
            message = request.POST['message']
            shava_id = request.POST['shava_id']
            coords = request.POST['geo']
            geo = list(map(float, request.POST['geo'].split(',')))
            dist = get_distance_global(geo[0], geo[1], shad_coords[0],
                                       shad_coords[1])
            eth = calculate(250)  # сколько эфира снять

            print(addr, key, message, geo, dist, shava_id)
            tx_hash, order = make_transaction(addr, key, eth, coords, int(dist),
                                              shava_id)

            data['completed'] = True
            # data['completed'] = False
            # data['error'] = True
            data['hash'] = tx_hash
            data['order'] = order
            print(tx_hash, order)
        except:
            try:
                data['pgeo'] = request.POST['geo'].split(',')[0][0:5] + ' ' + \
                               request.POST['geo'].split(',')[1][0:5]
                data['geo'] = request.POST['geo']
            except:
                pass
            try:
                if request.POST['type'] == 'straight':
                    data['shava_id'] = request.POST['shava_id']
                    return render(request, 'pay.html', data)
                elif request.POST['type'] == 'metamask':
                    data['geo'] = request.POST['geo']
                    data['eth'] = int(
                        calculate(250) * 10e17)  # сколько wei снять
                    data['shava_id'] = request.POST['shava_id']
                    return render(request, 'away.html', data)
                else:
                    return render(request, 'main.html')
            except:
                pass

            return render(request, 'redirect.html',
                          {'geo': request.POST['geo']})
        return render(request, 'pay.html', data)


@csrf_exempt
def check(request):
    print(request.headers)
    if request.method == 'GET':
        if request.GET.get('adrs') != None:
            data = dict()
            data['post'] = True
            addr = request.GET['adrs']
            data['message'] = 'Ваш заказ почти готов'
            load_data = get_order_info(addr)
            if load_data == 'error':
                data['error'] = True
            else:
                data['error'] = False
                data['shava_id'] = id_to_shava[int(load_data[0])]
                data['delivery_distance'] = '{} метров'.format(
                    str(load_data[1]))
                data['order_time'] = datetime.fromtimestamp(
                    load_data[2]).astimezone(
                    pytz.timezone('Europe/Moscow')).strftime(
                    '%H:%M:%S %Y-%m-%d')
                if load_data[3] != 0:
                    data['delivery_time'] = 'Доставлен в {}'.format(
                        datetime.fromtimestamp(
                            load_data[3]).astimezone(
                            pytz.timezone('Europe/Moscow')).strftime(
                            '%H:%M:%S %Y-%m-%d'))
                else:
                    if load_data[8] == 1:
                        data['delivery_time'] = 'Заказ готовится'
                    else:
                        data['delivery_time'] = 'Заказ доставляется'
                data['estimated_time'] = datetime.fromtimestamp(
                    load_data[4]).astimezone(
                    pytz.timezone('Europe/Moscow')).strftime(
                    '%H:%M:%S %Y-%m-%d')
                data['geo'] = load_data[5]
                data['tx_hash'] = load_data[6]
                data['client'] = load_data[7]
            return render(request, 'check.html', data)

        else:
            return render(request, 'check.html')

    elif request.method == 'POST':
        data = dict()
        data['post'] = True
        addr = request.POST['adrs']
        data['message'] = 'Ваш заказ почти готов'
        load_data = get_order_info(addr)
        if load_data == 'error':
            data['error'] = True
        else:
            data['error'] = False
            data['shava_id'] = id_to_shava[int(load_data[0])]
            data['delivery_distance'] = '{} метров'.format(str(load_data[1]))
            data['order_time'] = datetime.fromtimestamp(
                load_data[2]).astimezone(
                pytz.timezone('Europe/Moscow')).strftime('%H:%M:%S %Y-%m-%d')
            if load_data[3] != 0:
                data['delivery_time'] = 'Доставлен в {}'.format(
                    datetime.fromtimestamp(
                        load_data[3]).astimezone(
                        pytz.timezone('Europe/Moscow')).strftime(
                        '%H:%M:%S %Y-%m-%d'))
            else:
                if load_data[8] == 1:
                    data['delivery_time'] = 'Заказ готовится'
                else:
                    data['delivery_time'] = 'Заказ доставляется'
            data['estimated_time'] = datetime.fromtimestamp(
                load_data[4]).astimezone(
                pytz.timezone('Europe/Moscow')).strftime(
                '%H:%M:%S %Y-%m-%d')

        data['geo'] = load_data[5]
        data['tx_hash'] = load_data[6]
        data['client'] = load_data[7]
    return render(request, 'check.html', data)


@csrf_exempt
def metamask_complited(request):
    global changed
    print('called metamask completed', request.GET['from'], request.GET['hash'])
    _from = request.GET['from']
    _hash = request.GET['hash']
    coords = request.GET['geo']
    geo = list(map(float, request.GET['geo'].split(',')))
    dist = int(
        get_distance_global(geo[0], geo[1], shad_coords[0], shad_coords[1]))
    shava_id = request.GET['shava_id']
    address = add_order(coords, dist, shava_id, _from, str(_hash))
    changed = True
    return JsonResponse({'address': address})


def away(request):
    return render(request, 'away.html')


@csrf_exempt
def confirm(request):
    data = dict()
    data['geo'] = request.GET['geo']
    data['shava_id'] = request.GET['shava_id']
    data['shava_name'] = id_to_shava[int(request.GET['shava_id'])]
    return render(request, 'confirm.html', data)


@csrf_exempt
def shaurman(request):
    global changed, drones
    '''if request.method == 'GET':
        changed = True
    else:'''
    if request.method == 'GET':
        return handler403(request, KeyError)
    if request.POST.get('very_secret_key', False):
        if request.POST['very_secret_key'] == 'jopa':
            changed = True
            return render(request, 'shaurman.html')

    elif request.POST['l'] == 'check':
        return HttpResponse(str(changed))
    elif request.POST['l'] == 'drones':
        data = drones
        return JsonResponse(data, safe=False)
    elif request.POST['l'] == 'orders':
        data = []
        i = 1
        for addr in get_uncompleted_orders():
            z = get_order_info(addr)
            data.append({
                '#': i,
                'order': id_to_shava[z[0]],
                'address': addr,
                'geo': str(list(map(float, z[5].split(','))))[1:-1]
            })
            i += 1
        changed = False
        return JsonResponse(data, safe=False)
    elif request.POST['l'] == 'send':
        change_to_delivery_status(request.POST['address'])
        for d, i in zip(drones, range(0, len(drones))):
            if d['#'] == int(request.POST['sID']):
                dh = DroneThread(d, request.POST['address'])
                drones.pop(i)
                dh.start()
                break

        changed = True
        return HttpResponse('')


def handler404(request, exception):
    response = render(request, "404.html", {'error': '404'})
    response.status_code = 404
    return response


def handler400(request, exception):
    response = render(request, "404.html", {'error': '400'})
    response.status_code = 400
    return response


def handler403(request, exception):
    response = render(request, "404.html", {'error': '403'})
    response.status_code = 403
    return response


def handler500(request):
    response = render(request, "404.html", {'error': '500'})
    response.status_code = 500
    return response
