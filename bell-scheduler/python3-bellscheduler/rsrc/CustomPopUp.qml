import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


Popup {
    id:popUpWaiting
    width:570
    height:80
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    visible:!mainStackBridge.closePopUp[0]
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
        switch (mainStackBridge.closePopUp[1]){
            case 1:
                var msg=i18nd("bell-scheduler","Loading basic configuration. Wait a moment...");
                break;
            case 2:
                var msg=i18nd("bell-scheduler","Loading bell info. Wait a moment...");
                break;
            case 3:
                var msg=i18nd("bell-scheduler","Validating the data entered. Wait a moment...")
                break;
            case 4:
                var msg=i18nd("bell-scheduler","Saving the data entered. Wait a moment...")
                break;
            case 5:
                var msg=i18nd("bell-scheduler","Activating the bell. Wait a moment...")
                break;
            case 6:
                var msg=i18nd("bell-scheduler","Activating all bells. Wait a moment...")
                break;
            case 7:
                var msg=i18nd("bell-scheduler","Deactivating the bell. Wait a moment...")
                break;
            case 8:
                var msg=i18nd("bell-scheduler","Deactivating all bells. Wait a moment...")
                break;
            case 9:
                var msg=i18nd("bell-scheduler","Removing the bell. Wait a moment...")
                break;
            case 10:
                var msg=i18nd("bell-scheduler","Removing all bells. Wait a moment...")
                break;
            case 11:
                var msg=i18nd("bell-scheduler","Exporting bells configuration. Wait a moment...")
                break;
            case 12:
                var msg=i18nd("bell-scheduler","Loading bells configuration. Wait a moment...")
                break;
            case 13:
                var msg=i18nd("bell-scheduler","Revovering previous bells configuration. Wait a moment...")
                break;
            default:
                var msg=""
                break;
        }
        return msg
    }
}
