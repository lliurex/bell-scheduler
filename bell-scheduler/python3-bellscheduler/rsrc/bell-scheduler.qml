import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.12 as Kirigami
import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.3



ApplicationWindow {

    property bool closing: false
    id:mainWindow
    visible: true
    title: "Bell-Scheduler"
    property int margin: 1
    width: mainLayout.implicitWidth + 2 * margin
    height: mainLayout.implicitHeight + 2 * margin
    minimumWidth: mainLayout.Layout.minimumWidth + 2 * margin
    minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin
    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height/0.4
    }

    onClosing: {
        close.accepted=closing;
        bellSchedulerBridge.closeBellScheduler()
        delay(100, function() {
            if (bellSchedulerBridge.closeGui){
                closing=true,
                closeTimer.stop(),           
                mainWindow.close();
            }
        })
    }

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: margin
        Layout.minimumWidth:980
        Layout.minimumHeight:740

        RowLayout {
            id: bannerBox
            Layout.alignment:Qt.AlignTop

            Rectangle{
                color: "#000000"
                Layout.minimumWidth:mainLayout.width
                Layout.preferredWidth:mainLayout.width
                Layout.fillWidth:true
                Layout.minimumHeight:120
                Layout.maximumHeight:120
                Image{
                    id:banner
                    source: "/usr/lib/python3/dist-packages/bellscheduler/rsrc/bell-scheduler_banner.png"
                    asynchronous:true
                    anchors.centerIn:parent
                }
            }
        }

        StackView {
            id: mainView
            property int currentIndex:bellSchedulerBridge.currentStack
            Layout.minimumWidth: 932
            Layout.preferredWidth: 932
            Layout.alignment:Qt.AlignHCenter
            Layout.leftMargin:0
            Layout.fillWidth:true
            Layout.fillHeight: true
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
            /*
            Component{
                id:bellView
                BellOptions{
                    id:bellOptions
                }
            }
            */

        }

    }

    Timer{
        id:closeTimer
    }

    function delay(delayTime,cb){
        closeTimer.interval=delayTime;
        closeTimer.repeat=true;
        closeTimer.triggered.connect(cb);
        closeTimer.start()
    }

}

