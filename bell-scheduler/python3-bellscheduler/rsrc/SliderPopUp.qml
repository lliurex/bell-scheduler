import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.plasma.components 3.0 as PC3

Popup {
    id: sliderPopUp

    property alias popUpWidth: sliderPopUp.width
    property alias popUpHeight: sliderPopUp.height
    property string headText: ""
    property string footText: ""
    property alias showFoot: footTextId.visible
    property alias sliderValue: sliderId.value

    signal applyButtonClicked
    signal cancelButtonClicked

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
        id: mainLayout
        anchors.fill: parent
        anchors.margins: 15
        spacing: 15

        Text {
            id: headTextId
            text: sliderPopUp.headText
            font.pointSize: 16
            Layout.fillWidth: true
        }

        ColumnLayout {
            id: controlsArea
            Layout.fillWidth: true
            Layout.fillHeight: true // Absorbe el espacio sobrante del popup
            spacing: 15

            PC3.Slider {
                id: sliderId
                from: 0
                to: 600
                value: 0
                stepSize: 5
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter
                focus: true
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text: i18nd("bell-scheduler", "Drag to change the value")

                onValueChanged: {
                    sliderEntry.text = sliderId.value
                }
            }

            RowLayout {
                id: inputControlsRow
                Layout.alignment: Qt.AlignHCenter
                spacing: 15

                Rectangle {
                    id: removeContainer
                    width: 24
                    height: 24
                    border.color: "transparent"
                    border.width: 1
                    color: "transparent"

                    Text {
                        id: removeText
                        text: "-"
                        font.pointSize: 20
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        anchors.fill: parent
                        ToolTip.delay: 1000
                        ToolTip.timeout: 3000
                        ToolTip.visible: mouseAreaRemove.containsMouse
                        ToolTip.text: i18nd("bell-scheduler", "Click to decrease value")

                        MouseArea {
                            id: mouseAreaRemove
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: removeContainer.border.color = "#add8e6"
                            onExited: {
                                sliderId.forceActiveFocus()
                                removeContainer.border.color = "transparent"
                            }
                            onClicked: {
                                if (sliderId.value > sliderId.from) sliderId.value -= 1
                            }
                        }
                    }
                }

                TextField {
                    id: sliderEntry
                    validator: RegularExpressionValidator { regularExpression: /([0-9][0-9][0-9])/ }
                    implicitWidth: 80
                    text: sliderId.value
                    horizontalAlignment: TextInput.AlignHCenter
                    font.pointSize: 14
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text: i18nd("bell-scheduler", "Enter the value you want")

                    onTextChanged: {
                        timerSlider.restart()
                    }
                }

                Rectangle {
                    id: addContainer
                    width: 24
                    height: 24
                    border.color: "transparent"
                    border.width: 1
                    color: "transparent"

                    Text {
                        id: addText
                        text: "+"
                        font.pointSize: 22
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        anchors.fill: parent
                        ToolTip.delay: 1000
                        ToolTip.timeout: 3000
                        ToolTip.visible: mouseAreaAdd.containsMouse
                        ToolTip.text: i18nd("bell-scheduler", "Click to increase value")

                        MouseArea {
                            id: mouseAreaAdd
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: addContainer.border.color = "#add8e6"
                            onExited: {
                                sliderId.forceActiveFocus()
                                addContainer.border.color = "transparent"
                            }
                            onClicked: {
                                if (sliderId.value < sliderId.to) sliderId.value += 1
                            }
                        }
                    }
                }
            }
        }

        Text {
            id: footTextId
            text: sliderPopUp.footText
            font.pointSize: 10
            visible: showFoot
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
        }

        RowLayout {
            id: actionButtonsRow
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight
            spacing: 12

            Button {
                id: applyBtn
                display: AbstractButton.TextBesideIcon
                icon.name: "dialog-ok"
                text: i18nd("bell-scheduler", "Apply")
                onClicked: {
                    if (sliderEntry.text === "") {
                        sliderEntry.text = sliderId.value
                    }
                    applyButtonClicked()
                }
            }

            Button {
                id: cancelBtn
                display: AbstractButton.TextBesideIcon
                icon.name: "dialog-cancel"
                text: i18nd("bell-scheduler", "Cancel")
                onClicked: {
                    cancelButtonClicked()
                }
            }
        }

        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_Plus) {
                if (sliderId.value < sliderId.to) sliderId.value += 1
                event.accepted = true;
            }
            if (event.key === Qt.Key_Minus) {
                if (sliderId.value > sliderId.from) sliderId.value -= 1
                event.accepted = true;
            }
        }

        Timer {
            id: timerSlider
            interval: 400
            onTriggered: {
                setNewValue()
            }
        }
    }

    function setNewValue() {
        if (sliderEntry.text !== "") {
            var newValue = parseInt(sliderEntry.text)
            if (newValue >= 0 && newValue <= 600) {
                sliderId.value = newValue
            } else {
                if (newValue > 600) {
                    sliderId.value = 600
                }
            }
        } else {
            sliderId.value = 0
        }
    }
}
