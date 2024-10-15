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
		palette.button:paletteBtn(dayBtn.checked)
		palette.buttonText:paletteBtnText(dayBtn.checked)
		focusPolicy: Qt.NoFocus
		states: [
			State {
				name: "Hovering"
				PropertyChanges {
					target: dayBtn
					palette.button: paletteBtn(dayBtn.checked,true)
				}
			},
			State {
				name: "Exited"
				PropertyChanges {
					target: dayBtn
					palette.button: paletteBtn(dayBtn.checked)
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
				parent.palette.button=paletteBtn(dayBtn.checked);
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
				return "#e4e5e7";
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
