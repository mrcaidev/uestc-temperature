# UESTC official APIs about reporting.
api_dict = {
    "check": {
        "url": "https://jzsz.uestc.edu.cn/wxvacation/api/epidemic/checkRegisterNew",
        "method": "get",
        "data": {},
    },
    "unreturned": {
        "url": "https://jzsz.uestc.edu.cn/wxvacation/api/epidemic/monitorRegister",
        "method": "post",
        "data": {
            "currentAddress": "江苏省苏州市常熟市",
            "remark": "",
            "healthInfo": "正常",
            "healthColor": "绿色",
            "isContactWuhan": 0,
            "isFever": 0,
            "isInSchool": 0,
            "isLeaveChengdu": 1,
            "isSymptom": 0,
            "temperature": "36.5°C~36.9°C",
            "province": "江苏省",
            "city": "苏州市",
            "county": "常熟市",
        },  # You can modify these data as you like.
    },
    "returned": {
        "url": "https://jzsz.uestc.edu.cn/wxvacation/api/epidemic/monitorRegisterForReturned",
        "method": "post",
        "data": {
            "healthCondition": "正常",
            "todayMorningTemperature": "36.5°C~36.9°C",
            "yesterdayEveningTemperature": "36.5°C~36.9°C",
            "yesterdayMiddayTemperature": "36.5°C~36.9°C",
            "location": "四川省成都市郫都区丹桂路",
            "healthColor": "绿色",
        },  # You can modify these data as you like.
    },
}

# Common request headers, regardless of student identities.
common_headers = {
    "connection": "close",
    "encode": "false",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; BMH-AN10 Build/HUAWEIBMH-AN10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3149 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/1967 MicroMessenger/8.0.16.2040(0x28001057) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "X-Tag": "flyio",
    "content-type": "application/json",
    "Accept": "*/*",
    "X-Requested-With": "com.tencent.mm",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://jzsz.uestc.edu.cn/epidemic2/?sessionid=",
    "Cookie": "SESSION=",
}
