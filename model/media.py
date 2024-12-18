# -*- coding: utf-8 -*-
# filename: media.py
import urllib.request
import json

import requests
from common.access import AccessTokenManager


class Media(object):
    def __init__(self):
        pass

    # 上传图片
    def upload(self, accessToken, filePath, mediaType):
        """
          上传图片 临时资源
          :param now_month 当前月
          :return:data_str 当前月的上个月
          """
        with open(filePath, 'rb') as openFile:
            url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={accessToken}&type={mediaType}"
            files = {'media': openFile}
            response = requests.post(url, files=files)

            if response.status_code == 200:
                print("Upload successful:", response.json())
            else:
                print("Failed to upload:", response.status_code, response.text)

    def get(self, accessToken, mediaId):
        """
        获取照片
        """
        postUrl = f"https://api.weixin.qq.com/cgi-bin/media/get?access_token={accessToken}&media_id={mediaId}"

        # Open the URL and read the response
        with urllib.request.urlopen(postUrl) as urlResp:
            headers = urlResp.getheaders()

            # Check the Content-Type
            if any('Content-Type' in header and ('application/json' in header[1] or 'text/plain' in header[1]) for
                   header in headers):
                jsonDict = json.loads(urlResp.read().decode('utf-8'))
                print(jsonDict)
            else:
                # Get the media file (binary data)
                buffer = urlResp.read()

                # Save the media as a file
                with open("test_media.jpg", "wb") as mediaFile:
                    mediaFile.write(buffer)

                print("get successful")



if __name__ == '__main__':
    myMedia = Media()
    accessToken = AccessTokenManager.get_access_token()  # Assume you have this method implemented
    filePath = "D:/code/mpGuide/media/test.jpg"  # Please update with your actual path
    mediaType = "image"
    myMedia.upload(accessToken, filePath, mediaType)
    # 获取照片
    myMedia = Media()
    accessToken = AccessTokenManager.get_access_token()
    mediaId = "2ZsPnDj9XIQlGfws31MUfR5Iuz-rcn7F6LkX3NRCsw7nDpg2268e-dbGB67WWM-N"
    myMedia.get(accessToken, mediaId)