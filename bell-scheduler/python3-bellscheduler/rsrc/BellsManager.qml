import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import org.kde.kirigami as Kirigami

Rectangle{
    id:rectLayout
    color:"transparent"

    ColumnLayout{
        id: mainContent
        anchors.top:parent.top
        anchors.left:parent.left
        anchors.right:parent.right
        anchors.bottom:btnBox.top

        anchors.leftMargin:5
        anchors.rightMargin:15
        anchors.bottomMargin:25
        spacing: 10

        property var backupAction:undefined

        Text{ 
            text:i18nd("bell-scheduler","Configured bells")
            font.pointSize: 16
        }

        Kirigami.InlineMessage {
            id: messageLabel
            visible:bellsOptionsStackBridge.showMainMessage.show
            text:getTextMessage(bellsOptionsStackBridge.showMainMessage.msgCode)
            type:getTypeMessage(bellsOptionsStackBridge.showMainMessage.type)
            Layout.fillWidth:true
        }
               
        BellsList{
            id:bellsList
            bellsModel:bellsOptionsStackBridge.bellsModel
            Layout.fillHeight:true
            Layout.fillWidth:true
        }
    }
    
    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin:5
        anchors.topMargin:20
        anchors.margins:15
        spacing: 30

        Button {
            id:backupBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"backup"
            text:i18nd("bell-scheduler","Backup")
            onClicked:backupMenu.open()
            
            Menu{
                id:backupMenu
                y: -height - 5
                x: backupBtn.width/2

                MenuItem{
                    icon.name:"document-export"
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
                    icon.name:"document-import"
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
            icon.name:"run-build"
            text:i18nd("bell-scheduler","Global Options")
            enabled:bellsOptionsStackBridge.enableGlobalOptions
            onClicked:actionsMenu.open()

            Menu{
                id:actionsMenu
                y: -height - 5
                x: actionsBtn.width/2

                MenuItem{
                    icon.name:"audio-on"
                    text:i18nd("bell-scheduler","Enable alls bells")
                    enabled:!bellsOptionsStackBridge.enableChangeStatusOptions.allActivated
                    onClicked:bellsOptionsStackBridge.changeBellStatus({"allBells":true,"active":true})
                }

                MenuItem{
                    icon.name:"audio-volume-muted"
                    text:i18nd("bell-scheduler","Disable all bells")
                    enabled:!bellsOptionsStackBridge.enableChangeStatusOptions.allDeactivated
                    onClicked:bellsOptionsStackBridge.changeBellStatus({"allBells":true,"active":false})
                }

                MenuItem{
                    icon.name:"document-preview-archive"
                    text:i18nd("bell-scheduler","View playback log file")
                    onClicked:bellsOptionsStackBridge.openPlayLogFile()
                }

                MenuItem{
                    icon.name:"document-preview-archive"
                    text:i18nd("bell-scheduler","View error log file")
                    onClicked:bellsOptionsStackBridge.openErrorLogFile()
                }

                MenuItem{
                    icon.name:"delete"
                    text:i18nd("bell-scheduler","Delete alls bells")
                    onClicked:bellsOptionsStackBridge.removeBell({"allBells":true,"bellId":""})
                }
            }
           
        }

        Button {
            id:settingsBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"configure"
            text:i18nd("bell-scheduler","Settings")
            enabled:bellsOptionsStackBridge.enableGlobalOptions
            onClicked:settingsMenu.open()

            Menu{
               id:settingsMenu
               y: -height - 5
               x: settingsBtn.width/2

               MenuItem{
                    icon.name:bellsOptionsStackBridge.isHolidayControlActive?"kt-stop.svg":"kt-start"
                    text:bellsOptionsStackBridge.isHolidayControlActive?i18nd("bell-scheduler","Disable holiday control"):i18nd("bell-scheduler","Enable holiday control")
                    enabled:bellsOptionsStackBridge.enableHolidayControl
                    onClicked:bellsOptionsStackBridge.manageHolidayControl()
                }
                MenuItem{
                    icon.name:"audio-card"
                    text:i18nd("bell-scheduler","Audio output configuration")
                    enabled:bellsOptionsStackBridge.enableAudioDeviceConfiguration
                    onClicked:audioDevicesSelector.open()
                }
            }    
            
            AudioDevicesSelector{
                id:audioDevicesSelector
            }
        }

        Item{
            Layout.fillWidth:true
        }

        Button {
            id:newBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"list-add"
            text:i18nd("bell-scheduler","New bell")
            onClicked:bellStackBridge.addNewBell() 
        }
    }

    ChangesDialog{
        id:removeBellDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogMsg:bellsOptionsStackBridge.showRemoveBellDialog.removeAll
                  ?i18nd("bell-scheduler","All bells will be deleted.\nDo yo want to continue?")
                  :i18nd("bell-scheduler","The bell will be deleted.\nDo yo want to continue?")
       
        dialogVisible:bellsOptionsStackBridge.showRemoveBellDialog.show
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
                    
                case "import":
                    bellsOptionsStackBridge.importBellsConfig(selectedPath)
                    
            }

        }
      
    }

    function getTextMessage(msgCode){
        switch (msgCode){
            case -9:
                return i18nd("bell-scheduler","Backup has errors. Unabled to load it")
            case -12:
                return i18nd("bell-scheduler","Unable to generate backup")
            case -19:
                return i18nd("bell-scheduler","Unabled to edit the Bell due to problems with cron sync")
            case -20:
                return i18nd("bell-scheduler","Unabled to create the Bell due to problems with cron sync")
            case -21:
                return i18nd("bell-scheduler","Unabled to delete the Bell due to problems with cron sync")
            case -22:
                return i18nd("bell-scheduler","Unabled to activate the Bell due to problems with cron sync")
            case -23:
                return i18nd("bell-scheduler","Unabled to deactivate the Bell due to problems with cron sync")
            case -24:
                return i18nd("bell-scheduler","Unabled to copy image and/or sound file to work directory")
            case -31:
                return i18nd("bell-scheduler","Detected alarms with errors")
            case -36:
                return i18nd("bell-scheduler","Unabled to apply changes due to problems with cron sync")
            case -37:
                return i18nd("bell-scheduler","Unabled to load bell list due to problems with cron sync")
            case -48:
                return i18nd("bell-scheduler","It is not possible to activate all bells")
            case -49:
                return i18nd("bell-scheduler","It is not possible to deactivate all bells")
            case -52:
                return i18nd("bell-scheduler","It is not possible to remove all bells")
            case -53:
                return i18nd("bell-scheduler","It is not possible to changed audio output")
            case -60:
                return i18nd("bell-scheduler","Unable to activate bell. There are no scheduled days")
            case 10:
                return i18nd("bell-scheduler","Backup loaded successfully")
            case 11:
                return i18nd("bell-scheduler","Backup generated successfully")
            case 14:
                return i18nd("bell-scheduler","Bell deleted successfully")
            case 15:
                return i18nd("bell-scheduler","Bell edited successfully")
            case 16:
                return i18nd("bell-scheduler","Bell activated successfully")
            case 17:
                return i18nd("bell-scheduler","Bell deactivated successfully")
            case 18:
                return i18nd("bell-scheduler","Bell created successfully")
            case 34:
                return i18nd("bell-scheduler","Holiday control deactivated successfully")
            case 35:
                return i18nd("bell-scheduler","Holiday control activated successfully")
            case 46:
                return i18nd("bell-scheduler","The bells have been activated successfully")
            case 47:
                return i18nd("bell-scheduler","The bells have been deactivated successfully")
            case 51:
                return i18nd("bell-scheduler","The bells have been removed successfully")
            case 53:
                return i18nd("bell-scheduler","Bells already activated. Nothing to do")
            case 54:
                return i18nd("bell-scheduler","Bells already deactivated. Nothing to do")
            case 55:
                return i18nd("bell-scheduler","Bells alreday removed. Nothing to do")
            case 57:
                return i18nd("bell-scheduler","Audio ouput already configurated. Nothing to do")
            case 58:
                return i18nd("bell-scheduler","Audio output have been changed successfully")
            case 59:
                return i18nd("bell-scheduler","There is no playback log available")
            case 60:
                return i18nd("bell-scheduler","There is no error log available")
            default:
                return ""
        }
    } 

    function getTypeMessage(msgType){

        switch(msgType){
            case 0:
                return Kirigami.MessageType.Positive
            case 1:
                return Kirigami.MessageType.Error
            case 2:
                return Kirigami.MessageType.Warning
            case 3:
            default:
                return Kirigami.MessageType.Information
        }
    }

} 
