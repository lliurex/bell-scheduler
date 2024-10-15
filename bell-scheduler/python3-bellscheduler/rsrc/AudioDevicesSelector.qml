import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {

    id:audioSelectorPopUp
    signal applyButtonClicked

    width:530
    height:200
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    closePolicy:Popup.NoAutoClose

    onVisibleChanged:{
        if (visible){
            loadInitVales()
        }
    }

     
    background:Rectangle{
        color:"#ebeced"
    }

    contentItem:Rectangle{
        id:container
        width:audioSelectorPopUp.width
        height:audioSelectorPopUp.height
        color:"transparent"
        Text{
            id:headText 
            text:i18nd("bell-scheduler","Set audio output")
            font.pointSize: 16
            anchors.topMargin:10
            anchors.leftMargin:10
        }
        GridLayout{
            id:audioSelectorLayout
            rows:2
            flow: GridLayout.TopToBottom
            rowSpacing:15
            anchors.top:headText.bottom
            anchors.left:parent.left
            anchors.topMargin:25
            anchors.bottomMargin:20
            anchors.horizontalCenter:parent.horizontalCenter
            enabled:true
           
              
            GridLayout{
                id: audioOptions
                rows:2
                flow: GridLayout.TopToBottom
                rowSpacing:5
                Layout.fillWidth:true

                CheckBox {
                    id:enableConfiguration
                    text:i18nd("bell-scheduler","Set the default audio ouput to play the alarm")
                    checked:bellsOptionsStackBridge.isAudioDeviceConfigurated
                    font.pointSize: 10
                    focusPolicy: Qt.NoFocus
                    Layout.bottomMargin:10
                    Layout.alignment:Qt.AlignLeft
                }
                ComboBox{
                    id:audioDevicesValues
                    textRole:"name"
                    valueRole:"value"
                    currentIndex:bellsOptionsStackBridge.currentAudioDevice
                    model:bellsOptionsStackBridge.audioDevicesModel
                    Layout.alignment:Qt.AlignHCenter
                    Layout.preferredWidth:500
                    enabled:enableConfiguration.checked?true:false
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
                enabled:true
                onClicked:{
                    bellsOptionsStackBridge.manageAudioDeviceControl([enableConfiguration.checked,audioDevicesValues.currentIndex])
                    audioSelectorPopUp.close()
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
                    audioSelectorPopUp.close()
                }
                
            }

        }
    }
 
    function loadInitVales(){

        enableConfiguration.checked=bellsOptionsStackBridge.isAudioDeviceConfigurated
        audioDevicesValues.currentIndex=bellsOptionsStackBridge.currentAudioDevice
     }


}
