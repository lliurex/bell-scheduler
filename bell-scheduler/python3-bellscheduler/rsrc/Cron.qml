import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


GridLayout{
	id:scheduler
	rows:2
	flow: GridLayout.TopToBottom

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
				font.pointSize: 40
				color:"#3daee9"
				text:formatText(Tumbler.tumbler.count,modelData)
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
					onWheel:(wheel)=>{
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
		    height: 60
		    width: 60
		    color:"transparent"
		    Tumbler {
		    	id: hoursTumbler
		    	width:60
	            height:60
	            model: 24
	            currentIndex:bellStackBridge.bellCron[0]
	            delegate:delegateComponent 
	            visibleItemCount:1
	            hoverEnabled:true
	        	ToolTip.delay: 1000
	            ToolTip.timeout: 3000
	            ToolTip.visible: hovered
	            ToolTip.text:i18nd("bell-scheduler","You can use the mouse wheel to change the hour")
	            onCurrentIndexChanged: {
	            	bellStackBridge.updateClockValues(["H",hoursTumbler.currentIndex]);
	            } 
	        }       
		}
		Text{
			id:clockSeparator
	       	Layout.alignment:Qt.AlignCenter
	       	font.pointSize:40
			color:"#3daee9"
			text:":"
	    }
	    Rectangle {
	    	anchors.topMargin: 4
	       	Layout.alignment:Qt.AlignCenter
	    	height: 60
	    	width: 60
	    	color:"transparent"

	    	Tumbler {
	    		id: minutesTumbler
	    		height:60
	    		width:60
	    		model: 60
	    		currentIndex:bellStackBridge.bellCron[1]
	    		delegate: delegateComponent
	    		visibleItemCount:1
	    		hoverEnabled:true
	    	 	ToolTip.delay: 1000
	    	 	ToolTip.timeout: 3000
	    	 	ToolTip.visible: hovered
	    	 	ToolTip.text:i18nd("bell-scheduler","You can use the mouse wheel to change the minutes")
	    		onCurrentIndexChanged: {
	    			bellStackBridge.updateClockValues(["M",minutesTumbler.currentIndex]);
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
			ToolTip.text:i18nd("bell-scheduler","Click to edit time with keyboard ")
			onClicked:{
				timeSelector.open()
			}
			TimeSelector{
				id:timeSelector
				hourEntry:formatEditText(hoursTumbler.currentIndex)
				minuteEntry:formatEditText(minutesTumbler.currentIndex)
				Connections{
					target:timeSelector
					function onTimeApplyClicked(hourValue,minuteValue){
						hoursTumbler.currentIndex=hourValue
						minutesTumbler.currentIndex=minuteValue
					}
				}

			}
		} 
	}	

	RowLayout {
		id: daysLayout
		enabled:true
	    Layout.alignment:Qt.AlignHCenter
	    Layout.fillWidth: true
	    Layout.bottomMargin: 5
	    spacing:8

	    DayButton {
	      	id:mondaybtn
			dayBtnChecked:bellStackBridge.bellDays[0]
			dayBtnText:i18nd("bell-scheduler","Monday")
			Connections{
				function onDayBtnClicked(value){
					bellStackBridge.updateWeekDaysValues(["MO",value]);	
				}
			}
					
		}
				
		DayButton {
	       	id:tuesdaybtn
			dayBtnChecked:bellStackBridge.bellDays[1]
			dayBtnText:i18nd("bell-scheduler","Tuesday")
			Connections{
				function onDayBtnClicked(value){
					bellStackBridge.updateWeekDaysValues(["TU",value]);
				}
			}
		}
		
		DayButton {
			id:wednesdaybtn
			dayBtnChecked:bellStackBridge.bellDays[2]
			dayBtnText:i18nd("bell-scheduler","Wednesday")
			Connections{
				function onDayBtnClicked(value){
					bellStackBridge.updateWeekDaysValues(["WE",value]);
				}
			}
			
		}
				
		DayButton {
			id:thursdaybtn
			dayBtnChecked:bellStackBridge.bellDays[3]
			dayBtnText:i18nd("bell-scheduler","Thursday")
			Connections{
				function onDayBtnClicked(value){
					bellStackBridge.updateWeekDaysValues(["TH",value]);
				}
			}
		}
			
		DayButton {
			id:fridaybtn
			dayBtnChecked:bellStackBridge.bellDays[4]
			dayBtnText:i18nd("bell-scheduler","Friday")
			Connections{
				function onDayBtnClicked(value){
					bellStackBridge.updateWeekDaysValues(["FR",value]);
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
