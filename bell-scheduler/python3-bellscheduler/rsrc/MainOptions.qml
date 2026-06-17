import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

RowLayout{
    id: mainGrid
    spacing:10

    Rectangle{
        id:sideBar
        width:120
        Layout.fillHeight:true
        border.color:palette.mid

        ColumnLayout{
            id: menuGrid
            anchors.fill:parent
            spacing:0

            MenuOptionBtn {
                id:listItem
                Layout.fillWidth:true
                optionText:i18nd("bell-scheduler","Bells")
                optionIcon:"appointment-reminder"
                onMenuOptionClicked:mainStackBridge.moveToMainOptions(0)                
            }

            MenuOptionBtn {
                id:holidayItem
                Layout.fillWidth:true
                optionText:i18nd("bell-scheduler","Holidays")
                optionIcon:"view-calendar"
                onMenuOptionClicked:mainStackBridge.moveToMainOptions(1)
            }

            MenuOptionBtn {
                id:helpItem
                Layout.fillWidth:true
                optionText:i18nd("bell-scheduler","Help")
                optionIcon:"help-contents"
                onMenuOptionClicked:mainStackBridge.openHelp()
            }

            Item {
                Layout.fillHeight:true
            }
        }
    }

    StackView {
        id: optionsView
        Layout.fillWidth:true
        Layout.fillHeight:true

        property int currentIndex:mainStackBridge.mainCurrentOption

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
            NumberAnimation {
                property: "opacity"
                from: 0
                to: 1
                duration: 60
            }
        }
        replaceExit: Transition {
            NumberAnimation {
                property: "opacity"
                from: 1
                to: 0
                duration: 60
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

