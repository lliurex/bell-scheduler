import org.kde.kirigami as Kirigami
import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

Popup {

    id:soundPopUp
    property string selectedSoundFile
    property string selectedSoundFolder
    property bool soundFileError:false

    width:580
    height:400
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
            text:i18nd("bell-scheduler","Edit sound for bell")
            font.pointSize: 16
        }

        Kirigami.InlineMessage {
            id: messageLabel
            visible:false
            text:i18nd("bell-scheduler","Sound file is not correct")
            type: Kirigami.MessageType.Error
            Layout.fillWidth:true
        }
        
        ColumnLayout{
            id:soundSelectorLayout
            Layout.fillWidth:true
            Layout.fillHeight:true
            Layout.topMargin:messageLabel.visible?0:10         
            spacing:12
           
            ButtonGroup{
                id:soundOptionsGroup
            }

            RowLayout{
                id:fileRow
                spacing:10
                Layout.fillWidth:true

                RadioButton{
                    id:fileOption
                    checked:bellStackBridge.bellSound.option==="file"
                    ButtonGroup.group:soundOptionsGroup

                    onToggled:{
                        if (checked){
                            if (soundFileError){
                                messageLabel.visible=true
                                applyBtn.enabled=false
                            }else{
                                if ((filePath.text=="")||(bellStackBridge.bellSound.error)){
                                    applyBtn.enabled=false
                                }else{
                                    applyBtn.enabled=true
                                }
                            }
                        }
                    }
                }
                
                TextField{
                    id:filePath 
                    text: (bellStackBridge.bellSound.option==="file" && !bellStackBridge.bellSound.error)
                          ?bellStackBridge.bellSound.path.substring(bellStackBridge.bellSound.path.lastIndexOf('/')+1)
                          : ""
               
                    Layout.preferredWidth:250
                    maximumLength:500
                    readOnly:true
                    enabled:fileOption.checked?true:false
                }
                
                Button{
                    id:fileSelectorBtn
                    display:AbstractButton.IconOnly
                    icon.name:"audio-x-mpeg"
                    enabled:fileOption.checked?true:false
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("bell-scheduler","Click to select a sound file")
                    onClicked:soundFileDialog.open()
                }
                    
            }

            RowLayout{
                id:folderRow
                spacing:10
                Layout.fillWidth:true

                RadioButton{
                    id:directoryOption
                    checked:bellStackBridge.bellSound.option==="directory"
                    ButtonGroup.group:soundOptionsGroup
                    text:i18nd("bell-scheduler","Random from directory")
                    
                    onToggled:{
                        if (checked){
                            messageLabel.visible=false
                            if ((folderPath.text=="")||(bellStackBridge.bellSound.error)){
                                applyBtn.enabled=false
                            }else{
                                applyBtn.enabled=true
                            }
                        }
                    }
                }
                
                TextField{
                    id:folderPath 
                    text:(bellStackBridge.bellSound.option==="directory" && !bellStackBridge.bellSound.error)
                         ?bellStackBridge.bellSound.path
                         :""
                              
                    Layout.preferredWidth:250
                    maximumLength:500
                    readOnly:true
                    enabled:directoryOption.checked?true:false
                }

                Button{
                    id:folderSelectorBtn
                    display:AbstractButton.IconOnly
                    icon.name:"view-media-playlist"
                    enabled:directoryOption.checked
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible: hovered
                    ToolTip.text:i18nd("bell-scheduler","Click to select a folder")
                    onClicked:soundFolderDialog.open()
                }
            }
            
            CheckBox {
                id:soundDefaultPath
                text:i18nd("bell-scheduler","Copy the sound file to the internal folder (*)")
                checked:bellStackBridge.bellSound.defaultPath
                enabled:fileOption.checked?true:false
                font.pointSize: 10
                focusPolicy: Qt.NoFocus
                Layout.fillWidth:true
            }
            
            Text{ 
                id:footText
                text:i18nd("bell-scheduler","(*) Checking this option the sound file will be copied to the internal folder.It will be this file that is used to reproduce the alarm. In addition, if alarms are exported the file will be included in the export. It is recommended to mark it")
                font.pointSize: 10
                Layout.preferredWidth:480
                wrapMode: Text.WordWrap
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
                enabled:!bellStackBridge.bellSound.error
                onClicked:{
                    var option=""
                    var tmpPath=""
                    if (fileOption.checked){
                        option="file"
                        if (selectedSoundFile!=""){
                            tmpPath=selectedSoundFile
                        }else{
                            tmpPath=bellStackBridge.bellSound.path
                        }
                    }else{
                        option="directory"
                        if (selectedSoundFolder!=""){
                            tmpPath=selectedSoundFolder
                        }else{
                            tmpPath=bellStackBridge.bellSound.path
                        }
                    }
                    bellStackBridge.updateSoundValues({"option":option,"path":tmpPath,"defaultPath":soundDefaultPath.checked})
                    restoreInitValues()
                    soundSelector.close()
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
                    soundSelector.close()
                }                
            }

        }
    }


    FileDialog{
        id:soundFileDialog
        title: "Select a sound file"
        currentFolder:{
            if (selectedSoundFile!==""){
                return Qt.resolvedUrl(selectedSoundFile.substring(0,selectedSoundFile.lastIndexOf("/")))
            }else{
               return StandardPaths.standardLocations(StandardPaths.MusicLocation)[0]
            }

        }
        onAccepted:{
            selectedSoundFile=""
            selectedSoundFile=soundFileDialog.selectedFile.toString()
            selectedSoundFile=selectedSoundFile.replace(/^(file:\/{2})/,"")
            filePath.text=selectedSoundFile.substring(selectedSoundFile.lastIndexOf('/')+1)
            if (!bellStackBridge.checkMimetypeSound(selectedSoundFile)){
                messageLabel.visible=true
                applyBtn.enabled=false
                soundFileError=true
            }else{
                messageLabel.visible=false
                applyBtn.enabled=true
                soundFileError=false
            }
        }
      
    }
    FolderDialog{
        id:soundFolderDialog
        title: "Select a folder"
        currentFolder:{
            if (selectedSoundFolder!==""){
               return selectedSoundFolder
            }else{
               return StandardPaths.standardLocations(StandardPaths.MusicLocation)[0]
            }
        }
        onAccepted:{
	    selectedSoundFolder=""
            selectedSoundFolder=soundFolderDialog.selectedFolder.toString()
            selectedSoundFolder=selectedSoundFolder.replace(/^(file:\/{2})/,"")
	    folderPath.text=selectedSoundFolder
            messageLabel.visible=false
            applyBtn.enabled=true
        }
      
    }

    function restoreInitValues(){

        soundFileError=false
        selectedSoundFile=""
        selectedSoundFolder=""
        messageLabel.visible=false
        soundDefaultPath.checked=bellStackBridge.bellSound.defaultPath
        applyBtn.enabled=!bellStackBridge.bellSound.error
        
        if (bellStackBridge.bellSound.option==="file"){
            fileOption.checked=true
            folderPath.text=""
            if (!bellStackBridge.bellSound.error){
                filePath.text=bellStackBridge.bellSound.path.substring(bellStackBridge.bellSound.path.lastIndexOf('/')+1)
            }else{
                filePath.text=""
            }
        }else{
            directoryOption.checked=true
            filePath.text=""
            if (!bellStackBridge.bellSound.error){
                folderPath.text=bellStackBridge.bellSound.path
            }else{
                folderPath.text=""
            }
        }

    }
  
}
