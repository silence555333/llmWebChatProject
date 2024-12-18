# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import logging  as log

from llmmodel.gptmodel import gpt_35_api
from model import receive, reply



class Handle:
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"

            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "thisisfernyangfei"  # 请按照公众平台官网\基本配置中信息填写

            # 将 token, timestamp 和 nonce 排序
            param_list = [token, timestamp, nonce]
            param_list.sort()

            # 创建 sha1 对象并更新哈希值
            sha1 = hashlib.sha1()
            sha1.update("".join(param_list).encode("utf-8"))
            hashcode = sha1.hexdigest()

            print("handle/GET func: hashcode, signature: ", hashcode, signature)

            # 校验 hashcode 是否匹配 signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return str(Argument)

    def POST(self):
        try:
            log.info("收到 POST 请求")
            # 获取网页数据
            webData = web.data() # Python 3 需要 decode 字节流为字符串
            log.info(f"打印从公众号接收到的用户请求数据{webData}")
            # 解析 XML 数据
            recMsg = receive.parse_xml(webData)

            if recMsg is None:
                raise ValueError("解析 XML 返回 None，无法处理")

            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                from_user_content = recMsg.Content
                # 消息类型处理
                if recMsg.MsgType == 'text':
                    log.info(f"接收的消息类型为text，先返回用户发送的消息内容本身")
                    # 替换为使用gpt3.5来回复
                    messages = [{'role': 'user', 'content': from_user_content}, ]
                    # log.info(f"收到的用户消息内容为: {messages}")
                    content = gpt_35_api(messages)
                    # content = from_user_content
                    reply_msg = reply.TextMsg(toUser, fromUser, content)
                    print(content)
                    log.info(f"接收到用户发送的文本消息 {content}")
                    return reply_msg.send()
                if recMsg.MsgType == 'image':
                    media_id = recMsg.MediaId
                    reply_msg = reply.ImageMsg(toUser, fromUser, media_id)
                    log.info(f"接收到图片消息，回复 MediaId: {media_id}")
                    return reply_msg.send()
                #接受语音消息
                if recMsg.MsgType == 'MediaId':
                    recognition = recMsg.Recognition  # 用户的语音识别内容
                    reply_msg = reply.TextMsg(toUser, fromUser, f"你说的是: {recognition}")
                    log.info(f"接收到语音消息，识别内容: {recognition}")
                    return reply_msg.send()

            if isinstance(recMsg, receive.EventMsg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.Event == 'CLICK':
                    if recMsg.Eventkey == 'mpGuide':
                        content = "编写中，尚未完成"  # Python 3 中默认是 Unicode 字符串
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        return replyMsg.send()

            print("暂且不处理")
            return reply.Msg().send()
        except KeyError as e:
            log.error(f"字段缺失错误: {e}")
            return str(e)
        except Exception as e:
            log.error(f"POST 请求处理异常: {e}")
            return str(e)




