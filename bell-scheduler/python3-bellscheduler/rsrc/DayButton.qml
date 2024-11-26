import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Item {
	id:dayBtnItem
	Layout.preferredWidth: 100
	Layout.preferredHeight: 40

	property alias dayBtnChecked:dayBtn.checked
	property alias dayBtnText:dayBtn.text
	signal dayBtnClicked(bool value)

	Button {
		id:dayBtn
		checkable:true
		checked:dayBtnChecked
		text:dayBtnText
		anchors.fill:parent
		//palette.button:paletteBtn(dayBtn.checked)
		//palette.buttonText:paletteBtnText(dayBtn.checked)
		contentItem:Label{
			text:dayBtn.text
			verticalAlignment:Text.AlignVCenter
			horizontalAlignment:Text.AlignHCenter
			color:paletteBtnText(dayBtn.checked)
		}
		background:Rectangle{
			anchors.fill:parent
			color:paletteBtn(dayBtn.checked)
			radius:5
			border.color:"#d2d2d3"
		}
		
		focusPolicy: Qt.NoFocus
		states: [
			State {
				name: "Hovering"
				PropertyChanges {
					target: dayBtn
					//palette.button: paletteBtn(dayBtn.checked,true)
					background.color:paletteBtn(dayBtn.checked,true)
					background.border.color:"#3daee9"
				}
			},
			State {
				name: "Exited"
				PropertyChanges {
					target: dayBtn
					//palette.button: paletteBtn(dayBtn.checked)
					background.color:paletteBtn(dayBtn.checked)
					background.border.color:"#d2d2d3"
				}
			}
		]

		MouseArea {
			id: mouseAreaDay
			anchors.fill: parent
			hoverEnabled:true
			onEntered: {
				parent.state="Hovering"
			}
			onExited: {
				parent.state="Exited"
			}
			onClicked: {
				dayBtn.checked=!dayBtn.checked,
				dayBtnClicked(dayBtn.checked),
				//parent.palette.button=paletteBtn(dayBtn.checked);
				parent.background.color=paletteBtn(dayBtn.checked)
			}
		}		
					
	}

	function paletteBtn(status,mouseArea=false){
		if (daysLayout.enabled){
			if (status){
				if (mouseArea){
					return "#add8e6";
				}else{
					return "#3daee9";
				}
			}else{ 
				//return "#e4e5e7";
				return "#ffffff"
			}
		}else{
			if (status){
				return "#87cefa";
			}else{
				return "#e4e5e7";
			}
		}	
	}

	function paletteBtnText(status){
		if (daysLayout.enabled){
			if (status){
				return "#ffffff";
			}else{ 
				return "#000000";
			}
		}else{
			if (status){
				return "#ffffff";
			}else{
				return "#b9babc";
			}
		}	
	}
}
