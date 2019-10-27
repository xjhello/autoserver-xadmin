import xadmin

from repository import models


class DiskAdmin(object):
    list_display = ['id','slot' ,'model','capacity','pd_type','server_obj']

    search_fields = ['id', 'slot' ,'model','capacity','pd_type']
    # list_editable = ['name' ,'email','phone','mobile']
    # list_filter = ['name' ,'email','phone','mobile']
    # list_filter = ['oid','user' ,'odate','oisPay','ototal','oadress']

class ServerAdmin(object):
    list_display = ['id', 'device_type_id', 'device_status_id', 'idc', 'business_unit', 'hostname', 'create_at']

    show_detail_fields = ['hostname']
    # search_fields = ['id', 'slot', 'model', 'capacity', 'pd_type']
    # data_charts = {
    #     "user_count": {'title': u"服务器分布", "x-field": "idc", "y-field": ("business_unit",),},
    #     # "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)}
    # }
    # list_per_page = 2
    data_charts = {
        "host_service_type_counts": {
            'title': '部门机器使用情况',
            'x-field': "business_unit",
            'y-field': ("business_unit"),
            'option': {
                "series": {"bars": {"align": "center", "barWidth": 0.8, "show": True}},
                "xaxis": {"aggregate": "count", "mode": "categories"}
            },
        },
        "host_idc_counts": {
            'title': '机房统计',
            'x-field': "idc",
            'y-field': ("idc",),
            'option': {
                "series": {"bars": {"align": "center", "barWidth": 0.3, "show": True}},
                "xaxis": {"aggregate": "count", "mode": "categories"}
            }
        }
    }


class IDCAdmin(object):
    list_display = ['id', 'name', 'floor']

    show_detail_fields = ['name']
    # search_fields = ['id', 'slot', 'model', 'capacity', 'pd_type']


xadmin.site.register(models.Disk,DiskAdmin)
xadmin.site.register(models.Server,ServerAdmin)
xadmin.site.register(models.IDC,IDCAdmin)
