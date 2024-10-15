import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Dialog {
    id: customDialog
    property alias dialogIcon:dialogIcon.source
    property alias dialogTitle:customDialog.title
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
    title:dialogTitle
    modal:true
    anchors.centerIn:Overlay.overlay
    background:Rectangle{
        color:"#ebeced"
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
      
        DialogButtonBox {
            buttonLayout:DialogButtonBox.KdeLayout
            anchors.bottom:parent.bottom
            anchors.right:parent.right
            anchors.topMargin:15

            Button {
                id:dialogApplyBtn
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-ok.svg"
                text: btnAcceptText
                visible:btnAcceptVisible
                font.pointSize: 10
                DialogButtonBox.buttonRole: DialogButtonBox.ApplyRole

            }

            Button {
                id:dialogDiscardBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnDiscardIcon
                text: btnDiscardText
                visible:btnDiscardVisible
                font.pointSize: 10
                DialogButtonBox.buttonRole: DialogButtonBox.DestructiveRole

            }

            Button {
                id:dialogCancelBtn
                display:AbstractButton.TextBesideIcon
                icon.name:btnCancelIcon
                text: btnCancelText
                font.pointSize: 10
                DialogButtonBox.buttonRole:DialogButtonBox.RejectRole
        
            }

            onApplied:{
                dialogApplyClicked()
            }

            onDiscarded:{
                discardDialogClicked()
            }

            onRejected:{
                rejectDialogClicked()
            }
        }
    }
 }
