#!/usr/bin/env python
# 2014-03-13 13:27:14Z pingliangchenisthebest@gmail.com
# Copyright (c) 2009, PinLiang Chen'. All rights reserved.
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

from datetime import datetime
from daemon import runner



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
    
'''
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
'''    
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
    

def poll(interval):
    """Retrieve raw stats within an interval window."""
    tot_before = psutil.net_io_counters()
    pnic_before = psutil.net_io_counters(pernic=True)
    # sleep some time
    time.sleep(interval)
    tot_after = psutil.net_io_counters()
    pnic_after = psutil.net_io_counters(pernic=True)
    return (tot_before, tot_after, pnic_before, pnic_after)    
    

def refresh_window(tot_before, tot_after, pnic_before, pnic_after):
    """Print stats on screen."""
    global lineno    

    nic_names = list(pnic_after.keys())
    nic_names.sort(key=lambda x: sum(pnic_after[x]), reverse=True)
    for name in nic_names:
        stats_before = pnic_before[name]
        stats_after = pnic_after[name]    

    if name == 'eth0':
    	write(str(bytes2human(stats_after.bytes_recv - stats_before.bytes_recv)), str(bytes2human(stats_after.bytes_sent - stats_before.bytes_sent)))
    win.refresh()
    lineno = 0    

def write(receiver, sent):    
#    filepath = '/var/lib/tomcat7/webapps/Systeminfo'
    filepath = '/home/Systeminfo'
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
    file.write(str(psutil.cpu_percent(interval=1))+","+g[0]+","+e[0]+","+receiver+","+sent+","+date+"\n")

class App():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/var/run/mydaemon.pid'
        self.pidfile_timeout = 5

    def run(self):
        interval = 0
        while True:
            args = poll(interval)
            refresh_window(*args)
            interval = 3

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
