#!/usr/bin/env python
# 2014-04-15 16:07:57Z pingliangchenisthebest@gmail.com
# Copyright (c) 2014, PinLiang Chen'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.


import sys
import os
if os.name != 'posix':
    sys.exit('platform not supported')
import atexit
import curses
import time
import datetime
import psutil
import json

from datetime import datetime
from daemon import runner
from threading import Thread


# --- curses stuff
def tear_down():
    win.keypad(0)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

win = curses.initscr()
atexit.register(tear_down)
curses.endwin()
lineno = 0    
    

def print_line(line, highlight=False):
    """A thin wrapper around curses's addstr()."""
    global lineno
    try:
        if highlight:
            line += " " * (win.getmaxyx()[1] - len(line))
            win.addstr(lineno, 0, line, curses.A_REVERSE)
        else:
            win.addstr(lineno, 0, line, 0)
    except curses.error:
        lineno = 0
        win.refresh()
        raise
    else:
        lineno += 1
# --- curses stuff    
    
def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)    
    

def poll(interval, i):
    """Retrieve raw stats within an interval window."""
    tot_before = psutil.net_io_counters()
    pnic_before = psutil.net_io_counters(pernic=True)
    # sleep some time
    time.sleep(interval)
    tot_after = psutil.net_io_counters()
    pnic_after = psutil.net_io_counters(pernic=True)
    return (tot_before, tot_after, pnic_before, pnic_after, i)    
    

def refresh_window(tot_before, tot_after, pnic_before, pnic_after, i):
    """Print stats on screen."""
    global lineno    
    nic_names = list(pnic_after.keys())
    nic_names.sort(key=lambda x: sum(pnic_after[x]), reverse=True)
    for name in nic_names:
        stats_before = pnic_before[name]
        stats_after = pnic_after[name]    
    if name == 'lo':
	write(str(stats_after.bytes_recv - stats_before.bytes_recv), str(stats_after.bytes_sent - stats_before.bytes_sent), i)
    win.refresh()
    lineno = 0    

def write(receiver, sent, i):
    if i ==0:
       filepath = '/root/python/4sec'
    elif i==1:
       filepath = '/root/python/1hour'
    elif i==2:
       filepath = '/root/python/6hour'
    elif i==3:
       filepath = '/root/python/12hour'
    elif i==4:
       filepath = '/root/python/1day'
    elif i==5:
       filepath = '/root/python/2day'
    elif i==6:
       filepath = '/root/python/4day'
    elif i==7:
       filepath = '/root/python/7day'
    elif i==8:
       filepath = '/root/python/14day'
    elif i==9:
       filepath = '/root/python/30day'

    dirpath = os.path.dirname(filepath)
    if not os.path.exists(dirpath) or not os.path.isdir(dirpath):
	os.makedirs(dirpath)
    a=psutil.disk_usage('/')
    b=str(a)
    d=b.split('percent=')
    e=d[1].split(')')    

    c=str(psutil.virtual_memory())
    f=c.split('percent=')
    g=f[1].split(',')    

    date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    file = open(filepath,'a+b')
    file.write(json.dumps({'CPU':str(psutil.cpu_percent(interval=1)), 'Memory':g[0], 'HardDisk':e[0], 'NetReceiver':receiver, 'NetSent':sent, 'Date':date})+","+"\n")
    file.close()
    num_line = 0
    f = open(filepath)
    allline = f.readlines()
    f.close()
    f = open(filepath)
    for line in f:
       num_line = num_line +1
    a = num_line-180
    f.close()
    if a>=0:
       f = open(filepath, "w")
       for a in range(a, num_line):
          f.write(allline[a])
       f.close()

def myfunc(i):
    if i==1:
	while True:
            interval=19
            args = poll(interval, i)
            refresh_window(*args)
    elif i==2:
        while True:
            interval=39
            args = poll(interval, i)
            refresh_window(*args)
    
    elif i==3:
        while True:
            interval=239
            args = poll(interval, i)
            refresh_window(*args)
    elif i==4:
        while True:
            interval=479
            args = poll(interval, i)
            refresh_window(*args)
    elif i==5:
        while True:
            interval=959
            args = poll(interval, i)
            refresh_window(*args)
    elif i==6:
        while True:
            interval=1919
            args = poll(interval, i)
            refresh_window(*args)
    elif i==7:
        while True:
            interval=3359
            args = poll(interval, i)
            refresh_window(*args)
    elif i==8:
        while True:
            interval=6719
            args = poll(interval, i)
            refresh_window(*args)
    elif i==9:
        while True:
            interval=14399
            args = poll(interval, i)
            refresh_window(*args)


class App():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/var/run/Hello.pid'
        self.pidfile_timeout = 5

    def run(self):
        for i in range(10):
            t = Thread(target=myfunc,args=(i,))
            t.start()

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
