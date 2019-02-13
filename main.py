#coding=utf8
 
import hashlib
import urllib
import random
import http.client
import json
from enum import Enum, unique
from ColorPrint import cPrint, LogLevel, getStrByLevel

@unique
class LanguageType(Enum):
    ALL_CHINESE = 0  # 全是中文
    SOME_CHINESE = 1  # 有部分中文
    NO_CHINESE = 2 # 没有中文

def getLanguageType(check_str):

    hasChinese = False
    hasOther = False

    for ch in check_str.encode('utf-8').decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            hasChinese = True
        else:
            hasOther = True

    if (hasChinese and hasOther):
         return LanguageType.SOME_CHINESE

    if (not hasChinese and hasOther):
         return LanguageType.NO_CHINESE

    if (hasChinese and not hasOther):
         return LanguageType.ALL_CHINESE

    return LanguageType.SOME_CHINESE
    

def languageDetect(words):

    fromLang = 'en'
    toLang = 'zh'
    
    lType = getLanguageType(words)

    if (lType == LanguageType.ALL_CHINESE):
        fromLang = 'zh'
        toLang = 'en'
    
    if (lType == LanguageType.NO_CHINESE):
        pass # use default

    if (lType == LanguageType.SOME_CHINESE):
        print('Wrong input type, please enter total chinese or english')
        exit() # todo: error handle

    return (fromLang, toLang)


def genUrl(words):

    appid = '20181219000250204'
    secretKey = 'RLLRadKjkALTDp8iSqMw'

    url = '/api/trans/vip/translate'
    q = words
    (fromLang, toLang) = languageDetect(words)
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(bytes(sign, 'utf-8'))
    sign = m1.hexdigest()
    url = url+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    return url

def doTranlate(httpClient, url):
    res = "🌈err"
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', url)
 
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        res = response.read()
    except Exception as e:
        res = str(e)
    finally:
        return res

def translate(client, words):
    url = genUrl(words)
    return doTranlate(client, url)

def parseRes(jsonRes):
    # {"from":"en","to":"zh","trans_result":[{"src":"hi","dst":"\u4f60\u597d"}]}
    res = json.loads(jsonRes)
    cPrint("( " + res["from"] + " => " + res["to"] + ")", LogLevel.HIGH_LIGHT)

    tRess = res["trans_result"]
    for tRes in tRess:

        cPrint(" ******* " + tRes["dst"] + " ******* ", LogLevel.HIGH_LIGHT)
    

if __name__ == "__main__":

    httpClient = None

    while(1):
        print("")
        cPrint("○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○", LogLevel.MARK)
        cPrint("Enter the word you wanna tranlate: " + getStrByLevel("", LogLevel.INPUT, False), LogLevel.TIPS, False)
        inputStr = input()
        print("")
        res = translate(httpClient, inputStr)
        parseRes(str(res, encoding='utf-8'))
