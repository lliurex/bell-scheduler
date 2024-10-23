import org.kde.kirigami as Kirigami
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

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

    background:Rectangle{
	color:"#ebeced"
	border.color:"#b8b9ba"
        border.width:1
        radius:5.0
    }


    contentItem:Rectangle{
        id:container
        width:timePopUp.width
        height:timePopUp.height
        color:"transparent"
        Text{ 
            text:i18nd("bell-scheduler","Edit time for bell")
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
                    validator: RegularExpressionValidator { regularExpression: /([0-1][0-9]|2[0-3])/ }
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
                    validator: RegularExpressionValidator { regularExpression: /[0-5][0-9]/ }
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
            spacing:10

            Button {
                id:applyBtn
                visible:true
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-ok.svg"
                text:i18nd("bell-scheduler","Apply")
                Layout.preferredHeight:40
                enabled:!bellStackBridge.bellImage[3]
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
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-cancel.svg"
                text:i18nd("bell-scheduler","Cancel")
                Layout.preferredHeight: 40
                enabled:true
                onClicked:{
                    restoreInitValues()
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

    function restoreInitValues(){

        hourEntry.text=formatEditText(bellStackBridge.bellCron[0])
        minuteEntry.text=formatEditText(bellStackBridge.bellCron[1])

    }

    function formatEditText(value){
        if (value<10){
            return "0"+value.toString();
        }else{
            return value.toString();
        }

    }
  
}
