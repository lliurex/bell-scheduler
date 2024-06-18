import QtQuick 2.15
import QtGraphicalEffects 1.0
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.1

Rectangle {
    width: 325
    height: 250
    property alias calendarLocale:calendar.calendarLocale
    property alias startDate:calendar.startDate
    property alias stopDate:calendar.stopDate
    property alias initDate:calendar.initDate
    property alias endDate:calendar.endDate
    property alias rangeDate:calendar.rangeDate
    property alias daysInRange:calendar.daysInRange
    property alias selectedDate:calendar.selectedDate
    signal getSelectedDate (variant value)

    Calendar {
        id: calendar
        width: parent.width
        height: parent.height
        anchors.centerIn:parent
        frameVisible: true
        weekNumbersVisible: false
        focus: true
        property var calendarLocale:calendarLocale
        property var startDate: startDate
        property var stopDate: stopDate
        property var initDate:initDate
        property var endDate:endDate
        property var daysInRange:daysInRange
        property bool rangeDate:rangeDate
        selectedDate:selectedDate
        locale:Qt.locale(calendar.calendarLocale)

       style: CalendarStyle {
            dayDelegate: Item {
                readonly property color sameMonthDateTextColor: "#444"
                readonly property color selectedDateColor: "#3778d0"
                readonly property color selectedDateTextColor: "white"
                readonly property color differentMonthDateTextColor: "#bbb"
                readonly property color invalidDatecolor: "#dddddd"
                property var dateOnFocus: styleData.date
            

                Rectangle {
                    anchors.fill: parent
                    border.color: "transparent"
                    color:{
                        if (calendar.startDate!==undefined || calendar.stopDate!== undefined){
                            "transparent"
                        }else{
                            if (Qt.formatDate(styleData.date,"dd/MM/yyyy")==calendar.initDate || Qt.formatDate(styleData.date,"dd/MM/yyyy")==calendar.endDate){
                            selectedDateColor
                        
                            }else{
                                if (calendar.daysInRange.includes(Qt.formatDate(styleData.date,"dd/MM/yyyy"))){
                                "#55555555"
                            }else{
                                "transparent"
                            }
                        }
                    }
                    
                }

            }

            Rectangle{
                id:fl
                anchors.fill: parent
                property bool flag: false
                color:{
                    if ((dateOnFocus>calendar.startDate) && (dateOnFocus< calendar.stopDate)){
                        "#55555555"
                   }else{
                        if (calendar.startDate !==undefined && dateOnFocus.getTime()===calendar.startDate.getTime() || calendar.stopDate !==undefined && dateOnFocus.getTime()===calendar.stopDate.getTime()){
                           "#3778d0" 
                        }else{
                            "transparent"
                        }
                   }
                }
            }

            MouseArea{
                anchors.fill: parent
                propagateComposedEvents: true
                onPressed: {
                    if(calendar.startDate===undefined){
                        calendar.startDate=styleData.date
                        if (!calendar.rangeDate){
                            calendar.stopDate=styleData.date
                        }else{
                            calendar.stopDate=undefined
                        }
                        getSelectedDate([Qt.formatDate(styleData.date,"dd/MM/yyyy"),"start"])
                    }
                    else if(calendar.stopDate=== undefined){
                        calendar.stopDate=styleData.date
                        getSelectedDate([Qt.formatDate(styleData.date,"dd/MM/yyyy"),"end"])
                    }
                    else{
                        if (calendar.rangeDate){
                            calendar.startDate=styleData.date
                            calendar.stopDate= undefined
                            getSelectedDate([Qt.formatDate(styleData.date,"dd/MM/yyyy"),"start"])
                        }else{
                            calendar.startDate=undefined
                            calendar.stopDate=styleData.date
                            getSelectedDate([Qt.formatDate(styleData.date,"dd/MM/yyyy"),"end"])
                        }
                    }
                    if(calendar.stopDate<=calendar.startDate){
                        if (!calendar.rangeDate){
                            calendar.startDate=styleData.date
                            calendar.stopDate=styleData.date
                        }else{
                            calendar.startDate=styleData.date
                            calendar.stopDate=undefined

                        }
                        getSelectedDate([Qt.formatDate(styleData.date,"dd/MM/yyyy"),"start"])
                    }

                    mouse.accepted = false
                }
            }


            Label {
                id: dayDelegateText
                text: styleData.date.getDate()
                anchors.centerIn: parent
                color: {
                    var color = invalidDatecolor;
                    if (styleData.valid) {
                            // Date is within the valid range.
                            color = styleData.visibleMonth ? sameMonthDateTextColor : differentMonthDateTextColor;
                            if (styleData.selected) {
                                color = "selectedDateTextColor";
                            }
                    }
                    color;
                }
            }
        }
    }

}

}