import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.12
import org.kde.plasma.components 3.0 as PC3
import org.kde.plasma.components 2.0 as Components


Rectangle{
    width:120
    height:120
    border.color: "#d3d3d3"

    PC3.ScrollView{
        implicitWidth:parent.width
        implicitHeight:parent.height
        anchors.leftMargin:10

        ListView{
            id:imagesSelector
            anchors.centerIn:parent
            focus:true
            onCurrentIndexChanged:{
                console.log(imagesSelector.currentIndex)
            }
            currentIndex:1
            snapMode:ListView.SnapOneItem
            highlightRangeMode: ListView.StrictlyEnforceRange
                  
            model:bellSchedulerBridge.imagesModel
            /*
            ListModel{
                id:imgId
                ListElement{imageSource:"/usr/share/bell-scheduler/banners/ball.png"}
                ListElement{imageSource:"/usr/share/bell-scheduler/banners/bell.png"}
                ListElement{imageSource:"/usr/share/bell-scheduler/banners/bus-entrance.png"}
                ListElement{imageSource:"/usr/share/bell-scheduler/banners/bus-exit.png"}
                ListElement{imageSource:"/usr/share/bell-scheduler/banners/clock.png"}
                ListElement{imageSource:"/usr/share/bell-scheduler/banners/enter.png"}
                ListElement{imageSource:"/usr/share/bell-scheduler/banners/exit.png"}
                ListElement{imageSource:"/usr/share/bell-scheduler/banners/lunch.png"}
                ListElement{imageSource:"/usr/share/bell-scheduler/banners/playground.png"}
                ListElement{imageSource:"/usr/share/bell-scheduler/banners/sandwich.png"}
                ListElement{imageSource:"/usr/share/bell-scheduler/banners/school-bell.png"}
                ListElement{imageSource:"/usr/share/bell-scheduler/banners/swing.png"}
                ListElement{imageSource:"/home/lliurex/Pictures/06_ZeroCenter_ES.png"}

            }
            */   
            delegate:Item{
                width:90
                height:120

                Image{
                  width:80
                  height:80
                  fillMode:Image.PreserveAspectFit
                  source:imageSource
                  anchors.centerIn:parent
                  clip:true
                }

            }
                  
        }
    }
}
