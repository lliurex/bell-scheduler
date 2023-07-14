import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import org.kde.plasma.components 3.0 as PC3



Popup {

    id:sliderPopUp
    property alias popUpWidth:sliderPopUp.width
    property alias popUpHeight:sliderPopUp.height
    property alias xPopUp:sliderPopUp.x
    property alias yPopUp:sliderPopUp.y
    property alias headText:headText.text
    property alias footText:footText.text
    property alias showFoot:footText.visible
    property alias sliderValue:sliderId.value
    signal applyButtonClicked

    width:popUpWidth
    height:popUpHeight
    x:sliderPopUp.x
    y:sliderPopUp.y
    /*anchors.centerIn: Overlay.overlay*/
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
            font.family: "Quattrocento Sans Bold"
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

        }

        PC3.Label {
            text:sliderId.value
            font.pointSize: 14
            anchors.top:sliderId.bottom
            anchors.topMargin:10
            anchors.horizontalCenter:parent.horizontalCenter
        }

        Text{ 
            id:footText
            text:footText
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 10
            visible:showFoot
            anchors.bottom:cancelBtn.top
            anchors.left:container.left
            anchors.leftMargin:10
            anchors.topMargin:10
            anchors.bottomMargin:10
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
            anchors.right:applyBtn.left
            anchors.rightMargin:10
            anchors.bottomMargin:25

            onClicked:{
                sliderPopUp.close()
            }
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
            anchors.right:container.right
            anchors.rightMargin:20
            anchors.bottomMargin:25
       
            onClicked:{
                applyButtonClicked()
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
            if (k >= Qt.Key_0 && k <= Qt.Key_9) {
                duration=duration+(k - Qt.Key_0)
                timerSlider.restart()
            }
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
        var newValue=parseInt(container.duration)
        if (newValue>=0 && newValue<=600){
            sliderId.value = newValue
        }
        container.duration=""
        
    }
}
