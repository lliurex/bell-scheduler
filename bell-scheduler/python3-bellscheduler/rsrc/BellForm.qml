import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Rectangle{
    color:"transparent"

    ColumnLayout{
        id: mainContent
        anchors.fill:parent
        anchors.leftMargin:5
        anchors.rightMargin:15
        anchors.bottomMargin:15
        spacing: 5

        Text{ 
            text:{
                switch(bellStackBridge.actionType){
                    case "add":
                        return i18nd("bell-scheduler","New Bell")
                    case "edit":
                        return i18nd("bell-scheduler","Edit Bell")
                    case "duplicate":
                        return i18nd("bell-scheduler","New Bell (duplicate)")
                }
            }
            font.pointSize: 16
        }
     
        Kirigami.InlineMessage {
            id: messageLabel
            visible:bellStackBridge.showBellFormMessage.show
            text:getMessageText()
            type:Kirigami.MessageType.Error
            Layout.fillWidth:true

        }

        Cron{
            id:scheduler
            Layout.alignment:Qt.AlignHCenter
        }

        RowLayout{
           Layout.alignment:Qt.AlignHCenter

           CheckBox {
                id:enableValidity
                checked:bellStackBridge.bellValidityActive
                enabled:bellStackBridge.enableBellValidity
                text:i18nd("bell-scheduler","Validity:")
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:enableValidity.checked
                        ?i18nd("bell-scheduler","Click to deactive the alarm validity period")
                        :i18nd("bell-scheduler","Click to active the alarm validity period")
                onToggled:{
                    bellStackBridge.updateBellValidityActive(checked)
                }
                   
            }
            
            Text{
                id:validityText
                text:bellStackBridge.bellValidity.value
                font.pointSize:10
            }
            
            Button {
                id:editValidityBtn
                display:AbstractButton.IconOnly
                icon.name:"document-edit"
                enabled:enableValidity.checked && enableValidity.enabled
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:i18nd("bell-scheduler","Click to edit validity")
                onClicked:validityMenu.open()
               
                Menu{
                    id:validityMenu
                    y: editValidityBtn.height
                    x:-(validityMenu.width-editValidityBtn.width/2)

                    MenuItem{
                        icon.name:"document-edit"
                        text:i18nd("bell-scheduler","Edit validity")
                        onClicked:validitySelector.open()
                    }
               
                    MenuItem{
                        icon.name:"delete"
                        text:i18nd("bell-scheduler","Delete validity")
                        enabled:bellStackBridge.bellValidityValue!==""
                        onClicked:removeValidityDialog.open()
                    }
                }
            
            }

        }
        Kirigami.Separator {
            Layout.fillWidth:true
        }
       
        GridLayout{
            id:optionsGrid
            columns:2
            rowSpacing:10
            columnSpacing:10
            Layout.topMargin:5
            Layout.alignment: Qt.AlignHCenter

            Text{
                id:bellName
                text:i18nd("bell-Scheduler","Name:")
                Layout.alignment:Qt.AlignRight | Qt.AlignVCenter
            }

            RowLayout{
                spacing:15

                TextField{
                    id:bellNameEntry
                    text:bellStackBridge.bellName
                    Layout.preferredWidth:400
                    onTextChanged:bellStackBridge.updateBellNameValue(bellNameEntry.text)
                }

                Rectangle{
                    id:container
                    width:80
                    height:80
                    border.color: mouseAreaImg.containsMouse?"#add8e6":"#ffffff"
                    border.width:5
                    color:"transparent"
                    radius:4
   
                    Image{
                        id:bellImg
                        anchors.fill:parent
                        anchors.margins:5
                        fillMode:Image.PreserveAspectFit
                        source:!bellStackBridge.bellImage.error
                                ?bellStackBridge.bellImage.path
                                :"/usr/lib/python3/dist-packages/bellscheduler/rsrc/image_nodisp.svg"

                        ToolTip.delay: 1000
                        ToolTip.timeout: 3000
                        ToolTip.visible:mouseAreaImg.containsMouse
                        ToolTip.text:i18nd("bell-scheduler","Clic to edit the image")
                        MouseArea {
                            id: mouseAreaImg
                            anchors.fill: parent
                            hoverEnabled: true
                            onClicked:imageSelector.open()
     
                        }
                     }
                }
            }

            Text{
                id:sound
                text:i18nd("bell-scheduler","Current option for sound: ")
                Layout.alignment:Qt.AlignRight
            }

            Text{
                id:soundOption
                text:{
                    switch (bellStackBridge.bellSound.option){
                    case "file":
                        return i18nd("bell-scheduler","Sound file")
                    case "directory":
                        return i18nd("bell-scheduler","Random from directory")
                    case "url":
                        return i18nd("bell-scheduler","YouTube url")
                    case "urlslist":
                        return i18nd("bell-scheduler","Random from urls list")
                    }
                }
            }

            Text{

            }

            RowLayout{
                Layout.alignment:Qt.AlignLeft
                Layout.rightMargin:15
                spacing:10

                Text{
                    id:soundPathText
                    text:i18nd("bell-scheduler","Resource:")
                }

                Text{
                    id:soundPath
                    text:getSoundPath()
                    width:400
                    Layout.fillWidth: soundPath.width>scheduler.width?true:false
                    elide:Text.ElideMiddle
                }

                Button {
                    id:editSoundBtn
                    display:AbstractButton.IconOnly
                    icon.name:"document-edit"
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("bell-scheduler","Click to edit sound")
                    onClicked:soundSelector.open()
                  }
            }
    
            Text{
                id:startOption
                text:i18nd("bell-scheduler","Start in second:")
                Layout.alignment:Qt.AlignRight
            }

            RowLayout{
                Layout.alignment:Qt.AlignLeft
                spacing:10

                Text{
                    id:startValue
                    text:bellStackBridge.bellStartIn
                    width:400
                    elide:Text.ElideMiddle
                }

                Button {
                    id:editStartBtn
                    display:AbstractButton.IconOnly
                    icon.name:"document-edit"
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("bell-scheduler","Click to edit start value")
                    onClicked:editStartForm.open()
                    
                }

            }

            Text{
                id:durationOption
                text:i18nd("bell-scheduler","Max. duration:")
                Layout.alignment:Qt.AlignRight
            }

            RowLayout{
                Layout.alignment:Qt.AlignLeft
                spacing:10

                Text{
                    id:durationValue
                    text:bellStackBridge.bellDuration>0
                         ?bellStackBridge.bellDuration+" "+i18nd("bell-scheduler","seconds")
                         :i18nd("bell-scheduler","Full reproduction")
                    width:400
                    elide:Text.ElideMiddle
                }
                Button {
                    id:editDurationBtn
                    display:AbstractButton.IconOnly
                    icon.name:"document-edit"
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("bell-scheduler","Click to edit duration value")
                    onClicked:editDurationForm.open()
                }

            }

        }

        Item {
            Layout.fillHeight:true
        }

        RowLayout{
            id:btnBox
            Layout.alignment: Qt.AlignRight
            spacing:10

            Button {
                id:applyBtn
                visible:true
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-ok"
                text:i18nd("bell-scheduler","Apply")
                enabled:bellStackBridge.changesInBell
                onClicked:{
                    closeTimer.stop()
                    bellStackBridge.applyBellChanges()
                    
                }
            }
            Button {
                id:cancelBtn
                visible:true
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-cancel"
                text:i18nd("bell-scheduler","Cancel")
                enabled:bellStackBridge.changesInBell
                onClicked:{
                   bellStackBridge.cancelBellChanges()
                }
            }
        }
    } 


    ValiditySelector{
        id:validitySelector
    }

    PictureSelector{
        id:imageSelector
    }

    SoundSelector{
        id:soundSelector
    }

    SliderPopUp{
        id:editStartForm
        popUpWidth:370
        popUpHeight:210
        headText:i18nd("bell-scheduler","Edit when the alarm starts")
        footText:""
        showFoot:false
        sliderValue:bellStackBridge.bellStartIn
        Connections{
            target:editStartForm
            function onApplyButtonClicked(){
                bellStackBridge.updateStartInValue(editStartForm.sliderValue)
                editStartForm.close()
            }
            function onCancelButtonClicked(){
                editStartForm.sliderValue=bellStackBridge.bellStartIn
                editStartForm.close()
            }
        }
    }

    SliderPopUp{
        id:editDurationForm
        popUpWidth:350
        popUpHeight:250
        headText:i18nd("bell-scheduler","Edit bell duration")
        footText:i18nd("bell-scheduler","(!) If duration is 0, the sound will be reproduced in its entirety")
        showFoot:true
        sliderValue:bellStackBridge.bellDuration
        Connections{
            target:editDurationForm
            function onApplyButtonClicked(){
                bellStackBridge.updateDurationValue(editDurationForm.sliderValue)
                editDurationForm.close()
            }
            function onCancelButtonClicked(){
                editDurationForm.sliderValue=bellStackBridge.bellDuration
                editDurationForm.close()
            }
        }
    }
    
  
    ChangesDialog{
        id:settingsChangesDialog
        dialogIcon:"dialog-warning"
        dialogVisible:bellStackBridge.showChangesInBellDialog
        dialogMsg:i18nd("bell-scheduler","The are pending changes to save.\nDo you want save the changes or discard them?")
        dialogWidth:400
        btnAcceptVisible:true
        btnAcceptText:i18nd("bell-scheduler","Apply")
        btnDiscardText:i18nd("bell-scheduler","Discard")
        btnDiscardIcon:"delete"
        btnDiscardVisible:true
        btnCancelText:i18nd("bell-scheduler","Cancel")
        btnCancelIcon:"dialog-cancel"
        Connections{
            target:settingsChangesDialog
            function onDialogApplyClicked(){
                bellStackBridge.manageChangesDialog("Accept")
            }
            function onDiscardDialogClicked(){
                bellStackBridge.manageChangesDialog("Discard")           
            }
            function onRejectDialogClicked(){
                closeTimer.stop()
                bellStackBridge.manageChangesDialog("Cancel")       
            }

        }
    }

    ChangesDialog{
        id:removeValidityDialog
        dialogIcon:"dialog-warning"
        dialogMsg:i18nd("bell-scheduler","The alarm validity will be deleted\nDo you want to continue?")
        dialogWidth:400
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("bell-scheduler","Accept")
        btnDiscardIcon:"dialog-ok"
        btnDiscardVisible:true
        btnCancelText:i18nd("bell-scheduler","Cancel")
        btnCancelIcon:"dialog-cancel"
        Connections{
           target:removeValidityDialog
           function onDiscardDialogClicked(){
                removeValidityDialog.close()
                bellStackBridge.updateBellValidityValue({"rangeOption":true,"value":""})         
           }
           function onRejectDialogClicked(){
                removeValidityDialog.close()       
           }

        }

    }

    ChangesDialog{
        id:bellDuplicateDialog
        dialogIcon:"dialog-warning"
        dialogMsg:i18nd("bell-scheduler","There are already alarms programmed for the same time and days.\nDo you wish to continue?")
        dialogVisible:bellStackBridge.showBellDuplicateDialog
        dialogWidth:500
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("bell-scheduler","Yes")
        btnDiscardIcon:"dialog-ok"
        btnDiscardVisible:true
        btnCancelText:i18nd("bell-scheduler","No")
        btnCancelIcon:"dialog-cancel"
        Connections{
           target:bellDuplicateDialog
           function onDiscardDialogClicked(){
                bellStackBridge.manageDuplicateDialog(true)         
           }
           function onRejectDialogClicked(){
                bellStackBridge.manageDuplicateDialog(false)      
           }

        }      

    }

    function getSoundPath(){

        var tmpPath=bellStackBridge.bellSound.path
               
        if (tmpPath===""){
           return i18nd("bell-scheduler","<specify the file/url for the sound>")
        }
        
        if (bellStackBridge.bellSound.option=="file"){
            return tmpPath.substring(tmpPath.lastIndexOf('/')+1)
        }

        return tmpPath
    }

    function getMessageText(){

         switch (bellStackBridge.showBellFormMessage.msgCode){
            case -1:
                return i18nd("bell-scheduler","You must indicate a name for the alarm")
            case -3:
                return i18nd("bell-scheduler","You must indicate sound file")
            case -5:
                return i18nd("bell-scheduler","You must indicate a image file")
            case -7:
                return i18nd("bell-scheduler","You must indicate a directory")
            case -8:
                return i18nd("bell-scheduler","The sound file is not reproducible")
            case -38:
                return i18nd("bell-scheduler","The specified folder does not contain playable files")
            case -41:
                return i18nd("bell-scheduler","Unabled to validated the data")
            case -56:
                return i18nd("bell-scheduler","Days outside the established validity period have been selected")
            default:
                return ""
        }

    }
   
}
