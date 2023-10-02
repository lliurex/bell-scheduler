import org.kde.plasma.core 2.1 as PlasmaCore
import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Rectangle{
    id:rectLayout
    color:"transparent"
    Text{ 
        text:i18nd("bell-scheduler","Configured bells")
        font.pointSize: 16
    }

    property var backupAction:undefined

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
            visible:mainStackBridge.showMainMessage[0]
            text:getTextMessage(mainStackBridge.showMainMessage[1])
            type:getTypeMessage(mainStackBridge.showMainMessage[2])
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
                bellsModel:mainStackBridge.bellsModel
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
                    enabled:mainStackBridge.enableGlobalOptions
                    onClicked:{
                        
                        backupAction="export"
                        backupFileDialog.title=i18nd("bell-scheduler","Please choose a file to save bells list")
                        backupFileDialog.selectExisting=false
                        
                        if (mainStackBridge.showExportBellsWarning){
                           exportBellDialog.open()
                        }else{
                            backupFileDialog.open()
                        }
                    }
                }

                MenuItem{
                    icon.name:"document-import.svg"
                    text:i18nd("bell-scheduler","Import bell backup")
                    onClicked:{

                        backupAction="import"
                        backupFileDialog.title=i18nd("bell-scheduler","Please choose a file to load bells list")
                        backupFileDialog.selectExisting=true
                        importBellDialog.open()

                    }
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
            enabled:mainStackBridge.enableGlobalOptions
            onClicked:actionsMenu.open()
            
            Menu{
                id:actionsMenu
                y: -actionsBtn.height*2.5
                x: actionsBtn.width/2

                MenuItem{
                    icon.name:"audio-on.svg"
                    text:i18nd("bell-scheduler","Enable alls bells")
                    onClicked:mainStackBridge.changeBellStatus([true,true])
                }

                MenuItem{
                    icon.name:"audio-volume-muted.svg"
                    text:i18nd("bell-scheduler","Disable all bells")
                    onClicked:mainStackBridge.changeBellStatus([true,false])

                }

                MenuItem{
                    icon.name:"document-preview-archive.svg"
                    text:i18nd("bell-scheduler","View log file")
                    onClicked:mainStackBridge.openLogFile()
                }

                MenuItem{
                    icon.name:"delete.svg"
                    text:i18nd("bell-scheduler","Delete alls bells")
                    onClicked:mainStackBridge.removeBell([true])
                }
            }
           
        }
        Button {
            id:holidadyBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:mainStackBridge.isHolidayControlEnabled?"kt-stop.svg":"kt-start.svg"
            text:mainStackBridge.isHolidayControlEnabled?i18nd("bell-scheduler","Disable holiday control"):i18nd("bell-scheduler","Enable holiday control")
            Layout.preferredHeight:40
            Layout.rightMargin:rectLayout.width-(backupBtn.width+actionsBtn.width+holidadyBtn.width+newBtn.width+40)
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:mainStackBridge.manageHolidayControl()
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
            onClicked:bellStackBridge.addNewBell() 
        }
    }

    ChangesDialog{
        id:removeBellDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Bell-Scheduler"+" - "+i18nd("bell-scheduler","Bell List")
        dialogMsg:{
            if (mainStackBridge.showRemoveBellDialog[1]){
                i18nd("bell-scheduler","All bells will be deleted.\nDo yo want to continue?")
            }else{
                i18nd("bell-scheduler","The bell will be deleted.\nDo yo want to continue?")
            }
        }
        dialogVisible:mainStackBridge.showRemoveBellDialog[0]
        dialogWidth:300
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("bell-scheduler","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnDiscardVisible:true
        btnCancelText:i18nd("bell-scheduler","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
           target:removeBellDialog
           function onDiscardDialogClicked(){
                mainStackBridge.manageRemoveBellDialog('Accept')         
           }
           function onRejectDialogClicked(){
                mainStackBridge.manageRemoveBellDialog('Cancel')       
           }

        }
    }

    ChangesDialog{
        id:exportBellDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-information.svg"
        dialogTitle:"Bell-Scheduler"+" - "+i18nd("bell-scheduler","Bell List")
        dialogMsg:i18nd("bell-scheduler","Alarms have been detected with random selection of sound files from a folder.\nRemember that this folder will not be included in the export made.\nIf the folder is not saved manually, when the export is restored, the alarms that\nuse it will be deactivated")
        dialogWidth:640
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardVisible:false
        btnCancelText:i18nd("bell-scheduler","Accept")
        btnCancelIcon:"dialog-ok.svg"
        Connections{
           target:exportBellDialog
           function onRejectDialogClicked(){
                exportBellDialog.close()
                backupFileDialog.open()         
           }

        }

    }

     ChangesDialog{
        id:importBellDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Bell-Scheduler"+" - "+i18nd("bell-scheduler","Bell List")
        dialogMsg:i18nd("bell-scheduler","New bells configuration will be loaded and replace the existing configuration.\nDo you want to continue?")
        dialogWidth:600
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardVisible:true
        btnDiscardText:i18nd("bell-scheduler","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("bell-scheduler","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
           target:importBellDialog
           function onDiscardDialogClicked(){
                importBellDialog.close()
                backupFileDialog.open()
           }
           function onRejectDialogClicked(){
                importBellDialog.close()
           }

        }

    }

    FileDialog{
        id:backupFileDialog
        folder:shortcuts.home
        nameFilters:["Zip files (*zip)"]
        onAccepted:{
            var selectedPath=""
            selectedPath=backupFileDialog.fileUrl.toString()
            selectedPath=selectedPath.replace(/^(file:\/{2})/,"")
            switch(backupAction){
                case "export":
                    mainStackBridge.exportBellsConfig(selectedPath)
                    break;
                case "import":
                    mainStackBridge.importBellsConfig(selectedPath)
                    break;
            }

        }
      
    }

    function getTextMessage(msgCode){
        switch (msgCode){
            case -9:
                var msg=i18nd("bell-scheduler","Backup has errors. Unabled to load it")
                break;
            case -12:
                var msg=i18nd("bell-scheduler","Unable to generate backup")
                break
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
            case -36:
                var msg=i18nd("bell-scheduler","Unabled to apply changes due to problems with cron sync")
                break;
            case -37:
                var msg=i18nd("bell-scheduler","Unabled to load bell list due to problems with cron sync")
                break;
            case -48:
                var msg=i18nd("bell-scheduler","It is not possible to activate all bells")
                break;
            case -49:
                var msg=i18nd("bell-scheduler","It is not possible to deactivate all bells")
                break;
            case -52:
                var msg=i18nd("bell-scheduler","It is not possible to remove all bells")
                break;
            case 10:
                var msg=i18nd("bell-scheduler","Backup loaded successfully")
                break;
            case 11:
                var msg=i18nd("bell-scheduler","Backup generated successfully")
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
            case 34:
                var msg=i18nd("bell-scheduler","Holiday control deactivated successfully")
                break
            case 35:
                var msg=i18nd("bell-scheduler","Holiday control activated successfully")
                break
            case 46:
                var msg=i18nd("bell-scheduler","The bells have been activated successfully")
                break;
            case 47:
                var msg=i18nd("bell-scheduler","The bells have been deactivated successfully")
                break;
            case 51:
                var msg=i18nd("bell-scheduler","The bells have been removed successfully")
                break;
            case 53:
                var msg=i18nd("bell-scheduler","Bells already activated. Nothing to do")
                break;
            case 54:
                var msg=i18nd("bell-scheduler","Bells already deactivated. Nothing to do")
                break;
            case 55:
                var msg=i18nd("bell-scheduler","Bells alreday removed. Nothing to do")
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
