# -*- coding: UTF-8 -*-
"""
 * @author  zfj
 * @date  2020/9/26 15:39
"""
import sys
import datetime
import time
import pytz
import requests
import json
import os
import logging
from logging import handlers
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

base_path = os.path.dirname(__file__)
if base_path == "":
    base_path = "/home/runner/work/mimikkoAutoSignIn/mimikkoAutoSignIn"
    os.system(f"chmod 777 {base_path}")


class Logger(object):
    level_relations = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
    }  # 日志级别关系映射

    def beijing(sec, what):
        beijing_time = datetime.datetime.now(tz=pytz.timezone("PRC"))
        return beijing_time.timetuple()

    def __init__(
        self,
        base_path,
        filename,
        level="info",
        when="MIDNIGHT",
        interval=1,
        backCount=30,
        fmt="%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    ):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        logging.Formatter.converter = self.beijing
        self.logger.setLevel(self.level_relations[level])  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        fh = handlers.TimedRotatingFileHandler(
            filename=filename, when=when, interval=interval, backupCount=backCount, encoding="utf-8"
        )
        fh_all = handlers.TimedRotatingFileHandler(
            filename=base_path + "/log/all.log", when="D", interval=30, backupCount=backCount, encoding="utf-8"
        )
        fh.setFormatter(format_str)  # 设置文件里写入的格式
        fh_all.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(fh)
        self.logger.addHandler(fh_all)


# log信息配置
if not os.path.exists(base_path + "/log"):
    os.makedirs(f"{base_path}/log", mode=777)
    os.system(f"chmod 777 {base_path}/log")
date = time.strftime("%Y-%m-%d", time.localtime(time.time() + 8 * 3600))
log = Logger(base_path, base_path + f"/log/{date}.log", level="debug")

# 默认参数配置
default_code = "momona"
default_app_version = "3.1.7"
default_max_favorability = 135950


# 开始脚本
if len(sys.argv) == 3:
    app_id = sys.argv[1]
    Authorization = sys.argv[2]
else:
    log.logger.warning("缺少必要参数！！！(Bot插件版忽略此错误)")
    # 也可以在这里设定默认值
    app_id = ""
    Authorization = ""
with open(base_path + "/config.json", "r") as f:
    config = json.loads(f.read(), encoding="utf8")
if config.get("code") and config["code"] == "":
    config["code"] = default_code
    log.logger.warning(f"config-code为空，自动设置签到助手为{default_code}")
if config.get("app_version") and config["app_version"] == "":
    config["app_version"] = default_app_version
    log.logger.warning(f"config-app_version为空，自动设置App版本为 {default_app_version}")
if config.get("max_favorability") and not config["max_favorability"]:
    config["max_favorability"] = default_max_favorability
    log.logger.warning(f"config-max_favorability为空，自动设置切换助手阈值为{default_max_favorability}")

apiPath = "http://api1.mimikko.cn/client/user/GetUserSignedInformation"
apiPath2 = "http://api1.mimikko.cn/client/dailysignin/log/30/0"
sign_path = "https://api1.mimikko.cn/client/RewardRuleInfo/SignAndSignInformationV3"
energy_info_path = "https://api1.mimikko.cn/client/love/GetUserServantInstance"
energy_reward_path = "https://api1.mimikko.cn/client/love/ExchangeReward"
defeat_set = "https://api1.mimikko.cn/client/Servant/SetDefaultServant"


## 写入json文件
def write2json(path, data):
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)
        log.logger.info(f"{data}写入文件{path}完成...")


def apiRequest(url, app_id, Authorization, params, method="GET"):
    params_get = params
    headers_get = {
        "Cache-Control": "Cache-Control:public,no-cache",
        "Accept-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0(Linux;Android6.0.1;MuMu Build/V417IR;wv)AppleWebKit/537.36(KHTML,"
        "like Gecko)Version/4.0 Chrome/52.0.2743.100MobileSafari / 537.36",
        "AppID": app_id,
        "Version": config["app_version"],
        "Authorization": Authorization,
        "Connection": "Keep-Alive",
        "Host": "api1.mimikko.cn",
    }
    headers_post = {
        "Accept": "application/json",
        "Cache-Control": "no-cache",
        "AppID": app_id,
        "Version": config["app_version"],
        "Content-Type": "application/json",
        "Host": "api1.mimikko.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.1",
    }

    try:
        if method == "GET":
            with requests.get(url, headers=headers_get, params=params_get, verify=False, timeout=300) as resp:
                res = resp.json()
                return res
        elif method == "POST":
            # 暂未用到，以后再写
            pass

    except Exception as ex:
        log.logger.error(ex)


