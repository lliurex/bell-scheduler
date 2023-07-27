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

    ChangesDialog{
        id:removeBellDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-question.svg"
        dialogTitle:"Bell-Scheduler"+" - "+i18nd("bell-scheduler","Bell")
        dialogMsg:i18nd("bell-scheduler","Do you want delete the bell?")
        dialogVisible:bellSchedulerBridge.showRemoveBellDialog
        dialogWidth:400
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("bell-scheduler","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("bell-scheduler","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
           target:removeBellDialog
           function onDiscardDialogClicked(){
                bellSchedulerBridge.manageRemoveBellDialog('Accept')         
           }
           function onRejectDialogClicked(){
                bellSchedulerBridge.manageRemoveBellDialog('Cancel')       
           }

        }
    }

    function getTextMessage(msgCode){
        switch (msgCode){
            case -19:
                var msg=i18nd("bell-scheduler","Unabled to edit the Bell due to problems with cron sync")
                break;
            case -20:
                var msg=i18nd("bell-scheduler","Unabled to create the Bell due to problems with cron sync")
                break;
            case -21:
                var msg=i18nd("bell-scheduler","Unabled to delete the Bell due to problems with cron sync")
                break;
            case -22:
                var msg=i18nd("bell-scheduler","Unabled to activate the Bell due to problems with cron sync")
                break;
            case -23:
                var msg=i18nd("bell-scheduler","Unabled to deactivate the Bell due to problems with cron sync")
                break;
            case -24:
                var msg=i18nd("bell-scheduler","Unabled to copy image and/or sound file to work directory")
                break;
            case -31:
                var msg=i18nd("bell-scheduler","Detected alarms with errors")
                break;
            case 14:
                var msg=i18nd("bell-scheduler","Bell deleted successfully")
                break;
            case 15:
                var msg=i18nd("bell-scheduler","Bell edited successfully")
                break;
            case 16:
                var msg=i18nd("bell-scheduler","Bell activated successfully")
                break;
            case 17:
                var msg=i18nd("bell-scheduler","Bell deactivated successfully")
                break;
            case 18:
                var msg=i18nd("bell-scheduler","Bell created successfully")
                break
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
