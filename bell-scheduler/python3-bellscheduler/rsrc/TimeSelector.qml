import org.kde.plasma.core 2.1 as PlasmaCore
import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Popup {
    id:timePopUp
    property alias hourEntry:hourEntry.text
    property alias minuteEntry:minuteEntry.text
    signal timeApplyClicked (hour:string,minute:string)

    width:320
    height:200
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    closePolicy:Popup.NoAutoClose

    Rectangle{
        id:container
        width:timePopUp.width
        height:timePopUp.height
        color:"transparent"
        Text{ 
            text:i18nd("bell-scheduler","Edit time for bell")
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 16
        }
        GridLayout{
            id:imageSelectorLayout
            rows:1
            flow: GridLayout.TopToBottom
            rowSpacing:10
            anchors.horizontalCenter:parent.horizontalCenter
            enabled:true

            RowLayout {
                id: popupTimerLayout
                Layout.topMargin:40
                spacing:4
                TextField{
                    id: hourEntry
                    validator: RegExpValidator { regExp: /([0-1][0-9]|2[0-3])/ }
                    implicitWidth: 70
                    horizontalAlignment: TextInput.AlignHCenter
                    color:"#3daee9"
                    font.pointSize: 35
                }

                Text{
                    font.pointSize:35
                    color:"#3daee9"
                    text:":"
                }
                        
                TextField{
                    id: minuteEntry
                    validator: RegExpValidator { regExp: /[0-5][0-9]/ }
                    implicitWidth: 70
                    horizontalAlignment: TextInput.AlignHCenter
                    color:"#3daee9"
                    font.pointSize: 35
                }
            }
        }
        RowLayout{
            id:btnBox
            anchors.bottom:parent.bottom
            anchors.right:parent.right
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
                enabled:!bellSchedulerBridge.bellImage[3]
                Keys.onReturnPressed: applyBtn.clicked()
                Keys.onEnterPressed: applyBtn.clicked()
                onClicked:{
                    if (validateEntry(hourEntry.text,minuteEntry.text)){
                        timeApplyClicked(hourEntry.text,minuteEntry.text)
                        delay(1000, function() {
                            timePopUp.close();
                        })
                    }else{
                        timePopUp.close();
                    }
                    
                }
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
                onClicked:{
                    timePopUp.close()
                }
            }

        }
    }


    function validateEntry(hour,minute){

        if ((hour =="") || (minute=="")){
            return false;
        }else{
            return true;
        }

    }

    Timer {
        id: timer
    }

    function delay(delayTime, cb) {
        timer.interval = delayTime;
        timer.repeat = false;
        timer.triggered.connect(cb);
        timer.start();
    }
  
}
