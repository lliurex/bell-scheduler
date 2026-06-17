import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: scheduler
    spacing: 10
    focus: true

    RowLayout {
        id: clockLayout
        enabled: true
        Layout.alignment: Qt.AlignHCenter
        spacing: 5

        property int hoursWheelAccumulator:0
        property int minutesWheelAccumulator:59
        readonly property int wheelThreshold:360

        Component {
            id: numberDelegate
            Item {
                width: 60
                height: 60

                Text {
                    text: modelData.toString().padStart(2, "0")
                    font.pointSize: 40
                    color: "#3daee9"
                    anchors.centerIn: parent
                }
            }
        }

        Rectangle {
            width: 60
            height: 60
            color: "transparent"
            clip: true

            PathView {
                id: hoursSelector
                anchors.fill: parent
                focus: true
                model: 24
                delegate: numberDelegate

                pathItemCount: 3
                preferredHighlightBegin: 0.5
                preferredHighlightEnd: 0.5
                highlightRangeMode: PathView.StrictlyEnforceRange

                currentIndex: bellStackBridge.bellCron.hour

                onCurrentIndexChanged: {
                    bellStackBridge.updateClockValues({"hour": hoursSelector.currentIndex});
                }

                WheelHandler {
                    acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad

                    onWheel: (event) => {

                        let delta=event.angleDelta.y;

                        if ((delta >0 && clockLayout.hoursWheelAccumulator < 0) || ( delta <0 && clockLayout.hoursWheelAccumulator > 0)){
                            clockLayout.hoursWheelAccumulator = 0;
                        }

                        clockLayout.hoursWheelAccumulator+=delta;

                        if (clockLayout.hoursWheelAccumulator >= clockLayout.wheelThreshold){
                            hoursSelector.decrementCurrentIndex();
                            clockLayout.hoursWheelAccumulator=0;
                        } 
                        else if (clockLayout.hoursWheelAccumulator <= -clockLayout.wheelThreshold) {
                            hoursSelector.incrementCurrentIndex();
                            clockLayout.hoursWheelAccumulator=0;
                        }
                            
                    }
                }

                path: Path {
                    startX: 30; startY: -60
                    PathPercent {value:0.0}

                    PathLine { x: 30; y: 30 }
                    PathPercent {value:0.5}

                    PathLine { x: 30; y: 120 }
                    PathPercent {value:1.0}

                }

                HoverHandler{
                    id:hoursHandler
                }

                ToolTip.delay:1000
                ToolTip.timeout:1000
                ToolTip.visible:hoursHandler.hovered
                ToolTip.text:i18nd("bell-scheduler","You can use the mouse wheel to change the hour")
            }
        }

        Text {
            text: ":"
            font.pointSize: 30
            color: "#3daee9"
            Layout.alignment: Qt.AlignCenter
        }

        Rectangle {
            width: 60
            height: 60
            color: "transparent"
            clip: true

            PathView {
                id: minutesSelector
                anchors.fill: parent
                focus: true
                model: 60
                delegate: numberDelegate

                pathItemCount: 3
                preferredHighlightBegin: 0.5
                preferredHighlightEnd: 0.5
                highlightRangeMode: PathView.StrictlyEnforceRange

                currentIndex: bellStackBridge.bellCron.minute

                onCurrentIndexChanged: {
                    bellStackBridge.updateClockValues({"minute": minutesSelector.currentIndex});
                }

                WheelHandler {
                    acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
                    onWheel: (event) => {

                        let delta=event.angleDelta.y;

                        if ((delta >0 && clockLayout.minutesWheelAccumulator < 0) || ( delta <0 && clockLayout.minutesWheelAccumulator > 0)){
                            clockLayout.minutesWheelAccumulator = 0;
                        }

                        clockLayout.minutesWheelAccumulator+=delta;

                        if (clockLayout.minutesWheelAccumulator >= clockLayout.wheelThreshold){ 
                            minutesSelector.decrementCurrentIndex();
                            clockLayout.minutesWheelAccumulator = 0;
                        } else if (clockLayout.minutesWheelAccumulator <= -clockLayout.wheelThreshold) {
                            minutesSelector.incrementCurrentIndex();
                            clockLayout.minutesWheelAccumulator = 0;
                        }
                    }
                }

                path: Path {
                    startX: 30; startY: -60
                    PathPercent {value:0.0}

                    PathLine { x: 30; y: 30 }
                    PathPercent {value:0.5}

                    PathLine { x: 30; y: 120 }
                    PathPercent {value:1.0}
                }

                HoverHandler{
                    id:minutesHandler
                }

                ToolTip.delay:1000
                ToolTip.timeout:1000
                ToolTip.visible:minutesHandler.hovered
                ToolTip.text:i18nd("bell-scheduler","You can use the mouse wheel to change the minutes")
            }
        }

        Button {
            id: editHourBtn
            display: AbstractButton.IconOnly
            icon.name: "edit-entry"
            Layout.alignment: Qt.AlignCenter
            Layout.topMargin: 10
            Layout.leftMargin: 10
            hoverEnabled: true

            ToolTip.delay: 1000
            ToolTip.timeout: 3000
            ToolTip.visible: hovered
            ToolTip.text: i18nd("bell-scheduler", "Click to edit time with keyboard")

            onClicked: {
                timeSelector.open()
            }
        }
                
    }

    RowLayout {
        id: daysLayout
        enabled: true
        Layout.alignment: Qt.AlignHCenter
        Layout.fillWidth: true
        Layout.bottomMargin: 5
        spacing: 8

        ListModel {
            id: daysModel
            ListElement { key: "0"; name: "Monday" }
            ListElement { key: "1"; name: "Tuesday" }
            ListElement { key: "2"; name: "Wednesday" }
            ListElement { key: "3"; name: "Thursday" }
            ListElement { key: "4"; name: "Friday" }
        }

        Repeater {
            model: daysModel

            DayButton {
                dayBtnChecked: bellStackBridge.bellDays[model.key]
                dayBtnText: i18nd("bell-scheduler", model.name)

                onDayBtnClicked: (value) => {
                    bellStackBridge.updateWeekDaysValues({[model.key]: value});
                }
            }
        }
    }

    TimeSelector {
        id: timeSelector
        hourValue: hoursSelector.currentIndex.toString().padStart(2, "0")
        minuteValue: minutesSelector.currentIndex.toString().padStart(2, "0")

        Connections {
            target: timeSelector
            function onTimeApplyClicked(hourValue, minuteValue){
                hoursSelector.currentIndex = hourValue
                minutesSelector.currentIndex = minuteValue
            }
        }
    }

    Timer {
        id: safetyTimer
        property var callback: null
        onTriggered: {
            if (callback) {
                callback();
                callback = null;
            }
        }
    }

    function delay(delayTime, cb) {
        safetyTimer.stop();
        safetyTimer.interval = delayTime;
        safetyTimer.callback = cb;
        safetyTimer.start();
    }

    function validateEntry(hour, minute) {
        return hour !== "" && minute !== "";
    }
}
