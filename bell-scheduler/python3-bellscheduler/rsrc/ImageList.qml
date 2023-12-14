import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.plasma.components 3.0 as PC3


Rectangle{
    width:120
    height:120
    border.color: "#d3d3d3"
    property alias currentImgIndex:imagesSelector.currentIndex
    property alias listEnabled:imagesSelector.enabled

    PC3.ScrollView{
        implicitWidth:parent.width
        implicitHeight:parent.height
        anchors.leftMargin:10

        ListView{
            id:imagesSelector
            anchors.centerIn:parent
            focus:true
            currentIndex:currentImgIndex
            snapMode:ListView.SnapOneItem
            highlightRangeMode: ListView.StrictlyEnforceRange
            enabled:listEnabled   
            model:bellStackBridge.imagesModel
           
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
