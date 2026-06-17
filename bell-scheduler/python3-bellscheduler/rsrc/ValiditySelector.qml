import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.16 as Kirigami

Popup {

    id:validityPopUp
    signal applyButtonClicked

    width:530
    height:530
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    closePolicy:Popup.NoAutoClose
    onVisibleChanged:{
        if (visible){
            loadInitValues()
        }
    }
    
    background:Rectangle{
	color:"#ebeced"
	border.color:"#b8b9ba"
        border.width:1
        radius:5.0
    }

    contentItem:ColumnLayout{
        id:container
        anchors.fill:parent
        anchors.margins:15
        spacing:12

        Text{ 
            text:i18nd("bell-scheduler","Edit bell validity")
            font.pointSize: 16
            Layout.fillWidth:true
        }

        ColumnLayout{
            id:centerArea
            Layout.fillWidth:true
            Layout.fillHeight:true
            Layout.bottomMargin:10
            spacing:10

            Kirigami.InlineMessage {
                id: messageLabel
                visible:false
                text:""
                type: Kirigami.MessageType.Error
                Layout.fillWidth:true
            }

            Item{
                Layout.alignment:Qt.AlignHCenter
                Layout.fillWidth:true
                Layout.preferredHeight:250

                Calendar{
                    id:calendar
                    width:325
                    height:parent.height
                    anchors.horizontalCenter:parent.horizontalCenter
                    calendarLocale:mainStackBridge.systemLocale
                    startDate:undefined
                    stopDate:undefined
                    initDate:rangeDate.checked?day1Entry.text:dayEntry.text
                    endDate:rangeDate.checked?day2Entry.text:""
                    rangeDate:rangeDate.checked
                    daysInRange:bellStackBridge.bellValidity.daysInRange
   
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
            }
        }
            
        ColumnLayout{
            id: dateOptions
            Layout.fillWidth:true
            spacing:10

            ButtonGroup{
                id:dateOptionsGroup
            }
            
            RowLayout{
                id:singleRow
                spacing:10
                Layout.fillWidth:true

                RadioButton{
                    id:singleDate
                    checked:!bellStackBridge.bellValidity.rangeOption
                    text:i18nd("bell-scheduler","Day:")
                    ButtonGroup.group:dateOptionsGroup
                        
                }

                TextField{
                    id:dayEntry 
                    font.pointSize: 10
                    horizontalAlignment:TextInput.AlignHCenter
                    readOnly:true
                    Layout.preferredWidth:100
                    enabled:singleDate.checked
                }
            }

            RowLayout{
                id:rangeRow
                spacing:10
                Layout.fillWidth:true

                RadioButton{
                    id:rangeDate
                    checked:bellStackBridge.bellValidity.rangeOption
                    text:i18nd("bell-scheduler","From:")
                    ButtonGroup.group:dateOptionsGroup
                        
                }

                TextField{
                    id:day1Entry 
                    font.pointSize: 10
                    horizontalAlignment:TextInput.AlignHCenter
                    readOnly:true
                    Layout.preferredWidth:100
                    enabled:rangeDate.checked
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
                    enabled:rangeDate.checked
                }
    
            }
        }

        Item {
            Layout.fillHeight:true
        }

        RowLayout{
            id:btnBox
            Layout.fillWidth:true
            Layout.alignment:Qt.AlignRight
            spacing:12

            Button {
                id:applyBtn
                visible:true
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-ok"
                text:i18nd("bell-scheduler","Apply")
                enabled:true
                onClicked:{
                    if (validateDates()){
                        var tmpValue=""
                        if (rangeDate.checked){
                            tmpValue=day1Entry.text+"-"+day2Entry.text
                        }else{
                            tmpValue=dayEntry.text
                        }
                        bellStackBridge.updateBellValidity({"value":tmpValue,"rangeOption":rangeDate.checked})
                        validitySelector.close()
                    }
                }
            }
            
            Button {
                id:cancelBtn
                visible:true
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-cancel"
                text:i18nd("bell-scheduler","Cancel")
                enabled:true
                onClicked:{
                    validitySelector.close()
                }
                
            }
        }
    }

    function validateDates(){

        if (rangeDate.checked){
            if (day2Entry.text===""){
                messageLabel.visible=true
                messageLabel.text=i18nd("bell-scheduler","You must indicate the two dates of range")
                return false
            }
            var date1=Date.fromLocaleString(Qt.locale(),day1Entry.text,"dd/MM/yyyy")
            var date2=Date.fromLocaleString(Qt.locale(),day2Entry.text,"dd/MM/yyyy")

            if (date1>=date2){
                messageLabel.visible=true
                messageLabel.text=i18nd("bell-scheduler","Last date in range must be major than init date")
                return false
            }
        }else if (dayEntry.text===""){
            messageLabel.visible=true
            messageLabel.text=i18nd("bell-scheduler","You must indicate a date")
            return false
        }
        
        messageLabel.visible=false;
        messageLabel.text="";
        return true;
    }

    function loadInitValues(){

        calendar.startDate=undefined
        calendar.stopDate=undefined
        calendar.daysInRange=bellStackBridge.bellValidity.daysInRange
        rangeDate.checked=bellStackBridge.bellValidity.rangeOption
        messageLabel.visible=false
        messageLabel.text=""

        var newDate=new Date()
        var days=bellStackBridge.bellValidity.daysInRange

        if (bellStackBridge.bellValidity.rangeOption){
            dayEntry.text=""
            
            if (days.length>0){
                day1Entry.text=days[0]
                day2Entry.text=days[days.length-1]
                newDate=Date.fromLocaleString(Qt.locale(),day1Entry.text,"dd/MM/yyyy")

            }else{
                day1Entry.text=""
                day2Entry.text=""

            }
        }else{
            day1Entry.text=""
            day2Entry.text=""
            dayEntry.text=days[0] || ""

            if (dayEntry.text !==""){
               newDate=Date.fromLocaleString(Qt.locale(),dayEntry.text,"dd/MM/yyyy")
            }
        }

        calendar.initDate=rangeDate.checked?day1Entry.text:dayEntry.text
        calendar.endDate=rangeDate.checked?day2Entry.text:"";
     }

}
