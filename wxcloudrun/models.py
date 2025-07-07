from datetime import datetime
from django.db import models

from django.contrib.auth.hashers import make_password, check_password
class DeviceData(models.Model):
    device_id = models.CharField(max_length=64, verbose_name="设备号")
    timestamp = models.DateTimeField(verbose_name="时间戳")
    temperature = models.FloatField(verbose_name="温度")
    humidity = models.FloatField(verbose_name="湿度")

    class Meta:
        db_table = "device_history"  # 替换为实际表名
        verbose_name = "设备数据"
        verbose_name_plural = verbose_name



# 用户模型（取消密码加密）
class User(models.Model):
    username = models.CharField(max_length=50, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=128, verbose_name="密码")  # 直接存储明文密码
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def set_password(self, raw_password):
        """直接存储明文密码（不加密）"""
        self.password = raw_password  # 取消加密，直接赋值

    def check_password(self, raw_password):
        """直接比对明文密码"""
        return self.password == raw_password  # 简单字符串比对

    class Meta:
        db_table = 'users'  # 对应数据库表名
        verbose_name = "用户"
        verbose_name_plural = "用户"