def mimikko(app_id, Authorization):
    sign_data = apiRequest(sign_path, app_id, Authorization, "")
    energy_info_data = apiRequest(energy_info_path, app_id, Authorization, {"code": config["code"]})
    if energy_info_data:
        if energy_info_data.get("body"):
            if energy_info_data["body"]["Energy"] > 0:
                energy_reward_data = apiRequest(energy_reward_path, app_id, Authorization, {"code": config["code"]})
            else:
                energy_reward_data = "您的能量值不足，无法兑换"
            if energy_info_data["body"]["Favorability"] > config["max_favorability"]:
                if config["code"] in config["servant_list"]:
                    if config["servant_list"].index(config["code"]) + 1 < len(config["servant_list"]):
                        config["code"] = config["servant_list"][config["servant_list"].index(config["code"]) + 1]
                        log.logger.info(f"当前助手成长值已达临界值,切换为下一助手{config['code']}")
                        log.logger.warning("同时其他客户端助手也可能会改变")
                    else:
                        log.logger.error("切换助手失败")
                else:
                    config["code"] = config["servant_list"][0]
                    log.logger.info(f"当前助手成长值已达临界值,切换为下一助手{config['code']}")
                    log.logger.warning("同时其他客户端助手也可能会改变")
        else:
            energy_reward_data = "您的能量值不足，无法兑换"
    else:
        energy_reward_data = "您的能量值不足，无法兑换"
    set_servant = apiRequest(defeat_set, app_id, Authorization, {"code": config["code"]})
    sign_info = apiRequest(apiPath, app_id, Authorization, "")
    sign_history = apiRequest(apiPath2, app_id, Authorization, "")
    write2json(base_path + "/config.json", config)
    return sign_data, energy_info_data, energy_reward_data, sign_info, sign_history


def timeStamp2time(timeStamp):
    timeArray = time.localtime(timeStamp / 1000)
    otherStyleTime = time.strftime("%m月%d日 %H:%M", timeArray)
    return otherStyleTime


if app_id and Authorization:
    sign_data, energy_info_data, energy_reward_data, sign_info, sign_history = mimikko(app_id, Authorization)
    # # sign_data
    log.logger.info("sign_data:\n" + str(sign_data))
    # print("code", sign_data["code"])
    # # print(sign_data["body"]["date"])
    # # print(sign_data["body"]["signTime"])
    # print("Name", sign_data["body"]["Name"])
    # print('Description', sign_data["body"]['Description'])
    # print('PictureUrl', sign_data["body"]['PictureUrl'])
    # print('成长值Reward', sign_data["body"]['Reward'])
    # print('硬币GetCoin', sign_data["body"]['GetCoin'])
    # # Energy info
    log.logger.info("energy_info_data:\n" + str(energy_info_data))
    # print('code', energy_info_data['code'])
    # print('msg', energy_info_data['msg'])
    # # print('Favorability',energy_data['body']['Favorability'])
    # # print('MaxFavorability',energy_data['body']['MaxFavorability'])
    # print('Favorability/MaxFavorability',
    #       str(energy_info_data['body']['Favorability']) + "/" + str(energy_info_data['body']['MaxFavorability']))
    # print('Energy', energy_info_data['body']['Energy'])
    # # Energy reward
    log.logger.info("energy_reward_data:\n" + str(energy_reward_data))
    # # sign_info
    # print(sign_info)
    # print(sign_info['code'])
    # print('IsSign', sign_info['body']['IsSign'])
    # print('连续登录天数ContinuousSignDays', sign_info['body']['ContinuousSignDays'])
    # # sign_history
    log.logger.info("sign_history:\n" + str(sign_history))
    # print('code', sign_history['code'])
    # print('startTime', timeStamp2time(sign_history["body"]['startTime']))
    # print('endTime', timeStamp2time(sign_history["body"]['endTime']))
    # print('signLogs', sign_history['body']['signLogs'])
    # for item in sign_history['body']['signLogs']:
    #     print('signTime', timeStamp2time(item['signDate']))
