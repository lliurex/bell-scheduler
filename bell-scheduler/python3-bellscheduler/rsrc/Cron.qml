import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


GridLayout{
	id:scheduler
	rows:2
	flow: GridLayout.TopToBottom

	property alias clockLayoutEnabled:clockLayout.enabled
	property alias daysLayoutEnabled:daysLayout.enabled
	
	GridLayout {
		id:clockLayout
		enabled:true
		Layout.leftMargin: 5
		Layout.rightMargin:5
		Layout.bottomMargin: 5
		Layout.alignment:Qt.AlignHCenter
		columns:4
		Component {
			id: delegateComponent
			Label {
				font.pointSize: 55
				color: clockLayout.enabled? "#3daee9":"#87cefa"
				text: formatText(Tumbler.tumbler.count, modelData)
				horizontalAlignment: Text.AlignHCenter
				verticalAlignment: Text.AlignVCenter
				MouseArea {
					id: mouseAreaHour
					anchors.fill: parent
					hoverEnabled: true
					onEntered: {
						parent.color="#add8e6"
					}
					onExited: {
						parent.color="#3daee9"
					}
					onWheel:{
						wheel.accepted=false
						if (wheel.angleDelta.y>0){
							if (modelData==0){
								if (Tumbler.tumbler.count==24){
									Tumbler.tumbler.currentIndex=23;
								}else{
									Tumbler.tumbler.currentIndex=59;
								}
							}else{
								Tumbler.tumbler.currentIndex=modelData-1;
							}
						}else{
							if (modelData==23){
								if (Tumbler.tumbler.count==24){
									Tumbler.tumbler.currentIndex=0;
								}else{
									Tumbler.tumbler.currentIndex=modelData+1;
								}
							}else{ 
								if (modelData==59){
									if (Tumbler.tumbler.count==60){
										Tumbler.tumbler.currentIndex=0;
									}else{
										Tumbler.tumbler.currentIndex=modelData+1;
									}
								}else{
									Tumbler.tumbler.currentIndex=modelData+1;
								}
							}
						}
					}
				}
			}
		}
			 
		Rectangle {
			anchors.topMargin: 4
	       	Layout.alignment:Qt.AlignCenter
		    height: 80
		    width: 80
		    color:"transparent"
		    Tumbler {
		    	id: hoursTumbler
		    	width:80
	            height:80
	            model: 24
	            currentIndex:bellSchedulerBridge.bellCron[0]
	            delegate:delegateComponent 
	            visibleItemCount:1
	            hoverEnabled:true
	        	ToolTip.delay: 1000
	            ToolTip.timeout: 3000
	            ToolTip.visible: hovered
	            ToolTip.text:i18nd("bell-scheduler","You can use the mouse wheel to change the hour")
	            onCurrentIndexChanged: {
	            	bellSchedulerBridge.updateClockValues(["H",hoursTumbler.currentIndex]);
	            } 
	        }       
		}
		Text{
			id:clockSeparator
	       	Layout.alignment:Qt.AlignCenter
	       	font.pointSize:55
			color: clockLayout.enabled? "#3daee9":"#87cefa"
			text:":"
	    }
	    Rectangle {
	    	anchors.topMargin: 4
	       	Layout.alignment:Qt.AlignCenter
	    	height: 80
	    	width: 80
	    	color:"transparent"

	    	Tumbler {
	    		id: minutesTumbler
	    		height:80
	    		width:80
	    		model: 60
	    		currentIndex:bellSchedulerBridge.bellCron[1]
	    		delegate: delegateComponent
	    		visibleItemCount:1
	    		hoverEnabled:true
	    	 	ToolTip.delay: 1000
	    	 	ToolTip.timeout: 3000
	    	 	ToolTip.visible: hovered
	    	 	ToolTip.text:i18nd("bell-scheduler","You can use the mouse wheel to change the minutes")
	    		onCurrentIndexChanged: {
	    			bellSchedulerBridge.updateClockValues(["M",minutesTumbler.currentIndex]);
	    		}
	    	}
		} 
		Button {
			id:editHourBtn
			display:AbstractButton.IconOnly
			icon.name:"edit-entry.svg"
			Layout.preferredHeight: 35
	       	Layout.alignment:Qt.AlignCenter
			Layout.topMargin:10
			Layout.leftMargin:10
			hoverEnabled:true
			ToolTip.delay: 1000
			ToolTip.timeout: 3000
			ToolTip.visible: hovered
			ToolTip.text:i18nd("bell-scheduler","Click to edit shutdown time with keyboard ")
			onClicked:{
				hourEntry.text=formatEditText(hoursTumbler.currentIndex),
				minuteEntry.text=formatEditText(minutesTumbler.currentIndex),
				popupEditHour.open();
			}
			Popup {
				id: popupEditHour
				x: Math.round(parent.width/ 2)
       			y: Math.round(parent.height)
				rightMargin:popupEditHour.width
				width: 205
				height: 170
				modal: true
				focus: true
				closePolicy: Popup.NoAutoClose
				enter: Transition {
				        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0 }
				}
				exit: Transition {
					NumberAnimation { property: "opacity"; from: 1.0; to: 0.0 }
    			}
				GridLayout{
					id:popupGrid
					rows:3
					flow: GridLayout.TopToBottom
					RowLayout {
						id: popupHourLayout
					    Layout.alignment:Qt.AlignHCenter
					    Layout.fillWidth: true
					    Layout.bottomMargin: 10
					    spacing:4
				    	TextField{
				    		id: hourEntry
				    		validator: RegExpValidator { regExp: /([0-1][0-9]|2[0-3])/ }
				    		implicitWidth: 70
				    		horizontalAlignment: TextInput.AlignHCenter
				    		color:"#3daee9"
				    		font.pointSize: 40
				    	}

				    	Text{
							font.pointSize:40
							color:"#3daee9"
							text:":"
				    	}
				    	
				    	TextField{
				    		id: minuteEntry
				    		validator: RegExpValidator { regExp: /[0-5][0-9]/ }
				    		implicitWidth: 70
				    		horizontalAlignment: TextInput.AlignHCenter
				    		color:"#3daee9"
				    		font.pointSize: 40
				    	}
				    }

			    	RowLayout {
					   id: footPopup
					   Layout.fillWidth: true
					   Layout.bottomMargin: 10

					   Layout.alignment:Qt.AlignHCenter
					   spacing:8

					   Button {
					   		id:cancelEditBtn
						   	display:AbstractButton.TextBesideIcon
						   	icon.name:"dialog-cancel.svg"
						   	text:i18nd("bell-scheduler","Cancel")
						   	Layout.preferredHeight: 40
						   	onClicked:{
						   		popupEditHour.close();
					   		}
					 	}
					 	Button {
							id:applyEditBtn
						   	display:AbstractButton.TextBesideIcon
						   	icon.name:"dialog-ok-apply.svg"
						   	text:i18nd("bell-scheduler","Apply")
						   	Layout.preferredHeight: 40
						   	onClicked:{
						   		if (validateEntry(hourEntry.text,minuteEntry.text)){
						   			hoursTumbler.currentIndex=hourEntry.text,
						   			minutesTumbler.currentIndex=minuteEntry.text,
									delay(1000, function() {
										popupEditHour.close();
							        })
							    }else{
							    	popupEditHour.close();
							    }
						   		
					   		}
					 	}
					}      

			    }
			}
		} 
	}	

	RowLayout {
		id: daysLayout
		enabled:daysLayoutEnabled
	    Layout.alignment:Qt.AlignHCenter
	    Layout.fillWidth: true
	    Layout.bottomMargin: 5
	    spacing:8

	    DayButton {
	      	id:mondaybtn
			dayBtnChecked:bellSchedulerBridge.bellDays[0]
			dayBtnText:i18nd("bell-scheduler","Monday")
			Connections{
				function onDayBtnClicked(value){
					bellSchedulerBridge.updateWeekDaysValues(["MO",value]);	
				}
			}
					
		}
				
		DayButton {
	       	id:tuesdaybtn
			dayBtnChecked:bellSchedulerBridge.bellDays[1]
			dayBtnText:i18nd("bell-scheduler","Tuesday")
			Connections{
				function onDayBtnClicked(value){
					bellSchedulerBridge.updateWeekDaysValues(["TU",value]);
				}
			}
		}
		
		DayButton {
			id:wednesdaybtn
			dayBtnChecked:bellSchedulerBridge.bellDays[2]
			dayBtnText:i18nd("bell-scheduler","Wednesday")
			Connections{
				function onDayBtnClicked(value){
					bellSchedulerBridge.updateWeekDaysValues(["WE",value]);
				}
			}
			
		}
				
		DayButton {
			id:thursdaybtn
			dayBtnChecked:bellSchedulerBridge.bellDays[3]
			dayBtnText:i18nd("bell-scheduler","Thursday")
			Connections{
				function onDayBtnClicked(value){
					bellSchedulerBridge.updateWeekDaysValues(["TH",value]);
				}
			}
		}
			
		DayButton {
			id:fridaybtn
			dayBtnChecked:bellSchedulerBridge.bellDays[4]
			dayBtnText:i18nd("bell-scheduler","Friday")
			Connections{
				function onDayBtnClicked(value){
					bellSchedulerBridge.updateWeekDaysValues(["FR",value]);
				}
			}
		}
	}

	

	function formatText(count, modelData) {
        var data = count === 12 ? modelData + 1 : modelData;
        return data.toString().length < 2 ? "0" + data : data;
    }
    
    function formatEditText(value){
    	if (value<10){
    		return "0"+value.toString();
    	}else{
    		return value.toString();
    	}

    }

    function validateEntry(hour,minute){

    	if ((hour =="") || (minute=="")){
    		console.log("Vacio");
    		return false;
    	}else{
    		return true;
    	}

    }
    Timer {
        id: timer
    }

    function delay(delayTime, cb) {
        timer.interval = delayTime;
        timer.repeat = false;
        timer.triggered.connect(cb);
        timer.start();
    }
}				
