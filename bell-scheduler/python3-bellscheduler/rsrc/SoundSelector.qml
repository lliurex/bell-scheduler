import org.kde.plasma.core 2.1 as PlasmaCore
import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Popup {

    id:soundPopUp
    property alias xPopUp:soundPopUp.x
    property alias yPopUp:soundPopUp.y
    signal applyButtonClicked
    property string selectedPath

    width:530
    height:390
    x:xPopUp
    y:yPopUp
    /*anchors.centerIn: Overlay.overlay*/
    modal:true
    focus:true
    closePolicy:Popup.NoAutoClose

    Rectangle{
        id:container
        width:soundPopUp.width
        height:soundPopUp.height
        color:"transparent"
        Text{ 
            text:i18nd("bell-scheduler","Sound selection")
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
                visible:true
                text:"Text test"
                type: Kirigami.MessageType.Error
                Layout.preferredWidth:505
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
                    id:standarRow
                    spacing:10
                    Layout.alignment:Qt.AlignLeft
                    Layout.bottomMargin:10
                    RadioButton{
                        id:fileOption
                        checked:{
                            if (bellSchedulerBridge.bellSound[0]=="file"){
                                true
                            }else{
                                false
                            }
                        }
                        text:i18nd("bell-scheduler","Sound file")
                        ButtonGroup.group:soundOptionsGroup
                        
                    }
                    Text{
                        id:soundPath 
                        text:bellSchedulerBridge.bellSound[1].substring(bellSchedulerBridge.bellSound[1].lastIndexOf('/')+1)
                        font.family: "Quattrocento Sans Bold"
                        font.pointSize: 10
                        Layout.maximumWidth:250
                        elide:Text.ElideMiddle
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
                        hoverEnabled:true
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
                            if (bellSchedulerBridge.bellSound[0]=="directory"){
                                true
                            }else{
                                false
                            }
                        }
                        text:i18nd("bell-scheduler","Random from directory")
                        ButtonGroup.group:soundOptionsGroup
                        
                    }
                    Text{
                        id:folderPath 
                        text:bellSchedulerBridge.bellSound[2]
                        font.family: "Quattrocento Sans Bold"
                        font.pointSize: 10
                        Layout.maximumWidth:250
                        elide:Text.ElideMiddle
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
                        hoverEnabled:true
                        onClicked:soundFolderDialog.open()
                    }
                }
                CheckBox {
                    id:bellCopyFilesCb
                    text:i18nd("bell-scheduler","Copy the sound file to the internal folder (*)")
                    checked:true
                    enabled:fileOption.checked?true:false
                    font.pointSize: 10
                    focusPolicy: Qt.NoFocus
                    Keys.onReturnPressed: cdcControlCb.toggled()
                    Keys.onEnterPressed: cdcControlCb.toggled()
                    Layout.alignment:Qt.AlignLeft
                    Layout.bottomMargin:15
                }
                Text{ 
                    id:footText
                    text:i18nd("bell-scheduler","(*) Checking this option the sound file will be copied to the internal folder.\n It will be this file that is used to reproduce the alarm. In addition, if alarms are exported the file will be included in the export. It is recommended to mark it")
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
            anchors.bottomMargin:30
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
                onClicked:soundSelector.close()
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
                onClicked:soundSelector.close()
                
            }

        }
    }


    FileDialog{
        id:soundFileDialog
        title: "Select a sound file"
        folder:shortcuts.home
        onAccepted:{
            selectedPath=soundFileDialog.fileUrl.toString()
            selectedPath=selectedPath.replace(/^(file:\/{2})/,"")
            console.log(selectedPath)
            soundPath.text=selectedPath.substring(selectedPath.lastIndexOf('/')+1)
        }
      
    }
    FileDialog{
        id:soundFolderDialog
        title: "Select a folder"
        folder:shortcuts.home
        selectFolder:true
        onAccepted:{
            selectedPath=soundFileDialog.fileUrl.toString()
            selectedPath=selectedPath.replace(/^(file:\/{2})/,"")
            console.log(selectedPath)
            folderPath.text=selectedPath
        }
      
    }
  
}
