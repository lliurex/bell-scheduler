import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15

ApplicationWindow {

    property bool closing: false
    id:mainWindow
    visible: true
    title: "Bell-Scheduler"
    property int margin: 1
    width: mainLayout.implicitWidth + 2 * margin
    height: mainLayout.implicitHeight + 2 * margin
    minimumWidth: 980 + 2 * margin
    minimumHeight: 670 + 2 * margin
    Component.onCompleted: {
        x = Screen.width / 2  - minimumWidth/2
        y = Screen.height / 2 - minimumHeight/2
    }

    onClosing: {
        close.accepted = closing;
        if (!closing) {
            mainStackBridge.closeBellScheduler();
            closeTimer.start();
        }
    }

    Timer {
        id: closeTimer
        interval: 100
        repeat: true
        onTriggered: {
            if (mainStackBridge.closeGui) {
                stop();
                mainWindow.closing = true;
                mainWindow.close();
            }
        }
    }

    ColumnLayout {
        id: mainLayout
        anchors.fill:parent

        Rectangle{
            color: "#0049ab"
            Layout.fillWidth: true
            Layout.preferredHeight: 120

            Image{
                id:banner
                source: "/usr/lib/python3/dist-packages/bellscheduler/rsrc/bell-scheduler_banner.png"
                asynchronous:false
                anchors.centerIn: parent
                fillMode: Image.PreserveAspectFit
            }
        }

        StackView {
            id: mainView
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight:545

            property int currentIndex:mainStackBridge.currentStack
            initialItem:loadView
            
            onCurrentIndexChanged:{
                switch (currentIndex){
                    case 0:
                        mainView.replace(loadView)
                        break;
                    case 1:
                        mainView.replace(listView)
                        break;
                    case 2:
                        mainView.replace(bellView)
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
                id:loadView
                LoadWaiting{
                    id:loadWaiting
                }
            }
            Component{
                id:listView
                MainOptions{
                    id:mainOptions
                }
            }
            Component{
                id:bellView
                BellOptions{
                    id:bellOptions
                }
            }
        }

    }


    CustomPopUp{
        id:waitingPopUp
    }

}

