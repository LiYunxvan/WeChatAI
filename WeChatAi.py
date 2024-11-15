# coding:utf-8
"""
@Author:https://github.com/LiYunxvan
详细说明请见目录下`README.md`文件
"""
# --------Conf-------- #
prompt = "你的名字叫做[机器人]，你需要回答用户的问题。"  # 提示词
module = "Qwen2:1.5b"  # 所使用的ollama模型
# -------------------- #

import ollama
from wxauto import WeChat
from rich import print
from os import system


def ai_chat(msg):  # ai答复使用ollama的API来调用
    response = ollama.chat(model='WeChatAi', messages=[
        {
            'role': 'user',
            'content': msg,
        },
    ])
    return response['message']['content']


# 创建Ai模型,调用时用"WeChatAi"
def create_ai():
    modelfile = f'''
    FROM {module}
    SYSTEM {prompt}。
    '''
    ollama.create(model='WeChatAi', modelfile=modelfile)


# ollama.create(model='WeChatAi', modelfile=modelfile)

if __name__ == '__main__':
    create_ai()
    who = input("请选择接入人/群名称:")
    if who == '':
        print("[red]不是一个有效的名称！[/red]")
    # 创建拒绝回复列表
    NOT_CHAT = ["[图片]", "[视频]", "[语音]", "[文件]", "[动画表情]", "[位置]", "[视频通话]", "[语音通话]",
                '[微笑]', '[撇嘴]', '[色]', '[发呆]', '[得意]', '[流泪]', '[害羞]', '[闭嘴]', '[睡]', '[大哭]',
                '[尴尬]', '[发怒]', '[调皮]', '[呲牙]', '[惊讶]', '[难过]', '[囧]', '[抓狂]', '[吐]', '[偷笑]',
                '[愉快]', '[白眼]', '[傲慢]', '[困]', '[惊恐]', '[憨笑]', '[悠闲]', '[咒骂]', '[疑问]', '[嘘]', '[晕]',
                '[衰]', '[骷髅]', '[敲打]', '[再见]', '[擦汗]', '[抠鼻]', '[鼓掌]', '[坏笑]', '[左哼哼]', '[鄙视]']

    wx = WeChat()  # 打开微信
    # wx.SendMsg("[人机已登录]")
    long = 0
    msgs = wx.GetAllMessage()  # 获取消息
    while True:
        if wx.GetAllMessage() != msgs:
            if long >= 15:
                long = 0
                system("cls")
            long += 1
            msgs = wx.GetAllMessage()
            if msgs[-1].type == "friend":  # 他人发的
                print(f"[red]{msgs[-1].content}[/red]")
            elif msgs[-1].type == "self":  # 自己发的
                print(f"[green]{msgs[-1].content}[/green]")
            else:  # 其他消息（如系统消息）
                print(f"[blue]{msgs[-1].content}[/blue]")
            if msgs and msgs[-1].type == "friend":  # 判断一下是不是人发的
                if msgs[-1].content == NOT_CHAT:
                    wx.SendMsg(f"[人机] (暂不支持此类型的消息)“{msgs[-1].content}”")
                else:
                    wx.SendMsg(f"[人机] {ai_chat(msgs[-1].content)}")
