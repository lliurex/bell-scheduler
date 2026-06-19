import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: calendarRoot
    spacing: 10

    property var startDate: undefined
    property var stopDate: undefined
    property string initDate: ""
    property string endDate: ""
    property bool rangeDate: false
    property var daysInRange: []
    property var currentLocale: Qt.locale()
    property int currentMonth: new Date().getMonth()
    property string fullMonth: ""
    property int currentYear: new Date().getFullYear()

    signal getSelectedDate(var value)

    RowLayout {
        Layout.fillWidth: true

        Rectangle {
            id: removeContainer
            width: 50
            height: 50
            border.color: "transparent"
            color: "transparent"

            Text {
                id: removeText
                text: "<"
                color: "#787878"
                font.pointSize: 25
                verticalAlignment: Text.AlignVCenter
                anchors.centerIn: removeContainer

                MouseArea {
                    id: mouseAreaRemove
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: removeContainer.color = "#ffffff"
                    onExited: removeContainer.color = "transparent"
                    onClicked: {
                        if (calendarRoot.currentMonth > 0) {
                            calendarRoot.currentMonth -= 1;
                        } else {
                            calendarRoot.currentMonth = 11;
                            calendarRoot.currentYear -= 1;
                        }
                        calendarRoot.fullMonth = calendarRoot.currentLocale.monthName(calendarRoot.currentMonth).split(" ").slice(-1)[0];
                    }
                }
            }
        }

        Text {
            text: calendarRoot.fullMonth + " " + calendarRoot.currentYear
            font.pointSize: 18
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
        }

        Rectangle {
            id: addContainer
            width: 50
            height: 50
            border.color: "transparent"
            color: "transparent"

            Text {
                id: addText
                text: ">"
                font.pointSize: 25
                color: "#787878"
                verticalAlignment: Text.AlignVCenter
                anchors.centerIn: addContainer

                MouseArea {
                    id: mouseAreaAdd
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: addContainer.color = "#ffffff"
                    onExited: addContainer.color = "transparent"
                    onClicked: {
                        if (calendarRoot.currentMonth < 11) {
                            calendarRoot.currentMonth += 1;
                        } else {
                            calendarRoot.currentMonth = 0;
                            calendarRoot.currentYear += 1;
                        }
                        calendarRoot.fullMonth = calendarRoot.currentLocale.monthName(calendarRoot.currentMonth).split(" ").slice(-1)[0];
                    }
                }
            }
        }
    }

    DayOfWeekRow {
        locale: calendarRoot.currentLocale
        Layout.fillWidth: true
    }

    MonthGrid {
        id: monthGrid
        Layout.fillWidth: true
        Layout.fillHeight: true
        month: calendarRoot.currentMonth
        year: calendarRoot.currentYear
        locale: calendarRoot.currentLocale

        delegate: Text {
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            opacity: model.month === monthGrid.month ? 1 : 0.5
            text: model.day
            font.pointSize: 10

            readonly property string cellFormattedDate: Qt.formatDate(model.date, "dd/MM/yyyy")

            Rectangle {
                anchors.fill: parent
                anchors.margins: -4
                border.color: "#d3d3d3"
                z: -2

                color: {
                    if (calendarRoot.startDate === undefined && calendarRoot.stopDate === undefined) {
                        if (cellFormattedDate === calendarRoot.initDate || cellFormattedDate === calendarRoot.endDate) {
                            return "#3778d0";
                        }
                        if (calendarRoot.daysInRange.includes(cellFormattedDate)) {
                            return "#55555555";
                        }
                        return "white";
                    }
                    else {
                        let cellTime = model.date.getTime();
                        if (cellTime > calendarRoot.startDate && cellTime < calendarRoot.stopDate) {
                            return "#55555555";
                        }
                        if ((calendarRoot.startDate !== undefined && cellTime === calendarRoot.startDate) ||
                            (calendarRoot.stopDate !== undefined && cellTime === calendarRoot.stopDate)) {
                            return "#3778d0";
                        }
                        return "white";
                    }
                }
            }
        }

        onClicked: (date) => {
            let dateTime = date.getTime();
            let cellFormatted = Qt.formatDate(date, "dd/MM/yyyy");

            if (calendarRoot.startDate === undefined) {
                calendarRoot.startDate = dateTime;
                calendarRoot.stopDate = !calendarRoot.rangeDate ? dateTime : undefined;
                calendarRoot.getSelectedDate([cellFormatted, "start"]);
            } else {
                if (calendarRoot.stopDate === undefined) {
                    calendarRoot.stopDate = dateTime;
                    calendarRoot.getSelectedDate([cellFormatted, "end"]);
                } else {
                    if (calendarRoot.rangeDate) {
                        calendarRoot.startDate = dateTime;
                        calendarRoot.stopDate = undefined;
                        calendarRoot.getSelectedDate([cellFormatted, "start"]);
                    } else {
                        calendarRoot.startDate = undefined;
                        calendarRoot.stopDate = dateTime;
                        calendarRoot.getSelectedDate([cellFormatted, "end"]);
                    }
                }

                if (calendarRoot.stopDate <= calendarRoot.startDate) {
                    calendarRoot.startDate = dateTime;
                    calendarRoot.stopDate = !calendarRoot.rangeDate ? dateTime : undefined;
                    calendarRoot.getSelectedDate([cellFormatted, "start"]);
                }
            }

            calendarRoot.currentMonth = date.getMonth();
            calendarRoot.fullMonth = date.toLocaleString(calendarRoot.currentLocale, 'MMMM').split(" ").slice(-1)[0];
            calendarRoot.currentYear = date.getFullYear();
        }
    }
}
