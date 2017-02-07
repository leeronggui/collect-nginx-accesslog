#!/bin/bash
PATH="/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin"

#tail -n 100 /data/logs/pay.56qq.com.log | ./collecter.py


#!/bin/bash

DAT1=/home/work/open-falcon/plugin/self/pay_offsetfile
ACCESSLOG=/data/logs/pay.56qq.com.log

dir=`dirname $0`

echo "=========" >> $dir/log.txt
date >> $dir/log.txt
/usr/sbin/logtail2 -f $ACCESSLOG -o $DAT1| /home/work/open-falcon/plugin/self/collecter.py  >> $dir/log.txt
