import org.kde.kirigami as Kirigami
import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

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
        height:parent.height-120
        enabled:true
        Kirigami.InlineMessage {
            id: messageLabel
            visible:bellsOptionsStackBridge.showMainMessage[0]
            text:getTextMessage(bellsOptionsStackBridge.showMainMessage[1])
            type:getTypeMessage(bellsOptionsStackBridge.showMainMessage[2])
            Layout.minimumWidth:650
            Layout.fillWidth:true
            Layout.topMargin: 40
        }
        
            
        BellsList{
            id:bellsList
            bellsModel:bellsOptionsStackBridge.bellsModel
            Layout.fillHeight:true
            Layout.fillWidth:true
            Layout.topMargin: messageLabel.visible?0:40
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
                    enabled:bellsOptionsStackBridge.enableGlobalOptions
                    onClicked:{
                        
                        backupAction="export"
                        backupFileDialog.title=i18nd("bell-scheduler","Please choose a file to save bells list")
                        backupFileDialog.fileMode=FileDialog.SaveFile
                        
                        if (bellsOptionsStackBridge.showExportBellsWarning){
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
                        backupFileDialog.fileMode=FileDialog.OpenFile
                        importBellDialog.open()

                    }
                }
           
            }
           
        }

        Button {
            id:actionsBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"run-build.svg"
            text:i18nd("bell-scheduler","Global Options")
            Layout.preferredHeight:40
            enabled:bellsOptionsStackBridge.enableGlobalOptions
            onClicked:actionsMenu.open()

            Menu{
                id:actionsMenu
                y: -actionsBtn.height*4
                x: actionsBtn.width/2

                MenuItem{
                    icon.name:"audio-on.svg"
                    text:i18nd("bell-scheduler","Enable alls bells")
                    enabled:!bellsOptionsStackBridge.enableChangeStatusOptions[0]
                    onClicked:bellsOptionsStackBridge.changeBellStatus([true,true])
                }

                MenuItem{
                    icon.name:"audio-volume-muted.svg"
                    text:i18nd("bell-scheduler","Disable all bells")
                    enabled:!bellsOptionsStackBridge.enableChangeStatusOptions[1]
                    onClicked:bellsOptionsStackBridge.changeBellStatus([true,false])
                }

                MenuItem{
                    icon.name:"document-preview-archive.svg"
                    text:i18nd("bell-scheduler","View playback log file")
                    onClicked:bellsOptionsStackBridge.openPlayLogFile()
                }

                MenuItem{
                    icon.name:"document-preview-archive.svg"
                    text:i18nd("bell-scheduler","View error log file")
                    onClicked:bellsOptionsStackBridge.openErrorLogFile()
                }

                MenuItem{
                    icon.name:"delete.svg"
                    text:i18nd("bell-scheduler","Delete alls bells")
                    onClicked:bellsOptionsStackBridge.removeBell([true])
                }
            }
           
        }
        Button {
            id:settingsBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"configure.svg"
            text:i18nd("bell-scheduler","Settings")
            enabled:bellsOptionsStackBridge.enableGlobalOptions
            Layout.preferredHeight:40
            Layout.rightMargin:rectLayout.width-(backupBtn.width+actionsBtn.width+settingsBtn.width+newBtn.width+40)
            onClicked:settingsMenu.open()

            Menu{
               id:settingsMenu
               y: -settingsBtn.height*1.7
               x: settingsBtn.width/2

               MenuItem{
                    icon.name:bellsOptionsStackBridge.isHolidayControlActive?"kt-stop.svg":"kt-start.svg"
                    text:bellsOptionsStackBridge.isHolidayControlActive?i18nd("bell-scheduler","Disable holiday control"):i18nd("bell-scheduler","Enable holiday control")
                    enabled:bellsOptionsStackBridge.enableHolidayControl
                    onClicked:bellsOptionsStackBridge.manageHolidayControl()
                }
                MenuItem{
                    icon.name:"audio-card.svg"
                    text:i18nd("bell-scheduler","Audio output configuration")
                    enabled:bellsOptionsStackBridge.enableAudioDeviceConfiguration
                    onClicked:audioDevicesSelector.open()
                }
            }    
            
            AudioDevicesSelector{
                id:audioDevicesSelector
            }
        }
        Button {
            id:newBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"list-add.svg"
            text:i18nd("bell-scheduler","New bell")
            Layout.preferredHeight:40
            onClicked:bellStackBridge.addNewBell() 
        }
    }

    ChangesDialog{
        id:removeBellDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Bell-Scheduler"+" - "+i18nd("bell-scheduler","Bell List")
        dialogMsg:{
            if (bellsOptionsStackBridge.showRemoveBellDialog[1]){
                i18nd("bell-scheduler","All bells will be deleted.\nDo yo want to continue?")
            }else{
                i18nd("bell-scheduler","The bell will be deleted.\nDo yo want to continue?")
            }
        }
        dialogVisible:bellsOptionsStackBridge.showRemoveBellDialog[0]
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
                bellsOptionsStackBridge.manageRemoveBellDialog('Accept')         
           }
           function onRejectDialogClicked(){
                bellsOptionsStackBridge.manageRemoveBellDialog('Cancel')       
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
        currentFolder:StandardPaths.standardLocations(StandardPaths.HomeLocation)[0]
        nameFilters:["Zip files (*zip)"]
        onAccepted:(selectedPath)=>{
            var selectedPath=""
            selectedPath=backupFileDialog.selectedFile.toString()
            selectedPath=selectedPath.replace(/^(file:\/{2})/,"")
            switch(backupAction){
                case "export":
                    bellsOptionsStackBridge.exportBellsConfig(selectedPath)
                    break;
                case "import":
                    bellsOptionsStackBridge.importBellsConfig(selectedPath)
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
            case -53:
                var msg=i18nd("bell-scheduler","It is not possible to changed audio output")
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
            case 57:
                var msg=i18nd("bell-scheduler","Audio ouput already configurated. Nothing to do")
                break;
            case 58:
                var msg=i18nd("bell-scheduler","Audio output have been changed successfully")
                break;
            case 59:
                var msg=i18nd("bell-scheduler","There is no playback log available")
                break;
            case 60:
                var msg=i18nd("bell-scheduler","There is no error log available")
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
