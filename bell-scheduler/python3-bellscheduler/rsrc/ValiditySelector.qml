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
                visible:false
                text:""
                type: Kirigami.MessageType.Error
                Layout.preferredWidth:505
                Layout.topMargin: 40
            }

            Calendar{
                id:calendar
                Layout.alignment:Qt.AlignHCenter
                Layout.preferredWidth:325
                Layout.topMargin: messageLabel.visible?0:50
                startDate:undefined
                stopDate:undefined
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
                daysInRange:bellSchedulerBridge.bellValidityDaysInRange
                Connections{
                    target:calendar
                    function onGetSelectedDate(info){
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
                        checked:!bellSchedulerBridge.bellValidityRangeOption
                        text:i18nd("bell-scheduler","Day:")
                        ButtonGroup.group:dateOptionsGroup
                            
                    }
                    TextField{
                        id:dayText 
                        text:{
                            if (!bellSchedulerBridge.bellValidityRangeOption){
                                 bellSchedulerBridge.bellValidityDaysInRange[0]
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
                        checked:bellSchedulerBridge.bellValidityRangeOption
                        text:i18nd("bell-scheduler","From:")
                        ButtonGroup.group:dateOptionsGroup
                            
                    }
                    TextField{
                        id:day1Entry 
                        text:{
                            if (bellSchedulerBridge.bellValidityRangeOption){
                                if (bellSchedulerBridge.bellValidityDaysInRange.length>0){
                                    bellSchedulerBridge.bellValidityDaysInRange[0]
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
                           if (bellSchedulerBridge.bellValidityRangeOption){
                                if (bellSchedulerBridge.bellValidityDaysInRange.length>0){
                                    bellSchedulerBridge.bellValidityDaysInRange[ bellSchedulerBridge.bellValidityDaysInRange.length-1]
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
                onClicked:{
                    if (validateDates()){
                        var tmpValue=""
                        if (rangeDate.checked){
                            tmpValue=day1Entry.text+"-"+day2Entry.text
                        }else{
                            tmpValue=dayText.text
                        }
                        bellSchedulerBridge.updateBellValidityValue([tmpValue,rangeDate.checked])
                        restoreInitValues()
                        validitySelector.close()
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
                    restoreInitValues()
                    validitySelector.close()
                }
                
            }

        }
    }
    function validateDates(){

        if (rangeDate.checked){
            if (day2Entry.text==""){
                messageLabel.visible=true
                messageLabel.text=i18nd("bell-scheduler","You must indicate the two dates of range")
                return false
            }else{
                if (day1Entry.text>=day2Entry.text){
                    messageLabel.visible=true
                    messageLabel.text=i18nd("bell-scheduler","Last date in range must be major than init date")
                    return false
                }else{
                    messageLabel.visible=false
                    messageLabel.text=""
                    return true
                }
            }
        }else{
            return true
        }
    }

    function restoreInitValues(){

        if (bellSchedulerBridge.bellValidityRangeOption){
            dayText.text=""
            if (bellSchedulerBridge.bellValidityDaysInRange.length>0){
                day1Entry.text=bellSchedulerBridge.bellValidityDaysInRange[0]
                day2Entry.text=bellSchedulerBridge.bellValidityDaysInRange[ bellSchedulerBridge.bellValidityDaysInRange.length-1]
            }else{
                day1Entry.text=""
                day2Entry.text=""
            }
            /*calendar.initDate=day1Entry.text
            calendar.endDate=day2Entry.text*/
        }else{
            day1Entry.text=""
            day2Entry.text=""
            dayText.text=bellSchedulerBridge.bellValidityDaysInRange[0]
            calendar.initDate=dayText.text
            calendar.endDate=""
        }
        calendar.startDate=undefined
        calendar.stopDate=undefined
        calendar.daysInRange=bellSchedulerBridge.bellValidityDaysInRange
        rangeDate.checked=bellSchedulerBridge.bellValidityRangeOption

    }

}
