import hashlib
import json
import time

from django.shortcuts import render, HttpResponse
from repository import models

# Create your views here.

key_record = {
    # "548aa8aeb09db415d168b1010016a38c" : 123123143.123
}


def asset(request):
    if request.method == 'GET':
        server_token = "vdgsavhdsbhafbsdbfhbdshfbsd"
        server_time = time.time()
        client_md5_header = request.META.get('HTTP_TOKEN')
        if client_md5_header == None:
            return HttpResponse('没有权限')
        client_md5_token, client_time = client_md5_header.split('|')
        client_time = float(client_time)

        if server_time - client_time > 10:
            return HttpResponse('[第一关] 小伙子, 时间太久了.....')

        tmp = "%s|%s" % (server_token, client_time)
        m = hashlib.md5()
        m.update(bytes(tmp, encoding='utf-8'))
        server_md5_token = m.hexdigest()

        if server_md5_token != client_md5_token:
            return HttpResponse('[第二关] 你是不是修改了token')

        for k in list(key_record.keys()):
            if server_time > key_record[k]:
                del key_record[k]

        if client_md5_token in key_record:
            return HttpResponse('[第三关] 已经被别人访问过了')
        else:
            key_record[client_md5_token] = client_time + 10

        return HttpResponse('ok')

    elif request.method == 'POST':
        res = request.body
        new_server_info = json.loads(res)
        # print(new_server_info)

        hostname = new_server_info['basic']['data']['hostname']

        old_server_obj = models.Server.objects.filter(hostname=hostname).first()
        # print(old_server_obj)

        if not old_server_obj:
            return HttpResponse('该资产并未录入...')

        # 开始清理  disk  memory  nic  board
        if new_server_info['disk']['status'] != 10000:
            models.ErrorLog.objects.create(asset_obj=old_server_obj, title="(%s)的硬盘采集出错了" % hostname,
                                           content=new_server_info['disk']['data'])

        # memory {'DIMM #0': {'capacity': 1024, 'slot': 'DIMM #0', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #1': {'capacity': 0, 'slot': 'DIMM #1', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #2': {'capacity': 0, 'slot': 'DIMM #2', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #3': {'capacity': 0, 'slot': 'DIMM #3', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #4': {'capacity': 0, 'slot': 'DIMM #4', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #5': {'capacity': 0, 'slot': 'DIMM #5', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #6': {'capacity': 0, 'slot': 'DIMM #6', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'DIMM #7': {'capacity': 0, 'slot': 'DIMM #7', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}}}
        # old [4,5,6]
        # new [4,5,7]
        '''
        new_disk_info
           '0': 
               {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}, 
           '1': 
               {'slot': '1', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'}, 
           '2': 
               {'slot': '2', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'}, 
        '''
        '''
        old_disk_info
           [
               Disk(slot=0, model),
               Disk(slot=1, model),
           ]
        '''
        old_disk_info = models.Disk.objects.filter(server_obj=old_server_obj)
        new_disk_info = new_server_info['disk']['data']

        # print(new_disk_info)

        # [0,1,2,3,4,5]
        new_slot_list = list(new_disk_info.keys())
        old_slot_list = []
        for v in old_disk_info:
            old_slot_list.append(v.slot)

        '''
         new_slot_list: [1,2,3]
         old_slot_list: [1,2,4]
        '''
        # 1.增加的slot
        add_slot_list = set(new_slot_list).difference(set(old_slot_list))
        print(add_slot_list)

        if add_slot_list:
            # disk_res = {}
            recoder_list = []
            for v in add_slot_list:
                # {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}
                disk_res = new_disk_info[v]
                tmp = "增加磁盘槽位{slot}, 类型{pd_type}, 容量{capacity}, 型号{model}".format(**disk_res)
                disk_res['server_obj'] = old_server_obj
                models.Disk.objects.create(**disk_res)
                recoder_list.append(tmp)

            recoder_str = ";".join(recoder_list)
            models.AssetRecord.objects.create(asset_obj=old_server_obj, content=recoder_str)

        # 2. 删除的slot
        del_slot_list = set(old_slot_list).difference(set(new_slot_list))
        print(del_slot_list)
        # delete from disk where slot in (2,3,4)
        if del_slot_list:
            # for slot in del_slot_list:
            models.Disk.objects.filter(slot__in=del_slot_list, server_obj=old_server_obj).delete()

            del_str = "删除的槽位是%s" % (";".join(del_slot_list))
            models.AssetRecord.objects.create(asset_obj=old_server_obj, content=del_str)

        # 3. 更新的slot
        up_slot_list = set(old_slot_list).intersection(set(new_slot_list))
        print(up_slot_list)

        if up_slot_list:
            recoder_list = []
            for slot in up_slot_list:
                old_disk_row = models.Disk.objects.filter(slot=slot, server_obj=old_server_obj).first()  # [disk(slot)]
                # {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}
                new_disk_row = new_disk_info[slot]
                for k, new_v in new_disk_row.items():
                    '''
                    k: slot, pd_type, model
                    new_v: SAS
                    '''
                    old_v = getattr(old_disk_row, k)
                    if old_v != new_v:
                        tmp = "槽位:%s, %s由%s更改为%s" % (slot, k, old_v, new_v)
                        recoder_list.append(tmp)
                        setattr(old_disk_row, k, new_v)
                old_disk_row.save()

            if recoder_list:
                models.AssetRecord.objects.create(asset_obj=old_server_obj, content=";".join(recoder_list))

    return HttpResponse('ok')
