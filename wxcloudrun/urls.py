"""wxcloudrun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from wxcloudrun import views
from django.conf.urls import url

urlpatterns = (
    path('api/wechat-login/', WechatLoginView.as_view(), name="wechat-login"),
    //path('admin/', admin.site.urls),
    # 设备数据接口（保持不变）
    path('api/device/latest/', get_latest_device_data, name="get_latest_device_data"),
    # 包含应用的所有路由（关键：应用路由会自动拼接在根路径后）
    path('', include('humAndtem.urls')),
    # 新增接口：获取历史数据（方案1）
    path('api/device/history/', get_device_history, name='get_device_history'),
)
