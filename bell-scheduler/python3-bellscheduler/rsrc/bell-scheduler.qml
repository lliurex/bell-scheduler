import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window

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
        x = Screen.width / 2  - minimumWidth/2
        y = Screen.height / 2 - minimumHeight/2
    }

    onClosing:(close)=> {
        close.accepted=closing;
        mainStackBridge.closeBellScheduler()
        delay(100, function() {
            if (mainStackBridge.closeGui){
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
        Layout.minimumHeight:700

        RowLayout {
            id: bannerBox
            Layout.alignment:Qt.AlignTop

            Rectangle{
                color: "#0049ab"
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
            property int currentIndex:mainStackBridge.currentStack
            Layout.alignment:Qt.AlignHCenter|Qt.AlignVCenter
            Layout.leftMargin:0
            Layout.fillWidth:true
            Layout.fillHeight: true
            Layout.minimumHeight:575
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

