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
                    text:i18nd("bell-scheduler","Validity:")
                    font.pointSize: 10
                    focusPolicy: Qt.NoFocus
                    Keys.onReturnPressed: enableValidity.toggled()
                    Keys.onEnterPressed: enableValidity.toggled()
                   
                }
                Text{
                    id:validityText
                    text:"25/09/2023-31/10/2023"
                    font.pointSize: 10

                }
                Button {
                    id:editValidityBtn
                    display:AbstractButton.IconOnly
                    icon.name:"document-edit.svg"
                    Layout.preferredHeight: 35
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("bell-scheduler","Click to edit validity")
                    hoverEnabled:true
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
                        source:"/usr/share/bell-scheduler/banners/bell.png"
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
                    text:i18nd("bell-scheduler","Sound file")+": "
                }

                Text{
                    id:soundPath
                    text:i18nd("bell-scheduler","<specify the file/url for the sound>")
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
                    text:"0"
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
                        sliderValue:0
                        Connections{
                            target:editStartForm
                            function onApplyButtonClicked(){
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
                    text:"30"+" "+i18nd("bell-scheduler","seconds")
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
                        popUpWidth:450
                        popUpHeight:220
                        xPopUp:Math.round(parent.width/ 2)
                        yPopUp:-Math.round(editDurationForm.popUpHeight)
                        headText:i18nd("bell-scheduler","Max. duration")
                        footText:i18nd("bell-scheduler","(!) If duration is 0, the sound will be reproduced in its entirety")
                        showFoot:true
                        sliderValue:30
                        Connections{
                            target:editDurationForm
                            function onApplyButtonClicked(){
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
            enabled:true
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
            enabled:true
            Keys.onReturnPressed: cancelBtn.clicked()
            Keys.onEnterPressed: cancelBtn.clicked()
            /*
            onClicked:{
                discardChanges()
                closeTimer.stop()
                wifiControlBridge.cancelChanges()
            }
            */
        }
    } 
   
}