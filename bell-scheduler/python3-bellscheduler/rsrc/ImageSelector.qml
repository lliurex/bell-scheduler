import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3
import org.kde.kirigami 2.16 as Kirigami

Popup {

    id:imagePopUp
    property alias customImagePathText:customImagePath.text
    property string selectedImageFile
    property bool imageFileError:false

    width:500
    height:355
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    closePolicy:Popup.NoAutoClose

    background:Rectangle{
        color:"#ebeced"
        border.color:"#b8b9ba"
        border.width:1
        radius:5.0
    }

    contentItem:ColumnLayout{
        id:container
        anchors.fill:parent
        anchors.margins:15
        spacing:12

        Text{ 
            text:i18nd("bell-scheduler","Edit image for bell")
            font.pointSize: 16
        }

        Kirigami.InlineMessage {
            id: messageLabel
            visible:false
            text:i18nd("bell-scheduler","Image file is not correct")
            type: Kirigami.MessageType.Error
            Layout.fillWidth:true
        }
        
        ColumnLayout{
            id:imageSelectorLayout
            Layout.fillHeight:true
            Layout.topMargin:messageLabel.visible?0:10         
            spacing:15

            ButtonGroup{
                id:imageOptionsGroup
            }

            RowLayout{
                id:stockRow
                spacing:10
                Layout.fillWidth:true

                RadioButton{
                    id:stockOption
                    ButtonGroup.group:imageOptionsGroup
                    checked:bellStackBridge.bellImage.option==="stock"
                    text:i18nd("bell-scheduler","From stock")
                    onToggled:{
                        if (checked){
                            messageLabel.visible=false
                            applyBtn.enabled=true
                        }
                    }
                        
                }
                
                ImageList{
                    id:imageList
                    listEnabled:stockOption.checked
                }
            }

             RowLayout{
                 id:customRow
                 spacing:10
                 Layout.fillWidth:true

                 RadioButton{
                    id:customOption
                    ButtonGroup.group:imageOptionsGroup
                    checked:bellStackBridge.bellImage.option==="custom"
                    text:i18nd("bell-scheduler","Custom image")
                    onToggled:{
                        if (checked){
                            if (imageFileError){
                                messageLabel.visible=true
                                applyBtn.enabled=false
                            }else{
                                if ((customImagePath.text=="")||(bellStackBridge.bellImage.error)){
                                    applyBtn.enabled=false
                                }else{
                                    applyBtn.enabled=true
                                }
                            }
                        }
                    }
                }
                
                TextField{
                    id:customImagePath
                    text: (bellStackBridge.bellImage.option==="custom" && !bellStackBridge.bellImage.error)
                          ?bellStackBridge.bellImage.path.substring(bellStackBridge.bellImage.path.lastIndexOf('/')+1)
                          :""
                    Layout.preferredWidth:250
                    maximumLength:500
                    readOnly:true
                    enabled:customOption.checked
                }

                Button{
                    id:fileSelectorBtn
                    display:AbstractButton.IconOnly
                    icon.name:"insert-image"
                    enabled:customOption.checked
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("bell-scheduler","Click to select an image")
                    onClicked:imgDialog.open()
                }
            }
        }

        Item {
            Layout.fillHeight:true
        }

        RowLayout{
            id:btnBox
            Layout.alignment:Qt.AlignRight
            spacing:12

            Button {
                id:applyBtn
                visible:true
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-ok"
                text:i18nd("bell-scheduler","Apply")
                enabled:!bellStackBridge.bellImage.error
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
                        tmpPath=bellStackBridge.bellImage.path
                    }
                    bellStackBridge.updateImageValues({"option":option,"index":imageList.currentImgIndex,"path":tmpPath})
                    restoreInitValues()
                    imageSelector.close()
                }
            }
            
            Button {
                id:cancelBtn
                visible:true
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-cancel"
                text:i18nd("bell-scheduler","Cancel")
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
        folder:(selectedImageFile!=="")
                ? "file://"+selectedImageFile.substring(0,selectedImageFile.lastIndexOf("/"))
                : shortcuts.home
        onAccepted:{
            selectedImageFile=""
            var tmpFile=imgDialog.fileUrl.toString()
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

    onOpened:{
        imageList.currentImgIndex=bellStackBridge.bellImage.index
    
    }

    function restoreInitValues(){

        imageList.currentImgIndex=bellStackBridge.bellImage.index
        imageFileError=false
        selectedImageFile=""
        messageLabel.visible=""
        applyBtn.enabled=!bellStackBridge.bellImage.error
        
        if (bellStackBridge.bellImage.option==="stock"){
            stockOption.checked=true
            customImagePath.text=""
        }else{
            customOption.checked=true
            if (!bellStackBridge.bellImage.error){
                customImagePath.text=bellStackBridge.bellImage.path.substring(bellStackBridge.bellImage.path.lastIndexOf('/')+1)
            }else{
                customImagePath.text=""
            }
        }

    }
  
}
