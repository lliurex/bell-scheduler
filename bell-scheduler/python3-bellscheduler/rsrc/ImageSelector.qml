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
    signal applyButtonClicked

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
                text:"Text test"
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

                RowLayout{
                    id:standarRow
                    spacing:10
                    Layout.alignment:Qt.AlignLeft
                    Layout.bottomMargin:10
                    RadioButton{
                        id:standardOption
                        text:i18nd("bell-scheduler","From stock")
                        
                    }
                    ImageList{
                        id:imageList
                    }
                }

                RowLayout{
                    id:customRow
                    spacing:10
                    Layout.alignment:Qt.AlignLeft|Qt.AlignVCenter
                    Layout.bottomMargin:10
                    RadioButton{
                        id:customOption
                        text:i18nd("bell-scheduler","Custom image")
                        
                    }
                    Text{
                        id:customImagePath 
                        text:i18nd("bell-scheduler","No file selected")
                        font.family: "Quattrocento Sans Bold"
                        font.pointSize: 10
                        Layout.maximumWidth:250
                        elide:Text.ElideMiddle
                    }

                    Button{
                        id:fileSelectorBtn
                        display:AbstractButton.IconOnly
                        icon.name:"insert-image.svg"
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
                onClicked:imageSelector.close()
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
                onClicked:imageSelector.close()
                
            }

        }
    }


    FileDialog{
        id:imgDialog
        title: "Select and image file"
        folder:shortcuts.home
        onAccepted:{
            var tmpFile=imgDialog.fileUrl.toString()
            tmpFile=tmpFile.replace(/^(file:\/{2})/,"")
            customImagePath.text=tmpFile
        }
      
    }
  
}
