#---*- coding:utf-8----*---
import os, urllib, urllib2, re, json

class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    #删除<i>标签
    removeItag = re.compile('<i>|</i>')
    # 删除<script>标签
    # removeScript = re.compile('</?noscript>|<script.*?></?script>')
    # 应该有内定义的数组taglist 和替换数组replace , 以确保针对实际包含的标签进行过滤
    def replace(self,x,keepname = True):
        imgstr = ""
        addrstr = ""
        if keepname == True:
            imgstr = "[图片]"
            addrstr = "[链接]"
        x = re.sub(self.removeImg,imgstr,x)
        x = re.sub(self.removeAddr,addrstr,x)
        x = re.sub(self.replaceLine,"\r\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\r\n    ",x)
        x = re.sub(self.replaceBR,"\r\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        x = re.sub(self.removeItag, "", x)
        #strip()将前后多余内容删除
        return x.strip()

    def json_print(self, json_data):
        if isinstance(json_data, list) or isinstance(json_data, dict):
            print json.dumps(json_data, indent=2)
