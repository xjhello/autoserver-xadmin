from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from repository import models
# Create your views here.

from rest_framework import serializers






def server(request):
    # print(request.body)
    return render(request, 'server.html')
    # return render(request, 'index_bak.html')


def ajax_server(request):

    table_config = [
        {
            "field": 'id',
            "title": 'id',
        },
        {
            "field": 'hostname',
            "title": '主机名',
        },
        {
            "field": 'sn',
            "title": 'sn号',
        }
    ]
    filed_list = []
    for v in table_config:
        filed_list.append(v['field'])

    server_list = models.Server.objects.values(*filed_list)
    total = models.Server.objects.count()
    # select count(*) from server;
    ret = {
        'total': total,
        'rows': list(server_list),
    }
    return JsonResponse(ret, safe=False)



def asset(request):
    return render(request, 'asset.html')


def ajax_asset(request):

    table_config = [
        {
            "field": 'id',
            "title": 'id',
        },
        {
            "field": 'cabinet_num',
            "title": '机柜号',
        },
        {
            "field": 'cabinet_order',
            "title": '序号',
        }
    ]
    filed_list = []
    for v in table_config:
        filed_list.append(v['field'])


    res = models.Server.objects.values(*filed_list)
    print(res)
    ret = {
        'table_config': table_config,
        'data_list': list(res)
    }
    return JsonResponse(ret, safe=False)


def modify(request):
    print(request.POST.getlist('ids'))

    return HttpResponse('ok')

