import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.plasma.components as PC


Rectangle{
    width:120
    height:120
    border.color: "#d3d3d3"
    property alias currentImgIndex:imagesSelector.currentIndex
    property alias listEnabled:imagesSelector.enabled

    PC.ScrollView{
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
