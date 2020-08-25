import requests


def msg_robot(message, robot_Key):
    """
    企业微信机器人发送消息
    :param robot_Key: 机器人key
    :param message:消息内容
    :return:
    """
    headers = {"Content-Type": "text/plain"}
    data = {
        "msgtype": "markdown",  # 消息类型，此时固定为markdown
        "markdown": {
            "content": "# **%s环境后台api发布！自动化测试完成**\n" % (
                message.get('host_name')) +  # 标题 （支持1至6级标题，注意#与文字中间要有空格）
                       "#### **请相关同事注意，及时跟进！**\n" +  # 加粗：**需要加粗的字**
                       "> 发布模块：<font color=\"error\">%s</font> \n" % (message.get('project')) +  # 引用：> 需要引用的文字
                       "> 总用例数：<font color=\"info\">%s</font> \n" % (message.get('test_all')) +  # 引用：> 需要引用的文字
                       "> 成功数：<font color=\"info\">%s</font> \n" % (message.get('test_Pass')) +  # 引用：> 需要引用的文字
                       "> 失败数：<font color=\"warning\">%s</font> \n" % (message.get('test_fail')) +  # 引用：> 需要引用的文字
                       "> 错误数：<font color=\"warning\">%s</font> \n" % (message.get('test_Error')) +  # 引用：> 需要引用的文字
                       "> 成功率：<font color=\"error\">%s</font> \n" % (message.get('success_rate')) +  # 字体颜色(只支持3种内置颜色)
                       "[本次测试结果详情:%s](http://autotest.lrts.me/test_report/%s) \n" % (
                           message.get('report_name'), message.get('report_name')) +
                       "[近10测试结果](http://autotest.lrts.me/test_report_list10/) \n"  # 绿色：info、灰色：comment、橙红：warning
                       # "<@caozhuo> <@caozhuo>\n"
        }
    }
    ret = requests.post(
        url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + robot_Key,
        headers=headers,
        json=data
    )
    print(ret.text)
