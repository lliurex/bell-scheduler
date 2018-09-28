#!/bin/bash

xgettext --join-existing ./bell-scheduler/python3-bellscheduler/MainWindow.py -o ./translations/bell-scheduler.pot
xgettext --join-existing ./bell-scheduler/python3-bellscheduler/BellBox.py -o ./translations/bell-scheduler.pot
xgettext --join-existing ./bell-scheduler/python3-bellscheduler/rsrc/bell-scheduler.ui -o ./translations/bell-scheduler.pot
xgettext --join-existing -L python ./bell-scheduler-indicator.install/usr/bin/bell-scheduler-indicator -o ./translations/bell-scheduler.pot
