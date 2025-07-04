import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


GridLayout{
    id: bellGrid
    columns: 2
    flow: GridLayout.LeftToRight
    columnSpacing:10

    GridLayout{
        rows:2
        flow: GridLayout.TopToBottom

        MenuOptionBtn {
            id:goBackBtn
            optionText:i18nd("bell-scheduler","Bells")
            optionFontSize:14
            optionIcon:"/usr/share/icons/breeze/actions/24/go-previous.svg"
            Connections{
                function onMenuOptionClicked(){
                    bellStackBridge.goHome();
                }
            }
        }  
        Rectangle{
            width:120
            /*Layout.minimumHeight:475*/
            Layout.fillHeight:true
            border.color: "#d3d3d3"
            GridLayout{
                id: menuGrid
                rows:1 
                flow: GridLayout.TopToBottom
                rowSpacing:0

                MenuOptionBtn {
                    id:infoItem
                    optionText:i18nd("bell-scheduler","Bell")
                    optionIcon:"/usr/share/icons/breeze/status/22/appointment-reminder.svg"
                 }

            }
        }
    }

    StackView {
        id: manageView
        property int currentOption:bellStackBridge.bellCurrentOption
        Layout.fillWidth:true
        Layout.fillHeight: true
        initialItem:emptyView

        onCurrentOptionChanged:{
            switch(currentOption){
                case 0:
                    manageView.replace(emptyView)
                case 1:
                    manageView.replace(bellView)
            }

        }
        replaceEnter: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 0
                to:1
                duration: 60
            }
        }
        replaceExit: Transition {
            PropertyAnimation {
                property: "opacity"
                from: 1
                to:0
                duration: 60
            }
        }

        Component{
            id:emptyView
            Item{
                id:emptyPanel
            }
        }
        
        Component{
            id:bellView
            BellForm{
                id:bellForm
            }
        }
        
    }
}

