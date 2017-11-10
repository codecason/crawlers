# -coding:utf-8 -*-
import os

if __name__ == '__main__':
    os.chdir('tutorial')
    names = ['nowcoder', 'douban', 'shuimu']
    for i in names:
        os.system('scrapy crawl {}'.format(i))
    # os.system('python query.py')
