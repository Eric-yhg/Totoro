from django.shortcuts import render,redirect, HttpResponse,render_to_response,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout,admin
from cmdb import models
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

import json
from . import models
from . import asset_handler


def register(request):
    pass
    return render(request, 'register.html')

def acc_logout(request):
    logout(request)
    return redirect("/accounts/login/")


def User_list(request):
    sas = models.User2.objects.all()
    return render(request, "User.html", {
        'sas': sas
    })

@csrf_exempt
def asset(request):
    """
    通过csrf_exempt装饰器，跳过Django的csrf安全机制，让post的数据能被接收，但这又会带来新的安全问题。
    可以在客户端，使用自定义的认证token，进行身份验证。这部分工作，请根据实际情况，自己进行。
    :param request:
    :return:
    """
    if request.method == "POST":
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        # 各种数据检查，请自行添加和完善！
        if not data:
            return HttpResponse("没有数据！")
        if not issubclass(dict, type(data)):
            return HttpResponse("数据必须为字典格式！")
        # 是否携带了关键的sn号
        sn = data.get('sn', None)
        if sn:
            # 进入审批流程
            # 首先判断是否在上线资产中存在该sn
            asset_obj = models.Asset.objects.filter(sn=sn)
            if asset_obj:
                # 进入已上线资产的数据更新流程
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                return HttpResponse("资产数据已经更新！")
            else:   # 如果已上线资产中没有，那么说明是未批准资产，进入新资产待审批区，更新或者创建资产。
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse("没有资产sn序列号，请检查数据！")

@csrf_exempt
def User_add(request):
    if request.method == "GET":
        return render_to_response('User_add.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        passwd = request.POST.get('passwd')
        sex = request.POST.get('sex')
        jobs = request.POST.get('jobs')
        models.User2.objects.create(name=name, passwd=passwd, sex=sex, jobs=jobs)
        return redirect('User_list')

@csrf_exempt
def User_edit(request,id):
    if request.method == 'GET':
        obj = models.User2.objects.get(id=id)
        return render_to_response('User_edit.html', {'obj': obj})
    elif request.method == 'POST':
        name = request.POST.get('name')
        passwd = request.POST.get('passwd')
        sex = request.POST.get('sex')
        jobs = request.POST.get('jobs')
        models.User2.objects.filter(id=id).update(name=name,passwd=passwd, sex=sex, jobs=jobs)
        return redirect('User_list')

def User_del(request,id):
    if request.method == 'GET':
        models.User2.objects.filter(id=id).delete()
    return redirect('User_list')


def acc_login(request):
    errors = {}
    if request.method == "POST":
        _username = request.POST.get("username")
        _password = request.POST.get("password")
        user = authenticate(username = _username, password = _password)
        if user:
            login(request,user)
            next_url = request.GET.get("next","/")
            return redirect(next_url)
        else:
            errors['error'] = "账户或者密码错误"
    return render(request,"login.html",{"errors":errors})

@login_required
def index(request):

    assets = models.Asset.objects.all()
    return render(request, 'index.html', locals())

@login_required
def dashboard(request):
    total = models.Asset.objects.count()
    upline = models.Asset.objects.filter(status=0).count()
    offline = models.Asset.objects.filter(status=1).count()
    unknown = models.Asset.objects.filter(status=2).count()
    breakdown = models.Asset.objects.filter(status=3).count()
    backup = models.Asset.objects.filter(status=4).count()
    up_rate = round(upline/total*100)
    o_rate = round(offline/total*100)
    un_rate = round(unknown/total*100)
    bd_rate = round(breakdown/total*100)
    bu_rate = round(backup/total*100)
    server_number = models.Server.objects.count()
    networkdevice_number = models.NetworkDevice.objects.count()
    storagedevice_number = models.StorageDevice.objects.count()
    securitydevice_number = models.SecurityDevice.objects.count()
    software_number = models.Software.objects.count()

    return render(request, 'dashboard.html', locals())


def detail(request, asset_id):
    """
    以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。
    :param request:
    :param asset_id:
    :return:
    """
    asset = get_object_or_404(models.Asset, id=asset_id)
    return render(request, 'detail.html', locals())
