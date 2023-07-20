import org.kde.plasma.core 2.1 as PlasmaCore
import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Popup {

    id:imagePopUp
    property alias xPopUp:imagePopUp.x
    property alias yPopUp:imagePopUp.y
    property alias customImagePathText:customImagePath.text
    signal applyButtonClicked
    property var imageFileSelected:""
    property bool imageFileError:false

    width:500
    height:350
    x:xPopUp
    y:yPopUp
    /*anchors.centerIn: Overlay.overlay*/
    modal:true
    focus:true
    closePolicy:Popup.NoAutoClose

    Rectangle{
        id:container
        width:imagePopUp.width
        height:imagePopUp.height
        color:"transparent"
        Text{ 
            text:i18nd("bell-scheduler","Image selection")
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 16
        }
        GridLayout{
            id:imageSelectorLayout
            rows:2
            flow: GridLayout.TopToBottom
            rowSpacing:10
            anchors.left:parent.left
            enabled:true
            Kirigami.InlineMessage {
                id: messageLabel
                visible:false
                text:i18nd("bell-scheduler","Image file is not correct")
                type: Kirigami.MessageType.Error
                Layout.minimumWidth:480
                Layout.fillWidth:true
                Layout.topMargin: 40
            }

            GridLayout{
                id: imageOptions
                rows: 2
                flow: GridLayout.TopToBottom
                rowSpacing:10
                Layout.topMargin: messageLabel.visible?0:50
                ButtonGroup{
                    id:imageOptionsGroup
                }
                RowLayout{
                    id:stockRow
                    spacing:10
                    Layout.alignment:Qt.AlignLeft
                    Layout.bottomMargin:10
                    RadioButton{
                        id:stockOption
                        checked:{
                            if (bellSchedulerBridge.bellImage[0]=="stock"){
                                true
                            }else{
                                false
                            }
                        }
                        text:i18nd("bell-scheduler","From stock")
                        onToggled:{
                            if (checked){
                                messageLabel.visible=false
                                applyBtn.enabled=true
                            }
                        }
                        ButtonGroup.group:imageOptionsGroup
                        
                    }
                    ImageList{
                        id:imageList
                        currentImgIndex:bellSchedulerBridge.bellImage[1]
                    }
                }

                RowLayout{
                    id:customRow
                    spacing:10
                    Layout.alignment:Qt.AlignLeft|Qt.AlignVCenter
                    Layout.bottomMargin:10
                    RadioButton{
                        id:customOption
                        checked:{
                            if (bellSchedulerBridge.bellImage[0]=="custom"){
                                true
                            }else{
                                false
                            }
                        }
                        text:i18nd("bell-scheduler","Custom image")
                        onToggled:{
                            if (checked){
                                if (imageFileError){
                                    messageLabel.visible=true
                                    applyBtn.enabled=false
                                }else{
                                    if (customImagePath.text==""){
                                        applyBtn.enabled=false
                                    }else{
                                        applyBtn.enabled=true
                                    }
                                }
                            }
                        }
                        ButtonGroup.group:imageOptionsGroup
                    }
                    /*
                    Text{
                        id:customImagePath 
                        text:{
                            if (bellSchedulerBridge.bellImage[0]=="custom"){
                                bellSchedulerBridge.bellImage[2].substring(bellSchedulerBridge.bellImage[2].lastIndexOf('/')+1)
                            }else{
                                ""
                            }
                        }
                        text:customImagePathText
                        font.family: "Quattrocento Sans Bold"
                        font.pointSize: 10
                        Layout.maximumWidth:250
                        elide:Text.ElideMiddle
                    }
                    */
                    TextField{
                        id:customImagePath
                        text:{
                            if (bellSchedulerBridge.bellImage[0]=="custom"){
                                bellSchedulerBridge.bellImage[2].substring(bellSchedulerBridge.bellImage[2].lastIndexOf('/')+1)
                            }else{
                                ""
                            }
                        }
                        Layout.preferredWidth:250
                        maximumLength:500
                        readOnly:true
                        enabled:customOption.checked?true:false
                    }

                    Button{
                        id:fileSelectorBtn
                        display:AbstractButton.IconOnly
                        icon.name:"insert-image.svg"
                        enabled:customOption.checked?true:false
                        height: 35
                        ToolTip.delay: 1000
                        ToolTip.timeout: 3000
                        ToolTip.visible: hovered
                        ToolTip.text:i18nd("bell-scheduler","Click to select an image")
                        hoverEnabled:true
                        onClicked:imgDialog.open()
                    }
                }
            }
        }
        RowLayout{
            id:btnBox
            anchors.bottom:parent.bottom
            anchors.right:parent.right
            anchors.topMargin:10
            anchors.bottomMargin:25
            anchors.rightMargin:20
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
                onClicked:{
                    imageSelector.close()
                    var option=""
                    if (stockOption.checked){
                        option="stock"
                    }else{
                        option="custom"
                    }
                    bellSchedulerBridge.updateImageValues([option,imageList.currentImgIndex,imageFileSelected])
                }
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
                onClicked:{
                    restoreInitValues()
                    imageSelector.close()
                }
            }

        }
    }


    FileDialog{
        id:imgDialog
        title: "Select and image file"
        folder:{
            if (imageFileSelected!=""){
                shortcuts.imageFileSelected.substring(0,imageFileSelected.lastIndexOf("/"))
            }else{
                shortcuts.home
            }

        }
        onAccepted:{
            imageFileSelected=""
            var tmpFile=imgDialog.fileUrl.toString()
            tmpFile=tmpFile.replace(/^(file:\/{2})/,"")
            customImagePath.text=tmpFile.substring(tmpFile.lastIndexOf('/')+1)
            imageFileSelected=tmpFile
            if (bellSchedulerBridge.checkMimetypeImage(imageFileSelected)){
                messageLabel.visible=true
                applyBtn.enabled=false
                imageFileError=true
            }else{
                messageLabel.visible=false
                applyBtn.enabled=true
                imageFileError=false
            }
        }
      
    }

    function restoreInitValues(){

        imageList.currentImgIndex=bellSchedulerBridge.bellImage[1]
        imageFileError=false
        imageFileSelected=false
        messageLabel.visible=false
        applyBtn.enabled=true
        
        if (bellSchedulerBridge.bellImage[0]=="stock"){
            stockOption.checked=true
            customImagePath.text=""
        }else{
            customOption.checked=true
            customImagePath.text=bellSchedulerBridge.bellImage[2].substring(bellSchedulerBridge.bellImage[2].lastIndexOf('/')+1)
        }

    }
  
}
