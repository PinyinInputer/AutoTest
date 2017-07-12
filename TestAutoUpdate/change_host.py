#!/usr/bin/python
# coding:utf8
import os
import sys
import re

hostsfile = "/etc/hosts"  # hosts文件绝对路径

ip_dict = {"1.1.1.1": "2.2.2.1", "1.1.1.2": "2.2.2.2", "1.1.1.3": "2.2.2.3"}  # 这是自定义的字典形式为：old_ip:new_ip

ip = []  # 定一个空列表，来存储old_ip的列表
Line = []  # 定一个空列表，来存储修改后的hosts文件内容的列表

fd = open(hostsfile).readlines()  # 打开文件

# 用for循环得到old_ip的列表
for old_ip in ip_dict.keys():
    ip.append(old_ip)

# 用for循环列出每一行，并进行匹配old_ip 如果匹配到就使用re.sub()进行替换。并存储在Line这个列表中
for line in fd:
    if line.strip() == '':
        # continue
        Line.append(line)  ##如果是空行也加入列表中，保证文件内容与原内容形式一致
    else:
        h_ip = line.strip().split()[0]  ##取得hosts文件中的ip地址
        if h_ip in ip:
            lin = re.sub(h_ip, ip_dict[h_ip], line)  # 如果匹配到就进行替换
            print("文件修改的内容如下：")
            print("%s --> %s" % (line.strip("\n"), lin))
            Line.append(lin)
        else:
            Line.append(line)

# 最后得到Line列表
# 重新把列表的内容写入到/etc/hosts文件中
fc = open(hostsfile, 'w')
fc.writelines(Line)
fc.close()