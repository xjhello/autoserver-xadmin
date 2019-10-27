import xadmin

from repository import models

from xadmin import views

# 全局修改，固定写法
class GlobalSettings(object):
    # 修改title
    site_title = 'xxx后台管理界面'
    # 修改footer
    site_footer = 'xxx的公司'
    # 收起菜单
    menu_style = 'accordion'

    global_search_models = [models.Disk, models.Server]
    global_models_icon = {
        models.Server: "fa fa-linux", models.Disk: "fa fa-cloud", models.UserProfile: "fa fa-user"
    }

    # global_models_icon = {
    #     V_UserInfo: "glyphicon glyphicon-user", UserDistrict: "fa fa-cloud"
    # }  # 设置models的全局图标

# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView,GlobalSettings)


# 创建xadmin的最基本管理器配置，并与view绑定
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True

# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView,BaseSetting)



class UserProfileAdmin(object):
    list_display = ['id','name' ,'email','phone','mobile']

    search_fields = ['id', 'name', 'email', 'phone']
    list_editable = ['name' ,'email','phone','mobile']
    # list_filter = ['name' ,'email','phone','mobile']
    # list_filter = ['oid','user' ,'odate','oisPay','ototal','oadress']
    show_bookmarks = False



class UserGroupAdmin(object):
    list_display = ['id', 'name', 'users']

    search_fields = ['id', 'name', 'users']
    list_editable = ['name', ]

    # data_charts = {
    #     "user_count": {'title': u"用户分布", "x-field": "name", "y-field": ("id",),},
    #     # "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)}
    # }
    show_detail_fields = ['name']



xadmin.site.register(models.UserProfile,UserProfileAdmin)
xadmin.site.register(models.UserGroup,UserGroupAdmin)
