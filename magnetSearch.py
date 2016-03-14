# -*- coding: utf-8 -*-

import os
import threading
import time
import webbrowser

from magnetSite import *

__author__ = 'jingqiwang'


if __name__ == '__main__':
    ms = magnetSite()
    print '*' * 50
    print '*'
    print '* Magnet Search'
    print '*'
    print '* V 1.0.1'
    print '* Coded by Jingqi'
    print '*'
    print '*' * 50

    while True:
        fanhao = raw_input('请输入番号: ')
        if fanhao.lower() in ('exit', 'quit'):
            sys.exit()
        else:
            start = (time.time(), time.ctime())
            print start[1]

            threads = [threading.Thread(target=ms.icili, args=(fanhao,)),
                       threading.Thread(target=ms.btdao, args=(fanhao,)),
                       threading.Thread(target=ms.cilisou, args=(fanhao,)),
                       threading.Thread(target=ms.kickass, args=(fanhao,)),
                       threading.Thread(target=ms.kitty, args=(fanhao,))]

            [thread.start() for thread in threads]
            [thread.join() for thread in threads]
            result = ms.result
            result.sort(key=lambda x: x.popularity)

            html = ms.generate_html(result)
            finish = (time.time(), time.ctime())
            print finish[1]
            print 'Time cost:%.2f secs' % (finish[0] - start[0])

            with open('Result.html', 'wb') as f:
                f.write(str(html))

            ms.result = []

            webbrowser.open('file://' + os.getcwd() + '/Result.html', new=2)
