import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

GridLayout {
    id: scheduler
    rows: 2
    flow: GridLayout.TopToBottom
    focus:true

    Component.onCompleted:{
        hoursTumbler.forceActiveFocus()
    }

    GridLayout {
        id: clockLayout
        enabled: true
        Layout.leftMargin: 5
        Layout.rightMargin: 5
        Layout.bottomMargin: 5
        Layout.alignment: Qt.AlignHCenter
        columns: 4

        Component {
            id: delegateComponent
            Label {
                id: delegateLabel
                font.pointSize: 40
                text: modelData.toString().padStart(2, "0")
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                /*color:Tumbler.tumbler.hovered?"#add8e6":"#3daee9"*/
                color:"#3daee9"
             
            }
        }

   
        Rectangle {
            Layout.topMargin: 4
            Layout.alignment: Qt.AlignCenter
            height: 60
            width: 60
            color: "transparent"

            Tumbler {
                id: hoursTumbler
                width: 60
                height: 60
                model: 24
                currentIndex: bellStackBridge.bellCron.hour
                delegate: delegateComponent
                visibleItemCount: 1
                wheelEnabled:true
                hoverEnabled:true
                focus:hovered

                /*
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text: i18nd("bell-scheduler", "You can use the mouse wheel to change the hour")
                */

                onCurrentIndexChanged: {
                    bellStackBridge.updateClockValues({"hour": hoursTumbler.currentIndex});
                }
                
            }

        }

        Text {
            id: clockSeparator
            Layout.alignment: Qt.AlignCenter
            font.pointSize: 40
            color: "#3daee9"
            text: ":"
        }

        Rectangle {
            Layout.topMargin: 4 
            Layout.alignment: Qt.AlignCenter
            height: 60
            width: 60
            color: "transparent"

            Tumbler {
                id: minutesTumbler
                height: 60
                width: 60
                model: 60
                currentIndex: bellStackBridge.bellCron.minute
                delegate: delegateComponent
                visibleItemCount: 1
                wheelEnabled:true
                hoverEnabled:true
                focus:hovered

                /*
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text: i18nd("bell-scheduler", "You can use the mouse wheel to change the minutes")
                */

                onCurrentIndexChanged: {
                    bellStackBridge.updateClockValues({"minute": minutesTumbler.currentIndex});
                }

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

            TimeSelector {
                id: timeSelector
                hourValue: hoursTumbler.currentIndex.toString().padStart(2, "0")
                minuteValue: minutesTumbler.currentIndex.toString().padStart(2, "0")

                Connections {
                    target: timeSelector
                    function onTimeApplyClicked(hourValue, minuteValue){
                        hoursTumbler.currentIndex = hourValue
                        minutesTumbler.currentIndex = minuteValue
                    }
                }
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
