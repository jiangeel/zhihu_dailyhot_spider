__author__ = 'Eeljiang'

from scrapy.cmdline import execute
import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['crapy', 'crawl', 'jobbole'])
# execute(['crapy', 'crawl', 'lagou'])
execute(['crapy', 'crawl', 'zhihu_sel'])