import QtQuick 2.6
import Edupals.N4D.Agent 1.0 as N4DAgent


Rectangle {
    width:  childrenRect.width+5
    height:  childrenRect.height+5
    anchors.centerIn: parent
    color: "#e9e9e9"

    N4DAgent.Login
    {
        showAddress:false
        address:"localhost"
        showCancel: false
        inGroups:["sudo","admins","teachers"]
        
        /*anchors.centerIn: parent*/
        
        onLogged: {
            tunnel.on_ticket(ticket);
        }
    }
}
