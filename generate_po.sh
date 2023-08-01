#!/bin/bash

xgettext --join-existing -L python ./bell-scheduler/python3-bellscheduler/BellManager.py -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/BellForm.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/BellOptions.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/BellsInfo.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/BellsList.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/Cron.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/CustomPopUp.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/ImageSelector.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/ListDelegateBellItem.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/LoadWaiting.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/MainOptions.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/SliderPopUp.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/SoundSelector.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/TimeSelector.qml -o ./translations/bell-scheduler.pot
xgettext --join-existing -kde -ki18nd:2 ./bell-scheduler/python3-bellscheduler/rsrc/ValiditySelector.qml -o ./translations/bell-scheduler.pot
