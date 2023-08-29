import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.plasma.components 3.0 as PC3



Popup {

    id:sliderPopUp
    property alias popUpWidth:sliderPopUp.width
    property alias popUpHeight:sliderPopUp.height
    property alias headText:headText.text
    property alias footText:footText.text
    property alias showFoot:footText.visible
    property alias sliderValue:sliderId.value
    signal applyButtonClicked
    signal cancelButtonClicked

    width:popUpWidth
    height:popUpHeight
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    closePolicy:Popup.NoAutoClose

    Rectangle{
        id:container
        width:popUpWidth
        height:popUpHeight
        property string duration
        color:"transparent"

        Text{ 
            id:headText
            text:headText
            font.pointSize: 16
            anchors.topMargin:10
            anchors.leftMargin:10
        }

        PC3.Slider{
        
            id:sliderId
            from:0
            to:600
            value:sliderValue
            stepSize:5
            anchors.horizontalCenter:parent.horizontalCenter
            anchors.top:headText.bottom
            anchors.topMargin:25
            focus:true
            onValueChanged:{
                sliderEntry.text=sliderId.value
            }

        }
        TextField{
            id: sliderEntry
            validator: RegExpValidator { regExp: /([0-9][0-9][0-9])/ }
            implicitWidth: 70
            text:sliderId.value
            horizontalAlignment: TextInput.AlignHCenter
            anchors.top:sliderId.bottom
            anchors.topMargin:10
            anchors.bottomMargin:20
            anchors.horizontalCenter:parent.horizontalCenter
            font.pointSize: 14
            onTextChanged:{
                timerSlider.restart()
            }
        }

        Text{ 
            id:footText
            text:footText
            font.pointSize: 10
            visible:showFoot
            anchors.bottom:cancelBtn.top
            anchors.left:container.left
            anchors.leftMargin:10
            anchors.bottomMargin:10
            width:320
            wrapMode: Text.WordWrap
        }

        Button {
            id:applyBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("bell-scheduler","Apply")
            height:40
            enabled:true
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            anchors.bottom:container.bottom
            anchors.right:cancelBtn.left
            anchors.rightMargin:10
            anchors.bottomMargin:25
            onClicked:{
                applyButtonClicked()
                if (sliderEntry.text==""){
                    sliderEntry.text=sliderId.value
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
            height:40
            enabled:true
            Keys.onReturnPressed: cancelBtn.clicked()
            Keys.onEnterPressed: cancelBtn.clicked()
            anchors.bottom:container.bottom
            anchors.right:container.right
            anchors.rightMargin:25
            anchors.bottomMargin:25
            onClicked:{
                cancelButtonClicked()
            }
        }

        Keys.onPressed: {
            const k = event.key;

            if (k === Qt.Key_Plus) {
                sliderId.value=sliderId.value+1
            }
            if (k === Qt.Key_Minus){
                sliderId.value=sliderId.value-1
            }
            /*
            if (k >= Qt.Key_0 && k <= Qt.Key_9) {
                duration=duration+(k - Qt.Key_0)
                timerSlider.restart()
            }*/
            event.accepted = true;
        }
    
        Timer{
            id:timerSlider
            interval: 400
            onTriggered:{
                setNewValue()
            }
        }
    }    
    function setNewValue(){
        if (sliderEntry.text!=""){
            var newValue=parseInt(sliderEntry.text)
            if (newValue>=0 && newValue<=600){
                sliderId.value = newValue
            }else{
                if (newValue>600){
                    sliderId.value=600
                }
            }
        }else{
            sliderId.value=0
        }
        
    }
}
