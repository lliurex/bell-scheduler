import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


Popup {
    id: popUpWaiting
    width: 570
    height: 100
    anchors.centerIn: Overlay.overlay
    modal: true
    focus: true
    visible: mainStackBridge.showPopUp.show
    closePolicy: Popup.NoAutoClose

    background: Rectangle {
        color: palette.window
        border.color: palette.mid
        radius: 4
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 10

        Image{
            id:spinnerImage
            source: "/usr/lib/python3/dist-packages/bellscheduler/rsrc/loading.png"
            Layout.preferredWidth: 24
            Layout.preferredHeight: 24
            Layout.alignment: Qt.AlignHCenter
            fillMode: Image.PreserveAspectFit
            smooth:false
            antialiasing:false

            rotation:0
        }
            
        Timer{
            id:rotationTimer
            running:(spinnerImage!==null && popUpWaiting!==null) && spinnerImage.visible && popUpWaiting.visible
            repeat:true
            interval:100

            onTriggered:{
                spinnerImage.rotation=(spinnerImage.rotation+330)%360
            }
        }

        Text {
            id: popupText
            text: getTextMessage()
            font.pointSize: 10
            color: palette.windowText
            Layout.alignment: Qt.AlignHCenter
            horizontalAlignment: Text.AlignHCenter
        }
    }

    function getTextMessage(){
        switch (mainStackBridge.showPopUp.msgCode){
            case 1:
                return i18nd("bell-scheduler","Loading basic configuration. Wait a moment...")
            case 2:
                return i18nd("bell-scheduler","Loading bell info. Wait a moment...")
            case 3:
                return i18nd("bell-scheduler","Validating the data entered. Wait a moment...")
            case 4:
                return i18nd("bell-scheduler","Saving the data entered. Wait a moment...")
            case 5:
                return i18nd("bell-scheduler","Activating the bell. Wait a moment...")
            case 6:
                return i18nd("bell-scheduler","Activating all bells. Wait a moment...")
            case 7:
                return i18nd("bell-scheduler","Deactivating the bell. Wait a moment...")
            case 8:
                return i18nd("bell-scheduler","Deactivating all bells. Wait a moment...")
            case 9:
                return i18nd("bell-scheduler","Removing the bell. Wait a moment...")
            case 10:
                return i18nd("bell-scheduler","Removing all bells. Wait a moment...")
            case 11:
                return i18nd("bell-scheduler","Exporting bells configuration. Wait a moment...")
            case 12:
                return i18nd("bell-scheduler","Loading bells configuration. Wait a moment...")
            case 13:
                return i18nd("bell-scheduler","Revovering previous bells configuration. Wait a moment...")
            case 14:
                return i18nd("bell-scheduler","Deactivating holiday control. Wait a moment...")
            case 15:
                return i18nd("bell-scheduler","Activating holiday control. Wait a moment...")
            case 16:
                return i18nd("bell-scheduler","Loading holiday list. Wait a moment...")
            case 17:
                return i18nd("bell-scheduler","Duplicating bell info. Wait a moment...")
            case 18:
                return i18nd("bell-scheduler","Configuring audio output. Wait a moment...")
            default:
                return ""
        }
    }
}
