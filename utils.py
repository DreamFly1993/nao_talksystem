import logging as log
import time


class Write2Log(object):
    def __init__(self):
        print('initing write2log')
        log.basicConfig(level=log.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='logs/ts.log',
                        filemode='w')
        console = log.StreamHandler()
        console.setLevel(log.INFO)
        formatter = log.Formatter('%(name)-12s: %(message)s')
        console.setFormatter(formatter)
        log.getLogger('').addHandler(console)
        print 'initial finished!'

    @property
    def logs(self):
        return log

__logs = Write2Log()


def get_logger():
    return __logs.logs
