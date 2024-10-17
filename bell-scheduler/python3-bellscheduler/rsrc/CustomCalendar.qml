import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    property alias startDate:calendar.startDate
    property alias stopDate:calendar.stopDate
    property alias initDate:calendar.initDate
    property alias endDate:calendar.endDate
    property alias rangeDate:calendar.rangeDate
    property alias daysInRange:calendar.daysInRange
    property var currentLocale:Qt.locale(mainStackBridge.systemLocale)
    property alias selectedDate:calendar.selectedDate
    property var currentMonth:calendar.selectedDate.getMonth()
    property var fullMonth:calendar.selectedDate.toLocaleString(currentLocale,'MMMM')
    property var currentYear:calendar.selectedDate.getFullYear()
    signal getSelectedDate (variant value)

    RowLayout{
        Rectangle{
            id:removeContainer
            width:50
            height:50
            border.color: "transparent"
            border.width:1
            color:"transparent"

            Text{
                id:removeText
                text:"<"
                color:"#d3d3d3"
                font.pointSize: 30
                verticalAlignment: Text.AlignVCenter
                anchors.centerIn:removeContainer
                ToolTip.delay: 1000
                ToolTip.timeout: 3000
                ToolTip.visible:mouseAreaRemove.containsMouse?true:false
                MouseArea {
                    id: mouseAreaRemove
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        removeContainer.color="#c4c4c4"
                        removeText.color="white"
                    }
                    onExited: {
                        removeContainer.color="transparent"
                        removeText.color="#d3d3d3"
                    }
                    onClicked:{
                        if (currentMonth>0 && currentMonth<12){
                            currentMonth=currentMonth-1
                            fullMonth=currentLocale.monthName(currentMonth)
                        }else{
                            currentMonth=11
                            currentYear=currentYear-1
                            fullMonth=currentLocale.monthName(currentMonth)
                        }
                    }

                }

            }
        }
        Text{
            text:fullMonth+" "+currentYear
            font.pointSize:20
            Layout.fillWidth:true
            horizontalAlignment: Text.AlignHCenter
        }
        Rectangle{
            id:addContainer
            width:50
            height:50
            border.color: "transparent"
            border.width:1
            color:"transparent"

            Text{
                id:addText
                text:">"
                font.pointSize: 30
                color:"#d3d3d3"
                verticalAlignment: Text.AlignVCenter
                anchors.centerIn:addContainer
                MouseArea {
                    id: mouseAreaAdd
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: {
                        addContainer.color="#d6d4d4"
                        addText.color="white"
                    }
                    onExited: {
                        addContainer.color="transparent"
                        addText.color="#d3d3d3"
                    }
                    onClicked:{
                        if (currentMonth<11){
                            currentMonth=currentMonth+1
                            fullMonth=currentLocale.monthName(currentMonth)
                        }else{
                            currentMonth=0
                            currentYear=currentYear+1
                            fullMonth=currentLocale.monthName(currentMonth)
                        }
                    }
                }

            }
        }
    }
    DayOfWeekRow {
        locale: currentLocale
        Layout.fillWidth: true
    }

    MonthGrid {
        id:calendar
        Layout.fillWidth: true
        Layout.fillHeight:true

        month: currentMonth
        year: currentYear
        property var startDate: startDate
        property var stopDate: stopDate
        property var initDate:initDate
        property var endDate:endDate
        property var daysInRange:daysInRange
        property bool rangeDate:rangeDate
	property var selectedDate:selectedDate
        locale: currentLocale


        delegate: Text {
            property MonthGrid control: calendar
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            opacity: model.month === control.month ? 0.5 : 0.5
            text: day
            font.pointSize: 10
            Rectangle {
                anchors.fill: parent
                anchors.margins: -4
                color: {
     			if (calendar.startDate===undefined && calendar.stopDate=== undefined){
				if ((model.date.toLocaleString(locale,"dd/MM/yyyy")===calendar.initDate)||(model.date.toLocaleString(locale,"dd/MM/yyyy")===calendar.endDate)){
					"#3778d0"
				}else{
					if (calendar.daysInRange.includes(model.date.toLocaleString(locale,"dd/MM/yyyy"))){
						"#55555555"
					}else{
						"white"
					}
				}
			}else{
				if ((model.date.getTime()>calendar.startDate) && (model.date.getTime()< calendar.stopDate)){
					"#55555555"
				}else{
					if (calendar.startDate !==undefined && model.date.getTime()===calendar.startDate || calendar.stopDate !==undefined && model.date.getTime()===calendar.stopDate){
						"#3778d0" 
					}else{
						"white"
					}
				}
			}
		}
	        border.color:"grey"
                z: -2
            }

        }

        onClicked: function (date) {
  
		if (startDate===undefined){
			startDate=date.getTime()
			if (!rangeDate){
				stopDate=date.getTime()
			}else{
				stopDate=undefined
			}
			getSelectedDate([date.toLocaleString(locale,"dd/MM/yyyy"),"start"])
		}else{
			if(stopDate=== undefined){
				stopDate=date.getTime()
				getSelectedDate([date.toLocaleString(locale,"dd/MM/yyyy"),"end"])
			}else{
				if (rangeDate){
					startDate=date.getTime()
					stopDate= undefined
					getSelectedDate([date.toLocaleString(locale,"dd/MM/yyyy"),"start"])
				}else{
					startDate=undefined
					stopDate=date.getTime()
					getSelectedDate([date.toLocaleString(locale,"dd/MM/yyyy"),"end"])
				}
			}
			if(stopDate<=startDate){
				if (!rangeDate){
					startDate=date.getTime()
					stopDate=date.getTime()
				}else{
					startDate=date.getTime()
					stopDate=undefined

				}
				getSelectedDate([date.toLocaleString(locale,"dd/MM/yyyy"),"start"])
			}
		}
		currentMonth=date.getMonth()
		fullMonth=date.toLocaleString(locale,'MMMM')
		currentYear=date.getFullYear()
        }

    }
}
