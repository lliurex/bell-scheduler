import org.kde.plasma.core 2.1 as PlasmaCore
import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


Rectangle{
    color:"transparent"

    Text{ 
        text:i18nd("bell-scheduler","Edit Bell")
        font.family: "Quattrocento Sans Bold"
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
            visible:true
            text:"Test text"
            type:Kirigami.MessageType.Positive
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
                    checked:bellSchedulerBridge.bellValidityActive
                    enabled:bellSchedulerBridge.enableBellValidity
                    text:i18nd("bell-scheduler","Validity:")
                    font.pointSize: 10
                    focusPolicy: Qt.NoFocus
                    Keys.onReturnPressed: enableValidity.toggled()
                    Keys.onEnterPressed: enableValidity.toggled()
                    onToggled:{
                        bellSchedulerBridge.updateBellValidityActive(checked)
                    }
                   
                }
                Text{
                    id:validityText
                    text:bellSchedulerBridge.bellValidityValue
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
                    hoverEnabled:true
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
                            onClicked:removeValidityDialog.open()
                        }
                    }
                    ValiditySelector{
                        id:validitySelector
                        xPopUp:-Math.round(validitySelector.width-parent.width/2)
                        yPopUp:-Math.round(parent.height*4.55)

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
                    text:bellSchedulerBridge.bellName
                    horizontalAlignment:TextInput.AlignLeft
                    focus:true
                    implicitWidth:400
                }
                Rectangle{
                    id:container
                    width:100
                    height:100
                    border.color: "#ffffff"
                    border.width:5
                    color:"transparent"
   
                    Image{
                        id:bellImg
                        width:80
                        height:80
                        fillMode:Image.PreserveAspectFit
                        source:{
                            if (!bellSchedulerBridge.bellImage[3]){
                                bellSchedulerBridge.bellImage[2]
                            }else{
                                "/usr/lib/python3/dist-packages/bellscheduler/rsrc/image_nodisp.svg"
                            }
                        }
                        clip:true
                        anchors.centerIn:parent
                        MouseArea {
                            id: mouseAreaHour
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: {
                                container.border.color="#add8e6"
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
                            xPopUp:-Math.round(imageSelector.width-parent.width/2)
                            yPopUp:-Math.round(parent.height*4.55)
                            
                        }
                    }
                }

            }
            Text{
                id:sound
                text:i18nd("bell-Scheduler","Current option for sound: ")
                Layout.alignment:Qt.AlignRight
            }
            RowLayout{
                Layout.alignment:Qt.AlignLeft
                spacing:10

                Text{
                    id:soundOption
                    text:{
                        if (bellSchedulerBridge.bellSound[0]=="file"){
                            i18nd("bell-scheduler","Sound file")+": "
                        }else{
                            i18nd("bell-scheduler","Random from directory")+": "
                        }
                    }
                }

                Text{
                    id:soundPath
                    text:getSoundPath()
                    width:400
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
                    hoverEnabled:true
                    onClicked:{
                        soundSelector.open()
                    }
                    SoundSelector{
                        id:soundSelector
                        xPopUp:-Math.round(soundSelector.width-parent.width/2)
                        yPopUp:-Math.round(soundSelector.height)


                    }
                }

            }
            Text{
                id:startOption
                text:i18nd("bell-scheduler","Start in second")+":"
                Layout.alignment:Qt.AlignRight
            }
            RowLayout{
                Layout.alignment:Qt.AlignLeft
                spacing:10

                Text{
                    id:startValue
                    text:bellSchedulerBridge.bellStartIn
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
                    hoverEnabled:true
                    onClicked:editStartForm.open()
                    SliderPopUp{
                        id:editStartForm
                        popUpWidth:300
                        popUpHeight:190
                        xPopUp:Math.round(parent.width/ 2)
                        yPopUp:-Math.round(editStartForm.popUpHeight)
                        headText:i18nd("bell-scheduler","Start in second")
                        footText:""
                        showFoot:false
                        sliderValue:bellSchedulerBridge.bellStartIn
                        Connections{
                            target:editStartForm
                            function onApplyButtonClicked(){
                                bellSchedulerBridge.updateStartInValue(editStartForm.sliderValue)
                                editStartForm.close()
                            }
                            function onCancelButtonClicked(){
                                editStartForm.sliderValue=bellSchedulerBridge.bellStartIn
                                editStartForm.close()
                            }
                        }
                    }
                }

            }
            Text{
                id:durationOption
                text:i18nd("bell-scheduler","Max. duration")+":"
                Layout.alignment:Qt.AlignRight
            }
            RowLayout{
                Layout.alignment:Qt.AlignLeft
                spacing:10

                Text{
                    id:durationValue
                    text:{
                        if (bellSchedulerBridge.bellDuration>0){
                            bellSchedulerBridge.bellDuration+" "+i18nd("bell-scheduler","seconds")
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
                    hoverEnabled:true
                    onClicked:editDurationForm.open()
                    SliderPopUp{
                        id:editDurationForm
                        popUpWidth:350
                        popUpHeight:230
                        xPopUp:Math.round(parent.width/ 2)
                        yPopUp:-Math.round(editDurationForm.popUpHeight)
                        headText:i18nd("bell-scheduler","Max. duration")
                        footText:i18nd("bell-scheduler","(!) If duration is 0, the sound will be reproduced in its entirety")
                        showFoot:true
                        sliderValue:bellSchedulerBridge.bellDuration
                        Connections{
                            target:editDurationForm
                            function onApplyButtonClicked(){
                                bellSchedulerBridge.updateDurationValue(editDurationForm.sliderValue)
                                editDurationForm.close()
                            }
                            function onCancelButtonClicked(){
                                editDurationForm.sliderValue=bellSchedulerBridge.bellDuration
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
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("bell-scheduler","Apply")
            Layout.preferredHeight:40
            enabled:bellSchedulerBridge.changesInBell
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            /*
            onClicked:{
                applyChanges()
                closeTimer.stop()
                wifiControlBridge.applyChanges()
                
            }
            */
        }
        Button {
            id:cancelBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-cancel.svg"
            text:i18nd("bell-scheduler","Cancel")
            Layout.preferredHeight: 40
            enabled:bellSchedulerBridge.changesInBell
            Keys.onReturnPressed: cancelBtn.clicked()
            Keys.onEnterPressed: cancelBtn.clicked()

            onClicked:{
               bellSchedulerBridge.cancelBellChanges()
            }
            
        }
    } 

    ChangesDialog{
        id:settingsChangesDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"Bell-Scheduler"+" - "+i18nd("bell-scheduler","Bell")
        dialogVisible:bellSchedulerBridge.showChangesInBellDialog
        dialogMsg:i18nd("bell-scheduler","The are pending changes to save.\nDo you want save the changes or discard them?")
        dialogWidth:400
        btnAcceptVisible:true
        btnAcceptText:i18nd("bell-scheduler","Apply")
        btnDiscardText:i18nd("bell-scheduler","Discard")
        btnDiscardIcon:"delete.svg"
        btnCancelText:i18nd("bell-scheduler","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
            target:settingsChangesDialog
            function onDialogApplyClicked(){
                bellSchedulerBridge.manageChangesDialog("Accept")
            }
            function onDiscardDialogClicked(){
                bellSchedulerBridge.manageChangesDialog("Discard")           
            }
            function onRejectDialogClicked(){
                closeTimer.stop()
                bellSchedulerBridge.manageChangesDialog("Cancel")       
            }

        }
   }

   ChangesDialog{
        id:removeValidityDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-question.svg"
        dialogTitle:"Bell-Scheduler"+" - "+i18nd("bell-scheduler","Bell")
        dialogMsg:i18nd("bell-scheduler","Are you sure you want to delete the alarm validity?")
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
                bellSchedulerBridge.updateBellValidityValue(["",true])         
           }
           function onRejectDialogClicked(){
                removeValidityDialog.close()       
           }

        }

   }

   function getSoundPath(){

        var tmpPath=""
        tmpPath=bellSchedulerBridge.bellSound[1]
        
        if (tmpPath==""){
            return i18nd("bell-scheduler","<specify the file/url for the sound>")
        }else{
            if (bellSchedulerBridge.bellSound[0]=="file"){
                return tmpPath.substring(tmpPath.lastIndexOf('/')+1)
            }else{
                return tmpPath
            }

        }

    }
   
}