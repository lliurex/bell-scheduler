import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3
import org.kde.kirigami 2.16 as Kirigami

Dialog {
    id: customDialog

    property bool dialogVisible: false
    property string dialogIcon: ""
    property string dialogTitle:""
    property string dialogMsg: ""
    property real dialogWidth: 400
    property bool btnAcceptVisible: true
    property string btnAcceptText: ""
    property string btnDiscardText: ""
    property bool btnDiscardVisible: true
    property string btnDiscardIcon: ""
    property string btnCancelText: ""
    property string btnCancelIcon: ""

    signal dialogApplyClicked()
    signal discardDialogClicked()
    signal rejectDialogClicked()

    title: customDialog.dialogTitle
    modality: Qt.WindowModal
    visible:customDialog.dialogVisible

    contentItem: Rectangle {
        id: container
        color: "#ebeced"
        implicitWidth: customDialog.dialogWidth
        implicitHeight: 140

        RowLayout {
            id: contentLayout
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: 0
            spacing: 15

            Kirigami.Icon {
                id: dialogIcon
                source: customDialog.dialogIcon
                Layout.preferredWidth: 64
                Layout.preferredHeight: 64
                visible: status === Image.Ready
            }

            Text {
                id: dialogText
                text: customDialog.dialogMsg
                font.pointSize: 10
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
            }
        }

        DialogButtonBox {
            id: buttonBox
            buttonLayout: DialogButtonBox.KdeLayout
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.margins: 10

            Button {
                id: dialogApplyBtn
                display: AbstractButton.TextBesideIcon
                icon.name: "dialog-ok"
                text: customDialog.btnAcceptText
                visible: customDialog.btnAcceptVisible
                font.pointSize: 10
                DialogButtonBox.buttonRole: DialogButtonBox.ApplyRole
                onClicked: customDialog.dialogApplyClicked()
            }

            Button {
                id: dialogDiscardBtn
                display: AbstractButton.TextBesideIcon
                icon.name: customDialog.btnDiscardIcon
                text: customDialog.btnDiscardText
                visible: customDialog.btnDiscardVisible
                font.pointSize: 10
                DialogButtonBox.buttonRole: DialogButtonBox.DestructiveRole
                onClicked: customDialog.discardDialogClicked()
            }

            Button {
                id: dialogCancelBtn
                display: AbstractButton.TextBesideIcon
                icon.name: customDialog.btnCancelIcon
                text: customDialog.btnCancelText
                font.pointSize: 10
                DialogButtonBox.buttonRole: DialogButtonBox.RejectRole
                onClicked: {
                    customDialog.rejectDialogClicked()
                    customDialog.reject()
                }
            }
        }
    }
}
