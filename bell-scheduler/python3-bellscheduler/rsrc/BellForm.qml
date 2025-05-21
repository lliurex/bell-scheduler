import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


Rectangle{
    color:"transparent"

    Text{ 
        text:{
            switch(bellStackBridge.actionType){
                case "add":
                    i18nd("bell-scheduler","New Bell")
                    break;
                case "edit":
                    i18nd("bell-scheduler","Edit Bell")
                    break;
                case "duplicate":
                    i18nd("bell-scheduler","New Bell (duplicate)")
                    break;
            }
        }
        font.pointSize: 16
    }
    
    GridLayout{
        id:generalLayout
        rows:4
        flow: GridLayout.TopToBottom
        rowSpacing:10
        width:parent.width-10
        anchors.horizontalCenter:parent.horizontalCenter
  
        Kirigami.InlineMessage {
            id: messageLabel
            visible:bellStackBridge.showBellFormMessage[0]
            text:getMessageText()
            type:Kirigami.MessageType.Error
            Layout.minimumWidth:650
            Layout.fillWidth:true
            Layout.topMargin: 40
        }

        GridLayout{
            id: schedulerGrid
            rows: 2
            flow: GridLayout.TopToBottom
            rowSpacing:5
            Layout.topMargin: messageLabel.visible?0:40
            Layout.alignment:Qt.AlignHCenter

            Cron{
                id:scheduler
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
                    Keys.onReturnPressed: enableValidity.toggled()
                    Keys.onEnterPressed: enableValidity.toggled()
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:{
                        if (enableValidity.checked){
                            i18nd("bell-scheduler","Click to deactive the alarm validity period")
                        }else{
                            i18nd("bell-scheduler","Click to active the alarm validity period")
                        }
                    }
                    onToggled:{
                        bellStackBridge.updateBellValidityActive(checked)
                    }
                   
                }
                Text{
                    id:validityText
                    text:bellStackBridge.bellValidityValue
                    font.pointSize:10

                }
                Button {
                    id:editValidityBtn
                    display:AbstractButton.IconOnly
                    icon.name:"document-edit.svg"
                    enabled:{
                        if (enableValidity.checked){
                            if (enableValidity.enabled){
                                true
                            }else{
                                false
                            }
                        }else{
                            false
                        }
                    }
                    Layout.preferredHeight: 35
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
                            icon.name:"document-edit.svg"
                            text:i18nd("bell-scheduler","Edit validity")
                            onClicked:validitySelector.open()
                        }
                        MenuItem{
                            icon.name:"delete.svg"
                            text:i18nd("bell-scheduler","Delete validity")
                            enabled:{
                                if (bellStackBridge.bellValidityValue!=""){
                                    true
                                }else{
                                    false
                                }
                            }
                            onClicked:removeValidityDialog.open()
                        }
                    }
                    ValiditySelector{
                        id:validitySelector
                    }
                }

            }

        }
        Rectangle {
            Layout.leftMargin: 15
            Layout.rightMargin:15
            Layout.fillWidth:true
            height: 1
            border.color:"#000000"
            border.width: 5
            radius: 10
        }
       
        GridLayout{
            id:optionsGrid
            columns:2
            flow: GridLayout.LeftToRight
            columnSpacing:5
            Layout.alignment:Qt.AlignHCenter

            Text{
                id:bellName
                text:i18nd("bell-Scheduler","Name:")
                Layout.alignment:Qt.AlignRight
            }
            RowLayout{
                Layout.alignment:Qt.AlignLeft
                spacing:10

                TextField{
                    id:bellNameEntry
                    text:bellStackBridge.bellName
                    horizontalAlignment:TextInput.AlignLeft
                    implicitWidth:400
                    onTextChanged:{
                        bellStackBridge.updateBellNameValue(bellNameEntry.text)
                    }
                }
                Rectangle{
                    id:container
                    width:85
                    height:85
                    border.color: "#ffffff"
                    border.width:5
                    color:"transparent"
   
                    Image{
                        id:bellImg
                        width:65
                        height:65
                        fillMode:Image.PreserveAspectFit
                        source:{
                            if (!bellStackBridge.bellImage[3]){
                                bellStackBridge.bellImage[2]
                            }else{
                                "/usr/lib/python3/dist-packages/bellscheduler/rsrc/image_nodisp.svg"
                            }
                        }
                        ToolTip.delay: 1000
                        ToolTip.timeout: 3000
                        ToolTip.visible:mouseAreaImg.containsMouse?true:false 
                        ToolTip.text:i18nd("bell-scheduler","Clic to edit the image")
                        clip:true
                        anchors.centerIn:parent
                        Keys.onSpacePressed: imageSelector.open()
                        MouseArea {
                            id: mouseAreaImg
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: {
                                container.border.color="#add8e6"
                                focus=true
                            }
                            onExited: {
                                container.border.color="#ffffff"
                            }
                             onClicked:{
                                imageSelector.open()
                            }
                        }

                        ImageSelector{
                            id:imageSelector
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
                    switch (bellStackBridge.bellSound[0]){
                    case "file":
                        i18nd("bell-scheduler","Sound file")
                        break;
                    case "directory":
                        i18nd("bell-scheduler","Random from directory")
                        break;
                    case "url":
                        i18nd("bell-scheduler","YouTube url")
                        break;
                    case "urlslist":
                        i18nd("bell-scheduler","Random from urls list")
                        break;
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
                    Layout.fillWidth:{
                        if (soundPath.width>schedulerGrid.width){
                            true
                        }else{
                            false
                        }
                    }
                    elide:Text.ElideMiddle
                }
                Button {
                    id:editSoundBtn
                    display:AbstractButton.IconOnly
                    icon.name:"document-edit.svg"
                    Layout.preferredHeight: 35
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("bell-scheduler","Click to edit sound")
                    onClicked:{
                       soundSelector.open()
                    }
                    SoundSelector{
                        id:soundSelector
                    }
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
                    icon.name:"document-edit.svg"
                    Layout.preferredHeight: 35
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("bell-scheduler","Click to edit start value")
                    onClicked:editStartForm.open()
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
                    text:{
                        if (bellStackBridge.bellDuration>0){
                            bellStackBridge.bellDuration+" "+i18nd("bell-scheduler","seconds")
                        }else{
                            i18nd("bell-scheduler","Full reproduction")
                        }
                    }
                    width:400
                    elide:Text.ElideMiddle
                }
                Button {
                    id:editDurationBtn
                    display:AbstractButton.IconOnly
                    icon.name:"document-edit.svg"
                    Layout.preferredHeight: 35
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("bell-scheduler","Click to edit duration value")
                    onClicked:editDurationForm.open()
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
                }

            }

        }
       
    }
    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.right:parent.right
        anchors.bottomMargin:15
        anchors.rightMargin:10
        spacing:10

        Button {
            id:applyBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("bell-scheduler","Apply")
            Layout.preferredHeight:40
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
            icon.name:"dialog-cancel.svg"
            text:i18nd("bell-scheduler","Cancel")
            Layout.preferredHeight: 40
            enabled:bellStackBridge.changesInBell
            onClicked:{
               bellStackBridge.cancelBellChanges()
            }
            
        }
    } 

    ChangesDialog{
        id:settingsChangesDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Bell-Scheduler"+" - "+i18nd("bell-scheduler","Bell")
        dialogVisible:bellStackBridge.showChangesInBellDialog
        dialogMsg:i18nd("bell-scheduler","The are pending changes to save.\nDo you want save the changes or discard them?")
        dialogWidth:400
        btnAcceptVisible:true
        btnAcceptText:i18nd("bell-scheduler","Apply")
        btnDiscardText:i18nd("bell-scheduler","Discard")
        btnDiscardIcon:"delete.svg"
        btnDiscardVisible:true
        btnCancelText:i18nd("bell-scheduler","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
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
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Bell-Scheduler"+" - "+i18nd("bell-scheduler","Bell")
        dialogMsg:i18nd("bell-scheduler","The alarm validity will be deleted\nDo you want to continue?")
        dialogWidth:400
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("bell-scheduler","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("bell-scheduler","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
           target:removeValidityDialog
           function onDiscardDialogClicked(){
                removeValidityDialog.close()
                bellStackBridge.updateBellValidityValue(["",true])         
           }
           function onRejectDialogClicked(){
                removeValidityDialog.close()       
           }

        }

   }

   ChangesDialog{
        id:bellDuplicateDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Bell-Scheduler"+" - "+i18nd("bell-scheduler","Bell")
        dialogMsg:i18nd("bell-scheduler","There are already alarms programmed for the same time and days.\nDo you wish to continue?")
        dialogVisible:bellStackBridge.showBellDuplicateDialog
        dialogWidth:500
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("bell-scheduler","Yes")
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("bell-scheduler","No")
        btnCancelIcon:"dialog-cancel.svg"
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

        var tmpPath=""
        tmpPath=bellStackBridge.bellSound[1]
       
        
        if (tmpPath==""){
            tmpPath=i18nd("bell-scheduler","<specify the file/url for the sound>")
        }else{
            if (bellStackBridge.bellSound[0]=="file"){
                tmpPath=tmpPath.substring(tmpPath.lastIndexOf('/')+1)
            }
        }
        return tmpPath

    }

    function getMessageText(){

         switch (bellStackBridge.showBellFormMessage[1]){
            case -1:
                var msg=i18nd("bell-scheduler","You must indicate a name for the alarm");
                break;
            case -3:
                var msg=i18nd("bell-scheduler","You must indicate sound file");
                break;
            case -5:
                var msg=i18nd("bell-scheduler","You must indicate a image file");
                break;
            case -7:
                var msg=i18nd("bell-scheduler","You must indicate a directory");
                break;
            case -8:
                var msg=i18nd("bell-scheduler","The sound file is not reproducible");
                break;
            case -38:
                var msg=i18nd("bell-scheduler","The specified folder does not contain playable files");
                break;
            case -41:
                var msg=i18nd("bell-scheduler","Unabled to validated the data");
                break;
            case -56:
                var msg=i18nd("bell-scheduler","Days outside the established validity period have been selected");
                break;
          
            default:
                var msg=""
                break
        }
        return msg    

    }
   
}
