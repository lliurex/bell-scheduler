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
        radius:0,5
    }

    contentItem:Rectangle{
        id:container
        width:soundPopUp.width
        height:soundPopUp.height
        color:"transparent"
        Text{ 
            text:i18nd("bell-scheduler","Edit sound for bell")
            font.pointSize: 16
        }
        GridLayout{
            id:soundSelectorLayout
            rows:2
            flow: GridLayout.TopToBottom
            rowSpacing:10
            anchors.left:parent.left
            enabled:true
            Kirigami.InlineMessage {
                id: messageLabel
                visible:false
                text:i18nd("bell-scheduler","Sound file is not correct")
                type: Kirigami.MessageType.Error
                Layout.minimumWidth:560
                Layout.fillWidth:true
                Layout.topMargin: 40
            }

            GridLayout{
                id: soundOptions
                rows: 4
                flow: GridLayout.TopToBottom
                rowSpacing:10
                Layout.topMargin: messageLabel.visible?0:50
                ButtonGroup{
                    id:soundOptionsGroup
                }
                RowLayout{
                    id:fileRow
                    spacing:10
                    Layout.alignment:Qt.AlignLeft
                    Layout.bottomMargin:10
                    RadioButton{
                        id:fileOption
                        checked:{
                            if (bellStackBridge.bellSound[0]=="file"){
                                true
                            }else{
                                false
                            }
                        }
                        text:i18nd("bell-scheduler","Sound file")
                        onToggled:{
                            if (checked){
                                if (soundFileError){
                                    messageLabel.visible=true
                                    applyBtn.enabled=false
                                }else{
                                    if ((filePath.text=="")||(bellStackBridge.bellSound[2])){
                                        applyBtn.enabled=false
                                    }else{
                                        applyBtn.enabled=true
                                    }
                                }
                            }
                        }
                        ButtonGroup.group:soundOptionsGroup
                        
                    }
                    TextField{
                        id:filePath 
                        text:{
                            if (bellStackBridge.bellSound[0]=="file"){
                                if (!bellStackBridge.bellSound[2]){
                                    bellStackBridge.bellSound[1].substring(bellStackBridge.bellSound[1].lastIndexOf('/')+1)
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
                        enabled:fileOption.checked?true:false
                    }
                    Button{
                        id:fileSelectorBtn
                        display:AbstractButton.IconOnly
                        icon.name:"audio-x-mpeg.svg"
                        enabled:fileOption.checked?true:false
                        height: 35
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
                    Layout.alignment:Qt.AlignLeft|Qt.AlignVCenter
                    Layout.bottomMargin:10
                    RadioButton{
                        id:directoryOption
                        checked:{
                            if (bellStackBridge.bellSound[0]=="directory"){
                                true
                            }else{
                                false
                            }
                        }
                        text:i18nd("bell-scheduler","Random from directory")
                        onToggled:{
                            if (checked){
                                messageLabel.visible=false
                                if ((folderPath.text=="")||(bellStackBridge.bellSound[2])){
                                    applyBtn.enabled=false
                                }else{
                                    applyBtn.enabled=true
                                }
                            }
                        }
                        ButtonGroup.group:soundOptionsGroup
                        
                    }
                    TextField{
                        id:folderPath 
                        text:{
                            if (bellStackBridge.bellSound[0]=="directory"){
                                if (!bellStackBridge.bellSound[2]){
                                    bellStackBridge.bellSound[1]
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
                        enabled:directoryOption.checked?true:false
                    }

                    Button{
                        id:folderSelectorBtn
                        display:AbstractButton.IconOnly
                        icon.name:"view-media-playlist.svg"
                        enabled:directoryOption.checked?true:false
                        height: 35
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
                    checked:bellStackBridge.bellSound[3]
                    enabled:fileOption.checked?true:false
                    font.pointSize: 10
                    focusPolicy: Qt.NoFocus
                    Layout.alignment:Qt.AlignLeft
                    Layout.bottomMargin:15
                }
                Text{ 
                    id:footText
                    text:i18nd("bell-scheduler","(*) Checking this option the sound file will be copied to the internal folder.It will be this file that is used to reproduce the alarm. In addition, if alarms are exported the file will be included in the export. It is recommended to mark it")
                    font.family: "Quattrocento Sans Bold"
                    font.pointSize: 10
                    Layout.leftMargin:10
                    Layout.topMargin:10
                    Layout.bottomMargin:10
                    Layout.preferredWidth:480
                    wrapMode: Text.WordWrap
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
                enabled:!bellStackBridge.bellSound[2]
                onClicked:{
                    var option=""
                    var tmpPath=""
                    if (fileOption.checked){
                        option="file"
                        if (selectedSoundFile!=""){
                            tmpPath=selectedSoundFile
                        }else{
                            tmpPath=bellStackBridge.bellSound[1]
                        }
                    }else{
                        option="directory"
                        if (selectedSoundFolder!=""){
                            tmpPath=selectedSoundFolder
                        }else{
                            tmpPath=bellStackBridge.bellSound[1]
                        }
                    }
                    bellStackBridge.updateSoundValues([option,tmpPath,soundDefaultPath.checked])
                    restoreInitValues()
                    soundSelector.close()
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
                    soundSelector.close()
                }                
            }

        }
    }


    FileDialog{
        id:soundFileDialog
        title: "Select a sound file"
        currentFolder:{
            if (selectedSoundFile!=""){
                selectedSoundFile.substring(0,selectedSoundFile.lastIndexOf("/"))
            }else{
                StandardPaths.standardLocations(StandardPaths.MusicLocation)[0]
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
            if (selectedSoundFolder!=""){
               selectedSoundFolder
            }else{
               StandardPaths.standardLocations(StandardPaths.MusicLocation)[0]
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
        soundDefaultPath.checked=bellStackBridge.bellSound[3]
        applyBtn.enabled=!bellStackBridge.bellSound[2]
        
        if (bellStackBridge.bellSound[0]=="file"){
            fileOption.checked=true
            folderPath.text=""
            if (!bellStackBridge.bellSound[2]){
                filePath.text=bellStackBridge.bellSound[1].substring(bellStackBridge.bellSound[1].lastIndexOf('/')+1)
            }else{
                filePath.text=""
            }
        }else{
            directoryOption.checked=true
            filePath.text=""
            if (!bellStackBridge.bellSound[2]){
                folderPath.text=bellStackBridge.bellSound[1]
            }else{
                folderPath.text=""
            }
        }

    }
  
  
}
