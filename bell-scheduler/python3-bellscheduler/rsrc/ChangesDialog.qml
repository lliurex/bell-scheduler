import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Popup {
    id: customDialog
    property alias dialogIcon:dialogIcon.source
    property alias dialogVisible:customDialog.visible
    property alias dialogMsg:dialogText.text
    property alias dialogWidth:container.implicitWidth
    property alias btnAcceptVisible:dialogApplyBtn.visible
    property alias btnAcceptText:dialogApplyBtn.text
    property alias btnDiscardText:dialogDiscardBtn.text
    property alias btnDiscardVisible:dialogDiscardBtn.visible
    property alias btnDiscardIcon:dialogDiscardBtn.icon.name
    property alias btnCancelText:dialogCancelBtn.text
    property alias btnCancelIcon:dialogCancelBtn.icon.name
    signal dialogApplyClicked
    signal discardDialogClicked
    signal rejectDialogClicked

    visible:dialogVisible
    modal:true
    anchors.centerIn:Overlay.overlay
    closePolicy:Popup.NoAutoClose

    background:Rectangle{
        color:"#ebeced"
        border.color:"#b8b9ba"
        border.width:1
        radius:5.0
    }


    contentItem: Rectangle {
        id:container
        color: "#ebeced"
        implicitWidth: dialogWidth
        implicitHeight: 120
        anchors.topMargin:5
        anchors.leftMargin:5

        Image{
            id:dialogIcon
            source:dialogIcon

        }
        
        Text {
            id:dialogText
            text:dialogMsg
            font.pointSize: 10
            anchors.left:dialogIcon.right
            anchors.verticalCenter:dialogIcon.verticalCenter
            anchors.leftMargin:10
        
        }
      
        RowLayout {
            anchors.bottom:parent.bottom
            anchors.right:parent.right
            anchors.topMargin:15
            spacing:10

            Button {
                id:dialogApplyBtn
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-ok.svg"
                text: btnAcceptText
                visible:btnAcceptVisible
                font.pointSize: 10
                onClicked:{
                    dialogApplyClicked() 
                }

            }

            Button {
                id:dialogDiscardBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnDiscardIcon
                text: btnDiscardText
                visible:btnDiscardVisible
                font.pointSize: 10
                onClicked:{
                    discardDialogClicked()
                }
            }

            Button {
                id:dialogCancelBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnCancelIcon
                text: btnCancelText
                font.pointSize: 10
                onClicked:{
                    rejectDialogClicked()
                }        
            }
 
        }
    }
 }
