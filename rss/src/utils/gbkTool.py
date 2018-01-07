# -coding: utf-8 -
class GbkTool():
    @staticmethod
    def toGbk(s):
        return s.encode('gbk', 'ignore')

class TreeDir():
    def createTreeDir(tree_dict):
        rtdir = {
            "root": [1, {
                "child.txt" : ["0"],
                "child2dir" : ["1", {
                    "grand.txt": "0",
                    "grandsondir": "1"
                }]
            }]
        }
        for d in rtdir:
            if d is '':
                print '1'
        pass