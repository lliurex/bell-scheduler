import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: menuItem
    Layout.preferredWidth: 120
    Layout.preferredHeight: 35

    property string optionIcon: ""
    property alias optionText: control.text
    property alias optionPointSize:control.font.pointSize

    signal menuOptionClicked()

    ItemDelegate {
        id: control
        anchors.fill: parent

        icon.name: menuItem.optionIcon
        icon.width: 24
        icon.height: 24
        icon.color: "black"

        background: Rectangle {
            color: control.hovered ? "#add8e6" : "transparent"
        }

        onClicked: menuItem.menuOptionClicked()
    }
}
