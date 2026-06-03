import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Popup {
    id:popUpWaiting
    width:570
    height:80
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    visible:mainStackBridge.showPopUp.show
    closePolicy:Popup.NoAutoClose

    GridLayout{
        id: popupGrid
        rows: 2
        flow: GridLayout.TopToBottom
        anchors.centerIn:parent


        RowLayout {
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter
            Rectangle{
                color:"transparent"
                width:30
                height:30
                AnimatedImage{
                    source: "/usr/lib/python3/dist-packages/bellscheduler/rsrc/loading.gif"
                    transform: Scale {xScale:0.45;yScale:0.45}
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter

            Text{
                id:popupText
                text:getTextMessage()
                font.pointSize: 10
                Layout.alignment:Qt.AlignHCenter
            }
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
