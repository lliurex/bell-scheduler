import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.16 as Kirigami

Rectangle{
    visible: true
    color:"transparent"

    ColumnLayout{
        id: loadRoot
        anchors.centerIn: parent
        width: parent.width * 0.9
        spacing: 15
       
        ColumnLayout {
            Layout.alignment: Qt.AlignHCenter
            visible: !mainStackBridge.showLoadErrorMessage.show
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
                running:(spinnerImage!==null && loadRoot!==null) && spinnerImage.visible && loadRoot.visible
                repeat:true
                interval:100

                onTriggered:{
                    spinnerImage.rotation=(spinnerImage.rotation+330)%360
                }
            }

            Text {
                id: loadText
                text: i18nd("bell-scheduler", "Loading. Wait a moment...")
                font.pointSize: 10
                color: palette.windowText
                Layout.alignment: Qt.AlignHCenter
            }
        }

        Kirigami.InlineMessage {
            id: errorLabel
            visible: mainStackBridge.showLoadErrorMessage.show
            text: getMsgText(mainStackBridge.showLoadErrorMessage.msgCode)
            type: Kirigami.MessageType.Error
            Layout.fillWidth: true

        }

    }

    function getMsgText(msgCode){

        switch (msgCode){
            case -25:
                return i18nd("bell-scheduler","Unabled to read bells configuration file")
            case -37:
                return i18nd("bell-scheduler","Unabled to load bell list due to problems with cron sync")
            case -38:
                return i18nd("bell-scheduler","Unabled to create a bell with selected file")
            default:
                return ""
        }
    }
}
