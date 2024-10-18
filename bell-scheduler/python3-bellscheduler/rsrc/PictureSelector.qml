import org.kde.kirigami as Kirigami
import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

Popup {

    id:imagePopUp
    property alias customImagePathText:customImagePath.text
    property string selectedImageFile
    property bool imageFileError:false

    width:500
    height:350
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    closePolicy:Popup.NoAutoClose

    background:Rectangle{
        color:"#ebeced"
	border.color:"#b8b9ba"
    }

    contentItem:Rectangle{
        id:container
        width:imagePopUp.width
        height:imagePopUp.height
        color:"transparent"
        Text{ 
            text:i18nd("bell-scheduler","Edit image for bell")
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
                            if (bellStackBridge.bellImage[0]=="stock"){
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
                        currentImgIndex:bellStackBridge.bellImage[1]
                        listEnabled:stockOption.checked
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
                            if (bellStackBridge.bellImage[0]=="custom"){
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
                                    if ((customImagePath.text=="")||(bellStackBridge.bellImage[3])){
                                        applyBtn.enabled=false
                                    }else{
                                        applyBtn.enabled=true
                                    }
                                }
                            }
                        }
                        ButtonGroup.group:imageOptionsGroup
                    }
                    TextField{
                        id:customImagePath
                        text:{
                            if (bellStackBridge.bellImage[0]=="custom"){
                                if (!bellStackBridge.bellImage[3]){
                                    bellStackBridge.bellImage[2].substring(bellStackBridge.bellImage[2].lastIndexOf('/')+1)
                                }else{
                                    ""
                                }
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
            spacing:10

            Button {
                id:applyBtn
                visible:true
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-ok.svg"
                text:i18nd("bell-scheduler","Apply")
                Layout.preferredHeight:40
                enabled:!bellStackBridge.bellImage[3]
                onClicked:{
                    var option=""
                    var tmpPath=""
                    if (stockOption.checked){
                        option="stock"
                    }else{
                        option="custom"
                    }
                    if (selectedImageFile!=""){
                        tmpPath=selectedImageFile
                    }else{
                        tmpPath=bellStackBridge.bellImage[2]
                    }
                    bellStackBridge.updateImageValues([option,imageList.currentImgIndex,tmpPath])
                    restoreInitValues()
                    imageSelector.close()
                }
            }
            
            Button {
                id:cancelBtn
                visible:true
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-cancel.svg"
                text:i18nd("bell-scheduler","Cancel")
                Layout.preferredHeight: 40
                enabled:true
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
        currentFolder:{
            if (selectedImageFile!=""){
                selectedImageFile.substring(0,selectedImageFile.lastIndexOf("/"))
            }else{
                StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
            }

        }
        onAccepted:{
            selectedImageFile=""
            var tmpFile=imgDialog.selectedFile.toString()
            tmpFile=tmpFile.replace(/^(file:\/{2})/,"")
            customImagePath.text=tmpFile.substring(tmpFile.lastIndexOf('/')+1)
            selectedImageFile=tmpFile
            if (!bellStackBridge.checkMimetypeImage(selectedImageFile)){
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

        imageList.currentImgIndex=bellStackBridge.bellImage[1]
        imageFileError=false
        selectedImageFile=""
        messageLabel.visible=""
        applyBtn.enabled=!bellStackBridge.bellImage[3]
        
        if (bellStackBridge.bellImage[0]=="stock"){
            stockOption.checked=true
            customImagePath.text=""
        }else{
            customOption.checked=true
            if (!bellStackBridge.bellImage[3]){
                customImagePath.text=bellStackBridge.bellImage[2].substring(bellStackBridge.bellImage[2].lastIndexOf('/')+1)
            }else{
                customImagePath.text=""
            }
        }

    }
  
}
