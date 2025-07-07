import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from wxcloudrun.models import Counters


from django.views.decorators.csrf import csrf_exempt  # 前端跨域时关闭 CSRF 校验
from django.views import View
from .models import User
from django.utils.decorators import method_decorator  # 用于类视图
@csrf_exempt  # 生产环境建议用更安全的跨域方案（如 CORS 中间件）
def get_latest_device_data(request):
    if request.method == "GET":
        # 获取最新一条数据（按时间戳倒序）
        try:
            latest_data = DeviceData.objects.order_by("-timestamp").first()
            if latest_data:
                # 构造返回数据
                data = {
                    "device_id": latest_data.device_id,
                    "timestamp": latest_data.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "temperature": latest_data.temperature,
                    "humidity": latest_data.humidity,
                    "is_alert": latest_data.temperature > 30 or latest_data.humidity > 80,
                }
                return JsonResponse({"code": 200, "data": data})
            else:
                return JsonResponse({"code": 404, "msg": "无设备数据"})
        except Exception as e:
            return JsonResponse({"code": 500, "msg": f"数据库错误：{str(e)}"})
    return JsonResponse({"code": 405, "msg": "仅支持 GET 请求"})


# 对类视图关闭 CSRF 验证
@method_decorator(csrf_exempt, name='dispatch')
class WechatLoginView(View):
    def post(self, request):
        # 原有登录逻辑不变...
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"code": 400, "msg": "请输入账号和密码"})

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({"code": 401, "msg": "账号不存在"})

            if user.check_password(password):
                return JsonResponse({
                    "code": 200,
                    "msg": "登录成功",
                    "data": {"username": user.username, "user_id": user.id}
                })
            else:
                return JsonResponse({"code": 401, "msg": "密码错误"})

        except Exception as e:
            return JsonResponse({"code": 500, "msg": f"服务器错误：{str(e)}"})
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DeviceData
import json
from datetime import datetime

@csrf_exempt
def get_device_history(request):
    if request.method == "GET":
        try:
            # 按时间倒序取最近 10 条数据（可根据需求调整数量）
            history_data = DeviceData.objects.order_by("-timestamp")[:6]
            data_list = []
            for item in history_data:
                data_list.append({
                    "device_id": item.device_id,
                    "timestamp": item.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "temperature": item.temperature,
                    "humidity": item.humidity,
                    "is_alert": item.temperature > 30 or item.humidity > 80,
                })
            return JsonResponse({"code": 200, "data": data_list})
        except Exception as e:
            return JsonResponse({"code": 500, "msg": f"数据库错误：{str(e)}"})
    return JsonResponse({"code": 405, "msg": "仅支持 GET 请求"})
