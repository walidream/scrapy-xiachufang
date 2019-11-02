from scrapy.cmdline import execute 

import sys
import os

# 获取mian文件的路径
curr_path = os.path.abspath(__file__)
# 获取文件夹
dir_path = os.path.dirname(curr_path)

if __name__ == "__main__":
    sys.path.append(dir_path)
    execute(["python -m scrapy","crawl","xcf"])