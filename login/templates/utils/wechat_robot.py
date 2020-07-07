import requests


def msg_robot(message, robot_Key):
    """
    企业微信机器人发送消息
    :param message:消息内容
    :param url:发送消息到指定的群url
    :return:
    """
    headers = {"Content-Type": "text/plain"}
    # message = "测试环境：{}已经发布api，用例通过率：".format({str(message)})
    if message['envId'] == '4':
        host_names = '地球'
    elif message['envId'] == '3':
        host_names = '月亮'
    elif message['envId'] == '5':
        host_names = '火星'
    data = {
        "msgtype": "markdown",  # 消息类型，此时固定为markdown
        "markdown": {
            "content": "# **%s环境后台api发布！自动化测试完成。**\n" % (
                host_names) +  # 标题 （支持1至6级标题，注意#与文字中间要有空格）
                       "#### **请相关同事注意，及时跟进！**\n" +  # 加粗：**需要加粗的字**
                       "> 总用例数：<font color=\"info\">%s</font> \n" % (message.get('test_all')) +  # 引用：> 需要引用的文字
                       "> 成功数：<font color=\"info\">%s</font> \n" % (message.get('test_Pass')) +  # 引用：> 需要引用的文字
                       "> 失败数：<font color=\"warning\">%s</font> \n" % (message.get('test_fail')) +  # 引用：> 需要引用的文字
                       "> 错误数：<font color=\"warning\">%s</font> \n" % (message.get('test_Error')) +  # 引用：> 需要引用的文字
                       "> 成功率：<font color=\"error\">%s</font> \n" % (message.get('success_rate')) +  # 字体颜色(只支持3种内置颜色)
                       "[本次测试结果详情:%s](http://autotest.lrts.me/test_report/%s)" % (message.get('report_name'),message.get('report_name'))
            # 绿色：info、灰色：comment、橙红：warning
        }
    }
    ret = requests.post(
        url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="+robot_Key,
        headers=headers,
        json=data
    )
    print(ret.text)

