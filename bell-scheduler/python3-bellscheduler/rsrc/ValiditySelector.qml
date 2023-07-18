import org.kde.plasma.core 2.1 as PlasmaCore
import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Popup {

    id:validityPopUp
    property alias xPopUp:validityPopUp.x
    property alias yPopUp:validityPopUp.y
    signal applyButtonClicked

    width:530
    height:510
    x:xPopUp
    y:yPopUp
    /*anchors.centerIn: Overlay.overlay*/
    modal:true
    focus:true
    closePolicy:Popup.NoAutoClose

    Rectangle{
        id:container
        width:validityPopUp.width
        height:validityPopUp.height
        color:"transparent"
        Text{ 
            text:i18nd("bell-scheduler","Validity selection")
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 16
        }
        GridLayout{
            id:validitySelectorLayout
            rows:3
            flow: GridLayout.TopToBottom
            rowSpacing:15
            anchors.left:parent.left
            anchors.bottomMargin:20
            anchors.horizontalCenter:parent.horizontalCenter
            enabled:true
           
            Kirigami.InlineMessage {
                id: messageLabel
                visible:true
                text:"Text test"
                type: Kirigami.MessageType.Error
                Layout.preferredWidth:505
                Layout.topMargin: 40
            }

            Calendar{
                id:calendar
                Layout.alignment:Qt.AlignHCenter
                Layout.preferredWidth:325
                Layout.topMargin: messageLabel.visible?0:50
                initDate:{
                    if (rangeDate.checked){
                        day1Entry.text
                    }else{
                        dayText.text
                    }
                }
                endDate:{
                    if (rangeDate.checked){
                        day2Entry.text
                    }else{
                        ""
                    }
                }
                rangeDate:rangeDate.checked
                daysInRange:bellSchedulerBridge.daysInRange
                Connections{
                    target:calendar
                    function onGetSelectedDate(info){
                        console.log(info)
                        if (rangeDate.checked){
                            if (info[1]=="start"){
                                day1Entry.text=info[0]
                                day2Entry.text=""
                            }else{
                                day2Entry.text=info[0]
                            }
                        }else{
                            dayText.text=info[0]
                        }
                    }
                }
            }
            
            GridLayout{
                id: dateOptions
                rows:2
                flow: GridLayout.TopToBottom
                rowSpacing:5
                Layout.fillWidth:true
                ButtonGroup{
                    id:dateOptionsGroup
                }
                
                RowLayout{
                    id:singleRow
                    spacing:10
                    Layout.alignment:Qt.AlignLeft
                    Layout.bottomMargin:10
                    RadioButton{
                        id:singleDate
                        checked:!bellSchedulerBridge.validityRangeDate
                        text:i18nd("bell-scheduler","Day:")
                        ButtonGroup.group:dateOptionsGroup
                            
                    }
                    TextField{
                        id:dayText 
                        text:{
                            if (!bellSchedulerBridge.validityRangeDate){
                                bellSchedulerBridge.daysInRange[0]
                            }else{
                                ""
                            }
                        }
                        font.family: "Quattrocento Sans Bold"
                        font.pointSize: 10
                        horizontalAlignment:TextInput.AlignHCenter
                        readOnly:true
                        Layout.preferredWidth:100
                        enabled:singleDate.checked?true:false
                        
                    }
        
                }
                RowLayout{
                    id:rangeRow
                    spacing:10
                    Layout.alignment:Qt.AlignLeft
                    Layout.bottomMargin:10
                    RadioButton{
                        id:rangeDate
                        checked:bellSchedulerBridge.validityRangeDate
                        text:i18nd("bell-scheduler","From:")
                        ButtonGroup.group:dateOptionsGroup
                            
                    }
                    TextField{
                        id:day1Entry 
                        text:{
                            if (bellSchedulerBridge.validityRangeDate){
                                if (bellSchedulerBridge.daysInRange.length>0){
                                    bellSchedulerBridge.daysInRange[0]
                                }else{
                                    ""
                                }
                            }
                        }
                        font.family: "Quattrocento Sans Bold"
                        font.pointSize: 10
                        horizontalAlignment:TextInput.AlignHCenter
                        readOnly:true
                        Layout.preferredWidth:100
                        enabled:rangeDate.checked?true:false
                        
                    }
                    Text{
                        id:day2Text
                        text:i18nd("bell-scheduler","to:")
                    }
                    TextField{
                        id:day2Entry 
                        text:{
                           if (bellSchedulerBridge.validityRangeDate){
                                if (bellSchedulerBridge.daysInRange.length>0){
                                    bellSchedulerBridge.daysInRange[bellSchedulerBridge.daysInRange.length-1]
                                }else{
                                    ""
                                }
                            }
                        }
                        font.family: "Quattrocento Sans Bold"
                        font.pointSize: 10
                        horizontalAlignment:TextInput.AlignHCenter
                        readOnly:true
                        Layout.preferredWidth:100
                        enabled:rangeDate.checked?true:false
                    
                    }
        
                }
            }

        }
        RowLayout{
            id:btnBox
            anchors.bottom:parent.bottom
            anchors.right:parent.right
            anchors.topMargin:10
            anchors.bottomMargin:30
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
                enabled:true
                Keys.onReturnPressed: applyBtn.clicked()
                Keys.onEnterPressed: applyBtn.clicked()
                onClicked:validitySelector.close()
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
                onClicked:validitySelector.close()
                
            }

        }
    }

}
