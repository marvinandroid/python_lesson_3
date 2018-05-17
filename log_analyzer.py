#!/usr/bin/env python3
# MIT License
# Copyright (c) 2018 adzakha2@mts.ru
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
import time
import sqlite3
import os
from sys import argv

if not os.path.exists('db.sqlite3'):
    print('Database file not found')
    exit(1)

db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()

try:
    cursor.execute('select id from logview_logrecord limit 1')
except sqlite3.OperationalError:
    print('Table logview_logrecord not found')
    exit(1)

epoch_re = re.compile(r'\(([0-9\.]+)\)')
connect_re = re.compile(r'tcp/connect')
permission_re = re.compile(r'((\w+)\((\d+)\))')
status_re = re.compile(r'\s(\[|\]):')
username_re = re.compile(r'([a-zA-Z\.]+).(\w+)@')
userip_re = re.compile(r'@(([12]?\d?\d\.){3}[12]?\d?\d)\.?(\d+)?')
destination_re = re.compile(r'-> ((([12]?\d?\d\.){3}[12]?\d?\d)\.?(\d+)?) ((([12]?\d?\d\.){3}[12]?\d?\d)\.?(\d+)?)')

with open(argv[1]) as input_file:
    for line in input_file:
        if connect_re.search(line) is None:
            continue
        m_epoch = epoch_re.search(line)
        m_permission = permission_re.search(line)
        m_status = status_re.search(line)
        m_username = username_re.search(line)
        m_userip = userip_re.search(line)
        m_destination = destination_re.search(line)
        if m_epoch and m_permission and m_status and m_username and m_userip and m_destination:
            row_epoch, = m_epoch.groups()
            datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row_epoch)))
            _, permission, rule_num = m_permission.groups()
            if permission != 'pass':
                continue
            status, = m_status.groups()
            if status != '[':
                continue
            auth_system, username = m_username.groups()
            user_ip, _, _ = m_userip.groups()
            _, _, _, _, _, destination, _, dest_port = m_destination.groups()
            try:
                cursor.execute("insert into logview_logrecord values (NULL, ?, ?, ?, ?, ?, ?);",
                               (username, auth_system, user_ip, destination, dest_port, datetime))
            except sqlite3.IntegrityError:
                pass

try:
    db.commit()
except:
    print('Unable to save parse results')
    db.rollback()
finally:
    db.close()