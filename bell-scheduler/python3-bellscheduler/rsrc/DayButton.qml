import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: dayBtnItem

    Layout.preferredWidth: 100
    Layout.preferredHeight: 40

    property alias dayBtnChecked: dayBtn.checked
    property alias dayBtnText: dayBtn.text

    property bool layoutEnabled: true

    signal dayBtnClicked(bool value)

    Button {
        id: dayBtn
        anchors.fill: parent
        checkable: true
        checked: dayBtnChecked
        text: dayBtnText
        focusPolicy: Qt.NoFocus

        onCheckedChanged: {
            dayBtnItem.dayBtnClicked(checked)
        }

        contentItem: Label {
            text: dayBtn.text
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            color: dayBtnItem.paletteBtnText(dayBtn.checked)
        }

        background: Rectangle {
            radius: 5

            color: dayBtnItem.paletteBtn(dayBtn.checked, dayBtn.hovered)

            border.color: dayBtn.hovered ? "#3daee9" : "#d2d2d3"
            border.width: 1
        }
    }

    function paletteBtn(status, isHovered = false) {
        if (dayBtnItem.layoutEnabled) { 
            if (status) {
                return isHovered ? "#add8e6" : "#3daee9";
            } else {
                return isHovered ? "#eeeeee" : "#ffffff";
            }
        } else {
            return status ? "#87cefa" : "#e4e5e7";
        }
    }

    function paletteBtnText(status) {
        if (dayBtnItem.layoutEnabled) {
            return status ? "#ffffff" : "#000000";
        } else {
            return status ? "#ffffff" : "#b9babc";
        }
    }
}
