import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12


GridLayout{
    id: optionsGrid
    columns: 2
    flow: GridLayout.LeftToRight
    columnSpacing:10

    Rectangle{
        width:150
        Layout.minimumHeight:600
        Layout.fillHeight:true
        border.color: "#d3d3d3"

        GridLayout{
            id: menuGrid
            rows:4 
            flow: GridLayout.TopToBottom
            rowSpacing:0

            MenuOptionBtn {
                id:listItem
                optionText:i18nd("bell-scheduler","Bells")
                optionIcon:"/usr/share/icons/breeze/status/22/appointment-reminder.svg"
                /*
                Connections{
                    function onMenuOptionClicked(){
                        if (!onedriveBridge.requiredMigration){
                            onedriveBridge.moveToSpaceOption(0);
                        }
                    }
                }
                */
            }
            MenuOptionBtn {
                id:backupItem
                optionText:i18nd("bell-scheduler","Backup")
                optionIcon:"/usr/share/icons/breeze/actions/22/backup.svg"
                /*
                Connections{
                    function onMenuOptionClicked(){
                        if (!onedriveBridge.requiredMigration){
                            onedriveBridge.moveToSpaceOption(0);
                        }
                    }
                }
                */
            }
            MenuOptionBtn {
                id:holidayItem
                optionText:i18nd("bell-scheduler","Holiday manager")
                optionIcon:"/usr/share/icons/breeze/actions/22/view-calendar.svg"
                /*
                Connections{
                    function onMenuOptionClicked(){
                        if (!onedriveBridge.requiredMigration){
                            onedriveBridge.moveToSpaceOption(0);
                        }
                    }
                }
                */
            }

            MenuOptionBtn {
                id:helpItem
                optionText:i18nd("bell-scheduler","Help")
                optionIcon:"/usr/share/icons/breeze/actions/22/help-contents.svg"
                /*
                Connections{
                    function onMenuOptionClicked(){
                        onedriveBridge.openHelp();
                    }
                }
                */
            }
        }
    }

    StackView {
        id: optionsView
        property int currentIndex:bellSchedulerBridge.mainCurrentOption
        Layout.fillWidth:true
        Layout.fillHeight:true
        initialItem:bellsInfoView

        onCurrentIndexChanged:{
            switch(currentIndex){
                case 0:
                    optionsView.replace(bellsInfoView)
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
            id:bellsInfoView
            BellsInfo{
                id:bellsInfo
            }
        }
        
       
    }
}

