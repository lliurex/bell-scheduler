import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Rectangle{
    visible: true
    color:"transparent"

    GridLayout{
        id: loadGrid
        rows: 3
        flow: GridLayout.TopToBottom
        anchors.centerIn:parent

        RowLayout{
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter
            visible:!mainStackBridge.showLoadErrorMessage[0]

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

        RowLayout{
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter
            visible:!mainStackBridge.showLoadErrorMessage[0]

            Text{
                id:loadtext
                text:i18nd("bell-scheduler", "Loading. Wait a moment...")
                font.pointSize: 10
                Layout.alignment:Qt.AlignHCenter
            }
        }
        Kirigami.InlineMessage {
            id: errorLabel
            visible:mainStackBridge.showLoadErrorMessage[0]
            text:getMsgText(mainStackBridge.showLoadErrorMessage[1])
            type:Kirigami.MessageType.Error;
            Layout.minimumWidth:960
            Layout.fillWidth:true
            Layout.rightMargin:15
            Layout.leftMargin:15
        }
    }

    function getMsgText(msgCode){

        switch (msgCode){
            case -25:
                var msg=i18nd("bell-scheduler","Unabled to read bells configuration file")
                break;
            case -37:
                var msg=i18nd("bell-scheduler","Unabled to load bell list due to problems with cron sync")
                break;
            case -38:
                var msg=i18nd("bell-scheduler","Unabled to create a bell with selected file")
                break;
            default:
                var msg=""
                break;
        }
        return msg

    }
}
