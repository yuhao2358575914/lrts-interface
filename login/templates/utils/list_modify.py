def list_Duplicate_remove(list):
    """
    对输入的列表进行去重
    """
    news_list = []
    for i in list:
        if i not in news_list:
            news_list.append(i)
    return news_list