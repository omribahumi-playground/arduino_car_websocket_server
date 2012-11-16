#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import tornado
from lib.CarDispatcher import *
from lib.CarWebSocketHandler import *

def main():
    CarDispatcher.init()

    application = tornado.web.Application([
        (r"/", CarWebSocketHandler)
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
