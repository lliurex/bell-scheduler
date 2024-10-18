import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

GridLayout{
	rows:3
	flow: GridLayout.TopToBottom
	Layout.leftMargin:90
	Layout.rightMargin:90
	
	property alias startDate:monthGrid.startDate
	property alias stopDate:monthGrid.stopDate
	property alias initDate:monthGrid.initDate
	property alias endDate:monthGrid.endDate
	property alias rangeDate:monthGrid.rangeDate
	property alias daysInRange:monthGrid.daysInRange
	property alias currentLocale:monthGrid.locale
	property alias currentMonth:monthGrid.month
	property alias fullMonth:monthGrid.fullMonth
	property alias currentYear:monthGrid.year
	signal getSelectedDate (variant value)
	
	RowLayout{
		Rectangle{
			id:removeContainer
			width:50
			height:50
			border.color: "transparent"
			color:"transparent"
			
			Text{
				id:removeText
				text:"<"
				color:"#787878"
				font.pointSize: 25
				verticalAlignment: Text.AlignVCenter
				anchors.centerIn:removeContainer
				MouseArea {
					id: mouseAreaRemove
					anchors.fill: parent
					hoverEnabled: true
					onEntered: {
						removeContainer.color="#ffffff"
					}
					onExited: {
						removeContainer.color="transparent"
					}
					onClicked:{
						if (currentMonth>0 && currentMonth<12){
							currentMonth=currentMonth-1
							fullMonth=currentLocale.monthName(currentMonth).split(" ").slice(-1)[0]
						}else{
							currentMonth=11
							currentYear=currentYear-1
							fullMonth=currentLocale.monthName(currentMonth).split(" ").slice(-1)[0]
						}
					}
				}
			}
		}
		Text{
			text:fullMonth+" "+currentYear
			font.pointSize:18
			Layout.fillWidth:true
			horizontalAlignment: Text.AlignHCenter
		}
		Rectangle{
			id:addContainer
			width:50
			height:50
			border.color: "transparent"
			color:"transparent"

			Text{
				id:addText
				text:">"
				font.pointSize: 25
				color:"#787878"
				verticalAlignment: Text.AlignVCenter
				anchors.centerIn:addContainer
				MouseArea {
					id: mouseAreaAdd
					anchors.fill: parent
					hoverEnabled: true
					onEntered: {
						addContainer.color="#ffffff"
					}
					onExited: {
						addContainer.color="transparent"
					}
					onClicked:{
						if (currentMonth<11){
							currentMonth=currentMonth+1
							fullMonth=currentLocale.monthName(currentMonth).split(" ").slice(-1)[0]
						}else{
							currentMonth=0
							currentYear=currentYear+1
							fullMonth=currentLocale.monthName(currentMonth).split(" ").slice(-1)[0]
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
		id:monthGrid
		Layout.fillWidth: true
		Layout.fillHeight:true

		property var startDate: startDate
		property var stopDate: stopDate
		property var initDate:initDate
		property var endDate:endDate
		property var daysInRange:daysInRange
		property bool rangeDate:rangeDate
		property var fullMonth:fullMonth
		month: currentMonth
		year: currentYear
		locale: currentLocale

		delegate: Text {
			property MonthGrid control: monthGrid
			horizontalAlignment: Text.AlignHCenter
			verticalAlignment: Text.AlignVCenter
			opacity: model.month === control.month ? 1 : 0.5
			text: day
			font.pointSize: 10
			Rectangle {
				anchors.fill: parent
				anchors.margins: -4
				color: {
					if (monthGrid.startDate===undefined && monthGrid.stopDate=== undefined){
						if ((model.date.toLocaleString(locale,"dd/MM/yyyy")===monthGrid.initDate)||(model.date.toLocaleString(locale,"dd/MM/yyyy")===monthGrid.endDate)){
							"#3778d0"
						}else{
							if (monthGrid.daysInRange.includes(model.date.toLocaleString(locale,"dd/MM/yyyy"))){
								"#55555555"
							}else{
								"white"
							}
						}
					}else{
						if ((model.date.getTime()>monthGrid.startDate) && (model.date.getTime()< monthGrid.stopDate)){
							"#55555555"
						}else{
							if (monthGrid.startDate !==undefined && model.date.getTime()===monthGrid.startDate || monthGrid.stopDate !==undefined && model.date.getTime()===monthGrid.stopDate){
								"#3778d0" 
							}else{
								"white"
							}
						}
					}
				}
				border.color:"#d3d3d3"
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
			fullMonth=date.toLocaleString(locale,'MMMM').split(" ").slice(-1)[0]
			currentYear=date.getFullYear()
		}

	}	
}
