import os
import time
import requests
from threading import Lock

class AccessTokenManager:
    def __init__(self):
        # 从系统环境变量中读取 app_id 和 app_secret
        self.app_id = os.getenv("WX_APP_ID")
        self.app_secret = os.getenv("WX_APP_SECRET")

        if not self.app_id or not self.app_secret:
            raise ValueError("未找到系统变量 WX_APP_ID 或 WX_APP_SECRET，请确保已正确配置")

        self.access_token = None
        self.expires_at = 0  # 过期时间戳
        self.lock = Lock()  # 线程锁，防止多线程并发刷新

    def get_access_token(self):
        """获取有效的 accessToken"""
        # 检查是否需要刷新
        if self.is_token_valid():
            return self.access_token

        # 加锁防止重复刷新
        with self.lock:
            # 再次检查是否其他线程已刷新
            if self.is_token_valid():
                return self.access_token

            # 刷新 accessToken
            self.refresh_access_token()

        return self.access_token

    def is_token_valid(self):
        """检查 accessToken 是否有效"""
        return self.access_token and time.time() < self.expires_at - 300  # 提前 5 分钟刷新

    def refresh_access_token(self):
        """刷新 accessToken"""
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "access_token" in data:
                self.access_token = data["access_token"]
                self.expires_at = time.time() + data["expires_in"]
                print(f"成功刷新 accessToken: {self.access_token}")
            else:
                print(f"刷新 accessToken 失败，错误信息: {data}")
        except requests.exceptions.RequestException as e:
            print(f"请求 accessToken 接口失败: {e}")