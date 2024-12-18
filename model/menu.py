# -*- coding: utf-8 -*-
# filename: menu.py
import requests
import json
from common.access import AccessTokenManager

class Menu(object):
    def __init__(self):
        self.base_url = "https://api.weixin.qq.com/cgi-bin/menu/"

    # 创建菜单
    def create(self, postData, accessToken):
        postUrl = f"{self.base_url}/create?access_token={accessToken}"
        # 确保 postData 是 UTF-8 编码的字符串（Python 3 中字符串默认就是 UTF-8）
        if isinstance(postData, str):
            postData = postData.encode('utf-8')
        response = requests.post(postUrl, data=postData)
        print(response.text)

    # 查询菜单
    def query(self, accessToken):
        postUrl = f"{self.base_url}/get?access_token={accessToken}"
        response = requests.get(postUrl)
        print(response.text)

    # 删除菜单
    def delete(self, accessToken):
        postUrl = f"{self.base_url}/delete?access_token={accessToken}"
        response = requests.get(postUrl)
        print(response.text)

    # 获取当前自定义菜单配置
    def get_current_selfmenu_info(self, accessToken):
        postUrl = f"https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token={accessToken}"
        response = requests.get(postUrl)
        print(response.text)

if __name__ == '__main__':
    myMenu = Menu()
    postJson = """
    {
        "button":
        [
            {
                "type": "click",
                "name": "开发指引",
                "key":  "mpGuide"
            },
            {
                "name": "公众平台",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "更新公告",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "接口权限说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "返回码说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
                    }
                ]
            },
            {
                "type": "media_id",
                "name": "旅行",
                "media_id": "z2zOokJvlzCXXNhSjF46gdx6rSghwX2xOD5GUV9nbX4"
            }
          ]
    }
    """
    accessToken = AccessTokenManager.get_access_token()
    # 删除现有菜单
    # myMenu.delete(accessToken)
    # 创建菜单
    myMenu.create(postJson, accessToken)