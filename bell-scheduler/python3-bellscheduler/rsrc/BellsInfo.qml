import org.kde.plasma.core 2.1 as PlasmaCore
import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle{
    id:rectLayout
    Text{ 
        text:i18nd("bell-scheduler","Configured bells")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout{
        id:generalBellsLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        anchors.left:parent.left
        width:parent.width-10
        height:parent.height-90
        enabled:true
        Kirigami.InlineMessage {
            id: messageLabel
            visible:bellSchedulerBridge.showMainMessage[0]
            text:getTextMessage(bellSchedulerBridge.showMainMessage[1])
            type:getTypeMessage(bellSchedulerBridge.showMainMessage[2])
            Layout.minimumWidth:650
            Layout.fillWidth:true
            Layout.topMargin: 40
        }

        GridLayout{
            id: optionsGrid
            rows: 1
            flow: GridLayout.TopToBottom
            rowSpacing:10
            Layout.topMargin: messageLabel.visible?0:40
            
            BellsList{
                id:bellsList
                bellsModel:bellSchedulerBridge.bellsModel
                Layout.fillHeight:true
                Layout.fillWidth:true
            }
        }
    }
    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.fill:parent.fill
        anchors.bottomMargin:15
        spacing:10

        Button {
            id:backupBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"backup.svg"
            text:i18nd("bell-scheduler","Backup")
            Layout.preferredHeight:40
            onClicked:backupMenu.open()
            
            Menu{
                id:backupMenu
                y: -backupBtn.height*1.7
                x: backupBtn.width/2

                MenuItem{
                    icon.name:"document-export.svg"
                    text:i18nd("bell-scheduler","Generate bell backup")
                }

                MenuItem{
                    icon.name:"document-import.svg"
                    text:i18nd("bell-scheduler","Import bell backup")
                }
           
            }
           
        }

        Button {
            id:actionsBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"configure.svg"
            text:i18nd("bell-scheduler","Global Options")
            Layout.preferredHeight:40
            Layout.rightMargin:rectLayout.width-(backupBtn.width+actionsBtn.width+newBtn.width+30)
            onClicked:actionsMenu.open()
            
            Menu{
                id:actionsMenu
                y: -actionsBtn.height*2.5
                x: actionsBtn.width/2

                MenuItem{
                    icon.name:"audio-on.svg"
                    text:i18nd("bell-scheduler","Enable alls bells")
                }

                MenuItem{
                    icon.name:"audio-volume-muted.svg"
                    text:i18nd("bell-scheduler","Disable all bells")
                }

                MenuItem{
                    icon.name:"delete.svg"
                    text:i18nd("bell-scheduler","Delete alls bells")
                }
            }
           
        }
        Button {
            id:newBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"list-add.svg"
            text:i18nd("bell-scheduler","New bell")
            Layout.preferredHeight:40
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:bellSchedulerBridge.addNewBell() 
        }
    }

    CustomPopUp{
        id:loadBellForm
    }

    function getTextMessage(msgCode){
        switch (msgCode){
            case -31:
                var msg=i18nd("bell-scheduler","Detected alarms with errors")
                break;
            default:
                var msg=""
                break;
        }
        return msg
    } 

    function getTypeMessage(msgType){

        switch (msgType){
            case "Information":
                return Kirigami.MessageType.Information
            case "Ok":
                return Kirigami.MessageType.Positive
            case "Error":
                return Kirigami.MessageType.Error
            case "Warning":
                return Kirigami.MessageType.Warning
        }
    }

} 
