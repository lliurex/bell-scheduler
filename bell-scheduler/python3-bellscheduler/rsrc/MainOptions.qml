import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


GridLayout{
    id: mainGrid
    columns: 2
    flow: GridLayout.LeftToRight
    columnSpacing:10

    Rectangle{
        width:120
        Layout.fillHeight:true
        border.color: "#d3d3d3"

        GridLayout{
            id: menuGrid
            rows:3 
            flow: GridLayout.TopToBottom
            rowSpacing:0

            MenuOptionBtn {
                id:listItem
                optionText:i18nd("bell-scheduler","Bells")
                optionIcon:"/usr/share/icons/breeze/status/22/appointment-reminder.svg"
               
                Connections{
                    function onMenuOptionClicked(){
                        mainStackBridge.moveToMainOptions(0)
                    }
                }
                
            }
            MenuOptionBtn {
                id:holidayItem
                optionText:i18nd("bell-scheduler","Holidays")
                optionIcon:"/usr/share/icons/breeze/actions/22/view-calendar.svg"
                
                Connections{
                    function onMenuOptionClicked(){
                        mainStackBridge.moveToMainOptions(1)
                    }
                }
                
            }
            MenuOptionBtn {
                id:helpItem
                optionText:i18nd("bell-scheduler","Help")
                optionIcon:"/usr/share/icons/breeze/actions/22/help-contents.svg"
                Connections{
                    function onMenuOptionClicked(){
                        mainStackBridge.openHelp();
                    }
                }
            }
        }
    }

    StackView {
        id: optionsView
        property int currentIndex:mainStackBridge.mainCurrentOption
        Layout.fillWidth:true
        Layout.fillHeight:true
        initialItem:bellsView

        onCurrentIndexChanged:{
            switch(currentIndex){
                case 0:
                    optionsView.replace(bellsView)
                    break;
                case 1:
                    optionsView.replace(holidayView)
                    break;
            }
        }
        replaceEnter: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 0
                to:1
                duration: 600
            }
        }
        replaceExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to:0
                duration: 600
            }
        }
        Component{
            id:bellsView
            BellsManager{
                id:bellsManager
            }
        }

        Component{
            id:holidayView
            HolidayManager{
                id:holidayManager
            }
        }
        
       
    }
}

