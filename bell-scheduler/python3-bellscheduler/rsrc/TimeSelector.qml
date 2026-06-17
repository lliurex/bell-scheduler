import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.16 as Kirigami

Popup {
    id: timePopUp

    property alias hourValue: hourEntry.text
    property alias minuteValue: minuteEntry.text

    signal timeApplyClicked(string hour, string minute)

    width: 320
    height: 200
    anchors.centerIn: Overlay.overlay
    modal: true
    focus: true
    closePolicy: Popup.NoAutoClose

    background: Rectangle {
        color: "#ebeced"
        border.color: "#b8b9ba"
        border.width: 1
        radius: 5.0
    }

    contentItem: ColumnLayout {
        id: container
        anchors.fill: parent
        anchors.margins: 15
        spacing: 15

        Text {
            text: i18nd("bell-scheduler", "Edit time for bell")
            font.pointSize: 16
            Layout.fillWidth: true
        }

        RowLayout {
            id: popupTimerLayout
            Layout.alignment: Qt.AlignHCenter
            Layout.fillHeight: true
            spacing: 4

            TextField {
                id: hourEntry
                validator: RegularExpressionValidator { regularExpression: /([0-1][0-9]|2[0-3])/ }
                implicitWidth: 70
                horizontalAlignment: TextInput.AlignHCenter
                color: "#3daee9"
                font.pointSize: 35
            }

            Text {
                font.pointSize: 35
                color: "#3daee9"
                text: ":"
            }

            TextField {
                id: minuteEntry
                validator: RegularExpressionValidator { regularExpression: /[0-5][0-9]/ }
                implicitWidth: 70
                horizontalAlignment: TextInput.AlignHCenter
                color: "#3daee9"
                font.pointSize: 35
            }
        }

        RowLayout {
            id: btnBox
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight
            spacing: 10

            Button {
                id: applyBtn
                display: AbstractButton.TextBesideIcon
                icon.name: "dialog-ok"
                text: i18nd("bell-scheduler", "Apply")

                enabled: true

                onClicked: {
                    if (validateEntry(hourEntry.text, minuteEntry.text)) {
                        timeApplyClicked(hourEntry.text, minuteEntry.text);
                        delay(500, function() {
                            timePopUp.close();
                        });
                    } else {
                        restoreInitValues();
                        timePopUp.close();

                    }
                }
            }

            Button {
                id: cancelBtn
                display: AbstractButton.TextBesideIcon
                icon.name: "dialog-cancel"
                text: i18nd("bell-scheduler", "Cancel")
                onClicked: {
                    restoreInitValues();
                    timePopUp.close();
                }
            }
        }
    }

    function validateEntry(hour, minute) {
        return hour !== "" && minute !== "";
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

    function restoreInitValues() {
        hourEntry.text = formatEditText(bellStackBridge.bellCron.hour);
        minuteEntry.text = formatEditText(bellStackBridge.bellCron.minute);
    }

    function formatEditText(value) {
        return value.toString().padStart(2, "0");
    }
}
