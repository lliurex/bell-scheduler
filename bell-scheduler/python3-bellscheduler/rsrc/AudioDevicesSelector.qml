import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: audioSelectorPopUp
    signal applyButtonClicked

    width: 530
    height: 200
    anchors.centerIn: Overlay.overlay
    modal: true
    focus: true
    closePolicy: Popup.NoAutoClose

    onVisibleChanged: {
        if (visible){
            loadInitValues()
        }
    }

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
        spacing: 12

        Text {
            id: headText
            text: i18nd("bell-scheduler", "Set audio output")
            font.pointSize: 16
            Layout.fillWidth: true
        }

        ColumnLayout {
            id: audioOptions
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 8

            CheckBox {
                id: enableConfiguration
                text: i18nd("bell-scheduler", "Set the default audio ouput to play the alarm")
                checked: bellsOptionsStackBridge.isAudioDeviceConfigurated
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                Layout.alignment: Qt.AlignLeft
            }

            ComboBox {
                id: audioDevicesValues
                textRole: "name"
                valueRole: "value"
                currentIndex: bellsOptionsStackBridge.currentAudioDevice
                model: bellsOptionsStackBridge.audioDevicesModel
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 500

                enabled: enableConfiguration.checked
            }
        }

        RowLayout {
            id: btnBox
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight
            spacing: 12

            Button {
                id: applyBtn
                display: AbstractButton.TextBesideIcon
                icon.name: "dialog-ok"
                text: i18nd("bell-scheduler", "Apply")
                onClicked: {
                    bellsOptionsStackBridge.manageAudioDeviceControl({
                        "active": enableConfiguration.checked,
                        "device": audioDevicesValues.currentIndex
                    })
                    audioSelectorPopUp.close()
                }
            }

            Button {
                id: cancelBtn
                display: AbstractButton.TextBesideIcon
                icon.name: "dialog-cancel" 
                text: i18nd("bell-scheduler", "Cancel")
                onClicked: {
                    audioSelectorPopUp.close()
                }
            }
        }
    }

    function loadInitValues() {
        enableConfiguration.checked = bellsOptionsStackBridge.isAudioDeviceConfigurated
        audioDevicesValues.currentIndex = bellsOptionsStackBridge.currentAudioDevice
    }
}
