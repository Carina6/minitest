#!/usr/bin/env python
# -*- coding: utf-8 -*-
from queue import Queue, Empty
from threading import Thread


#
# http://eyalarubas.com/python-subproc-nonblock.html
#


class NonBlockingStreamReader(object):
    def __init__(self, stream):
        '''
        stream: the stream to read from. Usually a process' stdout or stderr.
        '''

        self._s = stream
        self._q = Queue()

        def _populate_queue(stream, queue):
            '''
            Collect lines from 'stream' and put them in 'quque'.
            '''

            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    raise Exception('')

        self._t = Thread(target=_populate_queue, args=(self._s, self._q))
        self._t.daemon = True
        self._t.start()

    def readline(self, timeout=None):
        try:
            return self._q.get(block=timeout is not None, timeout=timeout)
        except Empty:
            return None
