
def init_Substract_rules(N):
    """
    获取N个满减额度
    :param N:
    :return:
    """
    subtractRule = [{"limitFee": 1000, "subtractFee": 100, "showOrder": 1},
                    {"limitFee": 1200, "subtractFee": 200, "showOrder": 2},
                    {"limitFee": 1300, "subtractFee": 300, "showOrder": 3},
                    {"limitFee": 1400, "subtractFee": 400, "showOrder": 4},
                    {"limitFee": 1500, "subtractFee": 500, "showOrder": 5},
                    {"limitFee": 1600, "subtractFee": 600, "showOrder": 6}
                    ]
    subtractRuleNew = []
    if N < len(subtractRule):
        for i in range(N):
            subtractRuleNew.append(subtractRule[i])
        return subtractRuleNew
    else:
        return '"%d"越界了'%N