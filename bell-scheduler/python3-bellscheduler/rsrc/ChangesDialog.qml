import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Popup {
    id: customDialog

    property bool dialogVisible: false
    visible: dialogVisible

    property alias dialogIcon: iconInternal.source 
    property alias dialogMsg: dialogText.text
    property int dialogWidth:400
    
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

    modal:true
    anchors.centerIn:Overlay.overlay
    closePolicy:Popup.NoAutoClose

    background: Rectangle {
        color: "#ebeced"
        border.color: "#b8b9ba"
        border.width: 1
        radius: 5
    }


    contentItem: Rectangle {
        id:container
        color: "#ebeced"
        implicitWidth: customDialog.dialogWidth
        implicitHeight: 140

        RowLayout {
            id: contentRow
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            spacing: 15

            Kirigami.Icon {
                id: iconInternal
                Layout.preferredWidth: Kirigami.Units.iconSizes.huge
                Layout.preferredHeight: Kirigami.Units.iconSizes.huge
            }
            
            Text {
                id: dialogText
                font.pointSize: 10
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
                verticalAlignment: Text.AlignVCenter
                color: "#31363b"
            }
        }
        
        RowLayout {
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.margins: 10
            spacing: 10

            Button {
                id: dialogApplyBtn
                icon.name: "dialog-ok"
                onClicked: dialogApplyClicked() 
            }

            Button {
                id: dialogDiscardBtn
                onClicked: discardDialogClicked()
            }

            Button {
                id: dialogCancelBtn
                onClicked: rejectDialogClicked()
            }
        }
    }
}

