class Const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const value!")
        if not name.isupper():
            raise self.ConstCaseError('const "%s" is not all letters are capitalized' % name)
        self.__dict__[name] = value


import sys

sys.modules[__name__] = Const()
"""
首页模块推荐类型
"""
# 听单
Const.srcEntityType_collection = '5'
# 榜单
Const.srcEntityType_ranking = '42'
# 专题
Const.srcEntityType_topic = '8'
# 书籍分类
Const.srcEntityType_book = '9'
# 节目分类
Const.srcEntityType_albumn = '10'
# 热门主播
Const.srcEntityType_hotanounce = '11'
# 热门节目
Const.srcEntityType_hotalbumn = '13'
# 精品首发
Const.srcEntityType_boutique = '38'
# 付费精品
Const.srcEntityType_chargeboutique = '40'
# 付费分类
Const.srcEntityType_chargeType = '41'
# 限免阅读
Const.srcEntityType_limitRead = '61'
# 限免收听
Const.srcEntityType_limitListen = '62'
# 小编推荐
Const.srcEntityType_editorRec = '66'
# 新书推荐
Const.srcEntityType_newBookRec = '67'
# 标签
Const.srcEntityType_tag = '81'
# 标签类别筛选页
Const.srcEntityType_tagFilter = '89'
# 猜你想听
Const.srcEntityType_guessyoulike = '83'
# 满减
Const.srcEntityType_Fullreduction = '128'
# 听友会
Const.srcEntityType_listenFriendMeeting = '12'
# 购书折扣
Const.srcEntityType_buyBookDiscount = '129'
# 横幅推荐
Const.srcEntityType_ADVERT_RECOMMEND = '140'
"""
首页推荐模块展示样式

"""
# 横向
Const.showStyle_landscape = 1
# 纵向
Const.showStyle_portrait = 2
# 横3
Const.showStyle_landscape_3 = 3
# 横3可滑
Const.showStyle_landscape3_slide = 4
# 横1可滑
Const.showStyle_landscape1_slide = 5
# 3+3
Const.showStyle_landscape_3plus3 = 6
# 1+4
Const.showStyle_landscape_1plus4 = 7
# 1+4（小4）
Const.showStyle_landscape_1plus4_less = 8
# 4+4
Const.showStyle_landscape_4plus4 = 9
# 单个听单
Const.showStyle_single = 10
# 多个听单
Const.showStyle_multiple = 11
# 横排可滑动
Const.showStyle_lineup_slide = 12
# 横向重点(可滑）
Const.showStyle_landscape_important_slide = 13
# 横向可滑
Const.showStyle_landscape_slide = 14
# 单个榜单
Const.showStyle_single_list = 15
# 多个榜单
Const.showStyle_multiple_list = 16
# 多个营销活动
Const.showStyle_multiple_activity = 17
# 横向（可滑动带按钮）
Const.showStyle_crosswise_slide_button = 18
# 单个营销活动
Const.showStyle_single_activity = 19

"""
活动添加资源类型
"""
# 书籍资源类型
Const.resourceType_book = 1
# 节目资源类型
Const.resourceType_albumn = 2
# 节目资源类型
Const.resourceType_readBook = 3
"""
活动范围类型
"""
# 指定全部
Const.rangeType_whole = '0'
# 指定部分
Const.rangeType_special = '1'

"""
满减活动资源类型
"""
# 全部有声书籍，此时rangeType必须为0
Const.rangeEntityType_book = '1'
# 全部付费节目，此时rangeType必须为0
Const.rangeEntityType_albumn = '2'
# 指定阅读书籍
Const.rangeEntityType_readbook = '3'
# 指定付费书籍/节目
Const.rangeEntityType_bookandalbumn = '4'

"""
书籍付费类型
"""
# 免费
Const.payType_free = 0
# 整本收费
Const.payType_charge_whole = 1
# 按章收费
Const.payType_charge_charpter = 2
# 订阅收费
Const.payType_charge_subscribe = 3

"""
购书折扣营销对象选择
"""
# 全部有声付费书籍
Const.objectType_Book = '1'
# 全部有声付费节目
Const.objectType_Albumn = '2'
# 指定收费书籍/节目
Const.objectType_AlbumnAndBook = '3'
# 指定阅读书籍
Const.objectType_ReadBook = '4'
"""
购书折扣选择折扣方式
"""
# 指定折扣率
Const.discountType_discountRate = '1'
# 指定折扣后价格
Const.discountType_discountPrice = '2'

"""
充值类型cointype，安卓/ios
"""
Const.coinType_Andriod = 'coin'
Const.coinType_ios = 'ios_coin'
"""
购买方式
"""
# 分章节购买书籍
Const.buy_Type_Book_by_charpter = '27'
# 整本购买书籍
Const.buy_Type_Book_by_whole = '26'
# 分章节购买节目
Const.buy_Type_Album_by_charpter = '41'
# 整本购买节目
Const.buy_Type_Album_by_whole = '42'

"""
兑换码使用范围

"""
# 指定上传者
Const.exchange_Code_specUploader = '1'
# 指定阅读版权机构
Const.exchange_Code_specRead_copyright = '10'
# 指定阅读分类
Const.exchange_Code_Read_Classify = '11'
# 指定阅读书籍
Const.exchange_Code_Read_book = '12'
# 指定听书版权机构
Const.exchange_Code_specListen_copyright = '20'
# 指定有声听书分类
Const.exchange_Code_Listen__Classify = '21'
# 指定有声书籍
Const.exchange_Code_ListenBook = '22'
# 指定有声节目
Const.exchange_Code_Listen_Albumn = '30'

"""
兑换码兑换面额
"""
# 面额1元
Const.exchange_Code_ticket_amount_1 = '1'
# 面额2元
Const.exchange_Code_ticket_amount_2 = '2'
# 面额5元
Const.exchange_Code_ticket_amount_5 = '5'
# 面额10元
Const.exchange_Code_ticket_amount_10 = '10'
# 面额20元
Const.exchange_Code_ticket_amount_20 = '20'
# 面额50元
Const.exchange_Code_ticket_amount_50 = '50'
# 面额100元
Const.exchange_Code_ticket_amount_100 = '100'
# 面额150元
Const.exchange_Code_ticket_amount_150 = '150'

"""
vip的兑换值

"""
# 1天
Const.exchange_Code_vip_amount_1_day = '101'
# 7天
Const.exchange_Code_vip_amount_7_day = '102'
# 15天
Const.exchange_Code_vip_amount_15_day = '103'
# 1个月
Const.exchange_Code_vip_amount_1_month = '104'
# 3个月
Const.exchange_Code_vip_amount_3_month = '105'
# 6个月
Const.exchange_Code_vip_amount_6_month = '106'
# 12个月
Const.exchange_Code_vip_amount_12_month = '107'

"""
用券类型：0-全用券，1-券+余额,2-不用券
"""
Const.useTikectsType_all_use_tikect = '0'
Const.useTikectsType_tikect_and_monney = '1'
Const.useTikectsType_no_use_tikect = '2'
