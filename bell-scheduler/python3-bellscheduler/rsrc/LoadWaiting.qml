import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Rectangle{
    visible: true
    color:"transparent"

    ColumnLayout{
        id: loadGrid
        anchors.centerIn: parent
        width: parent.width * 0.9
        spacing: 15
       
        ColumnLayout {
            Layout.alignment: Qt.AlignHCenter
            visible: !mainStackBridge.showLoadErrorMessage.show
            spacing: 10

            AnimatedImage {
                id: loadingGif
                source: "/usr/lib/python3/dist-packages/bellscheduler/rsrc/loading.gif"
                Layout.preferredWidth: 32
                Layout.preferredHeight: 32
                Layout.alignment: Qt.AlignHCenter
                fillMode: Image.PreserveAspectFit
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
