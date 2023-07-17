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
            currentIndex:bellSchedulerBridge.bellImage[1]
            snapMode:ListView.SnapOneItem
            highlightRangeMode: ListView.StrictlyEnforceRange
                  
            model:bellSchedulerBridge.imagesModel
           
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
