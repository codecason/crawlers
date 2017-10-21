# -*- coding: utf-8 -*-
import os, scrapy, re

class CleanTool():
    pattern1 = re.compile('<br><br>|<br>')
    # 必须删除script
    pattern2 = re.compile('<tr>|<td>|<script.*?>.*?</script>', re.S)
    pattern3 = re.compile('<div.*?>', re.S)
    replaceSpan = re.compile('<span>|</span>')
    pattern4 = re.compile('</div>')

    def pureClean(self, s):
        s = re.sub(self.pattern1, '\n', s)
        s = re.sub(self.pattern2, '', s)
        s = re.sub(self.pattern3, '\n', s)
        s = re.sub(self.pattern4, '\n\n', s)
        s = re.sub(self.replaceSpan, '', s)
        return s
        # tag removed, strong, script removed, link reserved
    
    def htmlClean(self):
        # all reserved
        pass
    pass
