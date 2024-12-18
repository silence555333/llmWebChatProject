import json
import urllib.request
import urllib.error
import requests
from common.access import AccessTokenManager

class Material(object):
    def __init__(self):
        # Base URL for WeChat API (common for all material-related requests)
        self.base_url = "https://api.weixin.qq.com/cgi-bin/material"



    def add_news(self, accessToken, news):
        """
        Add a new article/news to WeChat's media library.

        Args:
           将一篇新的图文文章添加到微信的永久素材库。
	•	  news 参数应该是一个包含文章数据（例如标题、内容、封面图片媒体 ID）的 JSON 字符串
        """
        postUrl = f"{self.base_url}/add_news?access_token={accessToken}"
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = news.encode('utf-8')

        try:
            request = urllib.request.Request(postUrl, data=data, headers=headers, method='POST')
            with urllib.request.urlopen(request) as urlResp:
                response = urlResp.read()
                print(response.decode('utf-8'))
        except urllib.error.HTTPError as e:
            print(f"HTTPError: {e.code}, {e.reason}")
        except urllib.error.URLError as e:
            print(f"URLError: {e.reason}")

    # 上传素材
    def upload(self, accessToken, filePath, mediaType):
        with open(filePath, "rb") as openFile:
            files = {'media': openFile}
            postUrl = f"{self.base_url}/add_material?access_token={accessToken}&type={mediaType}"
            response = requests.post(postUrl, files=files)
            print(response.json())
     # 下载素材
    def get(self, accessToken, mediaId):
        postUrl = f"{self.base_url}/get_material?access_token={accessToken}"
        postData = json.dumps({"media_id": mediaId})
        response = requests.post(postUrl, data=postData)
        if response.headers['Content-Type'].startswith('application/json') or response.headers[
            'Content-Type'].startswith('text/plain'):
            print(response.json())  # 打印 JSON 响应
        else:
            with open('test_media.jpg', 'wb') as mediaFile:
                mediaFile.write(response.content)  # 写入素材的二进制内容
            print("get successful")
     # 删除素材
    def delete(self, accessToken, mediaId):
        postUrl = f"{self.base_url}/del_material?access_token={accessToken}"
        postData = json.dumps({"media_id": mediaId})
        response = requests.post(postUrl, data=postData)
        print(response.json())
        # 获取素材列表

    def batch_get(self, accessToken, mediaType, offset=0, count=20):
        postUrl = f"{self.base_url}/batchget_material?access_token={accessToken}"
        postData = json.dumps({
            "type": mediaType,
            "offset": offset,
            "count": count
        })
        response = requests.post(postUrl, data=postData)
        print(response.json())



if __name__ == '__main__':
    myMaterial = Material()
    accessToken = AccessTokenManager.get_access_token()

    # Example for adding a news article
    news = {
        "articles": [
            {
                "title": "New Article",
                "thumb_media_id": "media_id_for_thumb",
                "author": "Author Name",
                "digest": "Article summary",
                "show_cover_pic": 1,
                "content": "<p>Article content with HTML tags</p>",
                "content_source_url": "https://example.com"
            }
        ]
    }

    # Convert news to JSON string
    news_json = json.dumps(news, ensure_ascii=False)

    # Add a new news article
    myMaterial.add_news(accessToken, news_json)

    # Example for getting a media file by its media ID
    media_id = 'media_id_for_existing_media'
    myMaterial.get(accessToken, media_id)

    # Example for deleting a material by media ID
    myMaterial.delete(accessToken, media_id)

    # Example for updating a news article
    updated_news = {
        "articles": [
            {
                "title": "Updated Article Title",
                "thumb_media_id": "new_media_id_for_thumb",
                "author": "Updated Author",
                "digest": "Updated article summary",
                "show_cover_pic": 1,
                "content": "<p>Updated content with new HTML tags</p>",
                "content_source_url": "https://updated-example.com"
            }
        ]
    }
    myMaterial.update_news(accessToken, media_id, updated_news)
    mediaType = "news"
    myMaterial.batch_get(accessToken, mediaType)
