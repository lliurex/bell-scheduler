import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


RowLayout{
    id: bellGrid
    spacing:10

    ColumnLayout{
        Layout.fillHeight:true
        spacing:5

        MenuOptionBtn {
            id:goBackBtn
            optionText:i18nd("bell-scheduler","Bells")
            optionPointSize:14
            optionIcon:"actions/24/go-previous.svg"
            onMenuOptionClicked:bellStackBridge.goHome()
        }

        Rectangle{
            width:120
            Layout.fillHeight:true
            border.color: palette.mid
            ColumnLayout{
                anchors.fill:parent
                spacing:0

                MenuOptionBtn {
                    id:infoItem
                    optionText:i18nd("bell-scheduler","Bell")
                    optionIcon:"status/24/appointment-reminder.svg"
                }

                Item{
                    Layout.fillHeight:true
                }

            }
        }
    }

    StackView {
        id: manageView
        Layout.fillWidth:true
        Layout.fillHeight: true

        property int currentOption:bellStackBridge.bellCurrentOption

        initialItem:emptyView

        onCurrentOptionChanged:{
            switch(currentOption){
                case 0:
                    manageView.replace(emptyView)
                    break
                case 1:
                    manageView.replace(bellView)
                    break
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

