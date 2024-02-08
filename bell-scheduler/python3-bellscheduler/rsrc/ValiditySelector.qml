import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Popup {

    id:validityPopUp
    signal applyButtonClicked

    width:530
    height:510
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
        width:validityPopUp.width
        height:validityPopUp.height
        color:"transparent"
        Text{ 
            text:i18nd("bell-scheduler","Edit bell validity")
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
                calendarLocale:mainStackBridge.systemLocale
                startDate:undefined
                stopDate:undefined
                initDate:{
                    if (rangeDate.checked){
                        day1Entry.text
                    }else{
                        dayEntry.text
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
                daysInRange:bellStackBridge.bellValidityDaysInRange
                selectedDate:new Date()
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
                            dayEntry.text=""
                        }else{
                            dayEntry.text=info[0]
                            day1Entry.text=""
                            day2Entry.text=""
                            calendar.startDate=undefined
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
                        checked:!bellStackBridge.bellValidityRangeOption
                        text:i18nd("bell-scheduler","Day:")
                        ButtonGroup.group:dateOptionsGroup
                            
                    }
                    TextField{
                        id:dayEntry 
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
                        checked:bellStackBridge.bellValidityRangeOption
                        text:i18nd("bell-scheduler","From:")
                        ButtonGroup.group:dateOptionsGroup
                            
                    }
                    TextField{
                        id:day1Entry 
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
                    if (validateDates()){
                        var tmpValue=""
                        if (rangeDate.checked){
                            tmpValue=day1Entry.text+"-"+day2Entry.text
                        }else{
                            tmpValue=dayEntry.text
                        }
                        bellStackBridge.updateBellValidityValue([tmpValue,rangeDate.checked])
                        validitySelector.close()
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
                if (Date.fromLocaleString(Qt.locale(),day1Entry.text,"dd/MM/yyyy")>=Date.fromLocaleString(Qt.locale(),day2Entry.text,"dd/MM/yyyyy")){
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

    function loadInitVales(){

        calendar.startDate=undefined
        calendar.stopDate=undefined
        calendar.daysInRange=bellStackBridge.bellValidityDaysInRange
        rangeDate.checked=bellStackBridge.bellValidityRangeOption

        if (bellStackBridge.bellValidityRangeOption){
            dayEntry.text=""
            if (bellStackBridge.bellValidityDaysInRange.length>0){
                day1Entry.text=bellStackBridge.bellValidityDaysInRange[0]
                day2Entry.text=bellStackBridge.bellValidityDaysInRange[ bellStackBridge.bellValidityDaysInRange.length-1]
                calendar.selectedDate=Date.fromLocaleString(Qt.locale(),day1Entry.text,"dd/MM/yyyy")

            }else{
                day1Entry.text=""
                day2Entry.text=""
                calendar.selectedDate=new Date()

            }
            calendar.initDate=day1Entry.text
            calendar.endDate=day2Entry.text
        }else{
            day1Entry.text=""
            day2Entry.text=""
            dayEntry.text=bellStackBridge.bellValidityDaysInRange[0]
            calendar.initDate=dayEntry.text
            calendar.endDate=""
            if (dayEntry!=""){
                calendar.selectedDate=Date.fromLocaleString(Qt.locale(),dayEntry.text,"dd/MM/yyyy")
            }else{
                calendar.selectedDate=new Date()
            }
        }
    
    }

}
