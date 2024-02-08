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

    background:Rectangle{
        color:"#ebeced"
    }

    contentItem:Rectangle{
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
            ToolTip.delay: 1000
            ToolTip.timeout: 3000
            ToolTip.visible: hovered
            ToolTip.text:i18nd("bell-scheduler","Drag to change the the value")
            onValueChanged:{
                sliderEntry.text=sliderId.value
            }

        }
        Row{
            anchors.top:sliderId.bottom
            anchors.topMargin:10
            anchors.bottomMargin:20
            anchors.horizontalCenter:parent.horizontalCenter
            spacing:15
            Rectangle{
                id:removeContainer
                width:20
                height:20
                border.color: "transparent"
                border.width:1
                color:"transparent"
                anchors.verticalCenter:parent.verticalCenter

                Text{ 
                    id:removeText
                    text:"-"
                    font.pointSize: 20
                    verticalAlignment: Text.AlignVCenter
                    anchors.centerIn:removeContainer
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible:mouseAreaRemove.containsMouse?true:false 
                    ToolTip.text:i18nd("bell-scheduler","Click to decrease value")
                    MouseArea {
                        id: mouseAreaRemove
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: {
                            focus=true
                            removeContainer.border.color="#add8e6"
                        }
                        onExited: {
                            sliderId.focus=true
                            removeContainer.border.color="transparent"
                        }
                        onClicked:{
                              sliderId.value=sliderId.value-1
                        }

                     }
                                   
                }
            }
            TextField{
                id: sliderEntry
                validator: RegExpValidator { regExp: /([0-9][0-9][0-9])/ }
                implicitWidth: 70
                text:sliderId.value
                horizontalAlignment: TextInput.AlignHCenter
                font.pointSize: 14
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible: hovered
                ToolTip.text:i18nd("bell-scheduler","Enter the value you want")
                onTextChanged:{
                    timerSlider.restart()
                }
            }
            Rectangle{
                id:addContainer
                width:20
                height:20
                border.color: "transparent"
                border.width:1
                color:"transparent"
                anchors.verticalCenter:parent.verticalCenter
                Text{ 
                    id:addText
                    text:"+"
                    font.pointSize: 22
                    verticalAlignment: Text.AlignVCenter
                    anchors.centerIn:addContainer
                    ToolTip.delay: 1000
                    ToolTip.timeout: 3000
                    ToolTip.visible:mouseAreaAdd.containsMouse?true:false 
                    ToolTip.text:i18nd("bell-scheduler","Click to increase value")
                    MouseArea {
                        id: mouseAreaAdd
                        anchors.fill: parent
                        hoverEnabled: true
                        onEntered: {
                            focus=true
                            addContainer.border.color="#add8e6"
                        }
                        onExited: {
                            sliderId.focus=true
                            addContainer.border.color="transparent"
                        }
                        onClicked:{
                              sliderId.value=sliderId.value+1
                        }
                    }
                          
                }
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
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-ok.svg"
            text:i18nd("bell-scheduler","Apply")
            height:40
            enabled:true
            anchors.bottom:container.bottom
            anchors.right:cancelBtn.left
            anchors.rightMargin:10
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
            display:AbstractButton.TextBesideIcon
            icon.name:"dialog-cancel.svg"
            text:i18nd("bell-scheduler","Cancel")
            height:40
            enabled:true
            anchors.bottom:container.bottom
            anchors.right:container.right
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
