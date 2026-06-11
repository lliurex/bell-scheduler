import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Styles

Rectangle {
    width: 325
    height: 250

    property alias calendarLocale: calendar.calendarLocale
    property alias startDate: calendar.startDate
    property alias stopDate: calendar.stopDate
    property alias initDate: calendar.initDate
    property alias endDate: calendar.endDate
    property alias rangeDate: calendar.rangeDate
    property alias daysInRange: calendar.daysInRange
    property alias selectedDate: calendar.selectedDate

    signal getSelectedDate(var value)

    Calendar {
        id: calendar
        width: parent.width
        Layout.preferredHeight:200
        Layout.fillHeight:false
        anchors.centerIn: parent
        frameVisible: true
        weekNumbersVisible: false
        focus: true

        property var calendarLocale: "es_ES"
        property var startDate: undefined
        property var stopDate: undefined
        property string initDate: ""
        property string endDate: ""
        property var daysInRange: []
        property bool rangeDate: true

        selectedDate: new Date()
        locale: Qt.locale(calendar.calendarLocale)

        style: CalendarStyle {
            dayDelegate: Item {
                id: dayDelegateRoot
                readonly property color sameMonthDateTextColor: "#444"
                readonly property color selectedDateColor: "#3778d0"
                readonly property color selectedDateTextColor: "white"
                readonly property color differentMonthDateTextColor: "#bbb"
                readonly property color invalidDatecolor: "#dddddd"

                readonly property string formattedCellDate: Qt.formatDate(styleData.date, "dd/MM/yyyy")
                readonly property var dateOnFocus: styleData.date

                Rectangle {
                    anchors.fill: parent
                    border.color: "transparent"

                    color: {
                        if (calendar.startDate !== undefined || calendar.stopDate !== undefined) {
                            if (dateOnFocus > calendar.startDate && dateOnFocus < calendar.stopDate) {
                                return "#55555555"; // En medio del rango
                            }

                            let cellTime = dateOnFocus.setHours(0,0,0,0);
                            let startTime = calendar.startDate ? calendar.startDate.setHours(0,0,0,0) : -1;
                            let stopTime = calendar.stopDate ? calendar.stopDate.setHours(0,0,0,0) : -1;

                            if (cellTime === startTime || cellTime === stopTime) {
                                return selectedDateColor; // Extremos del rango
                            }
                            return "transparent";
                        }
                        else {
                            if (formattedCellDate === calendar.initDate || formattedCellDate === calendar.endDate) {
                                return selectedDateColor;
                            }
                            if (calendar.daysInRange.includes(formattedCellDate)) {
                                return "#55555555";
                            }
                            return "transparent";
                        }
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    onPressed: (mouse) => {
                        let cleanDate = new Date(styleData.date);
                        cleanDate.setHours(0,0,0,0);

                        if (calendar.startDate === undefined) {
                            calendar.startDate = cleanDate;
                            calendar.stopDate = !calendar.rangeDate ? cleanDate : undefined;
                            getSelectedDate([formattedCellDate, "start"]);
                        }
                        else if (calendar.stopDate === undefined) {
                            calendar.stopDate = cleanDate;
                            getSelectedDate([formattedCellDate, "end"]);
                        }
                        else {
                            if (calendar.rangeDate) {
                                calendar.startDate = cleanDate;
                                calendar.stopDate = undefined;
                                getSelectedDate([formattedCellDate, "start"]);
                            } else {
                                calendar.startDate = undefined;
                                calendar.stopDate = cleanDate;
                                getSelectedDate([formattedCellDate, "end"]);
                            }
                        }

                        if (calendar.stopDate <= calendar.startDate) {
                            calendar.startDate = cleanDate;
                            calendar.stopDate = !calendar.rangeDate ? cleanDate : undefined;
                            getSelectedDate([formattedCellDate, "start"]);
                        }

                        mouse.accepted = false; 
                    }
                }

                Label {
                    id: dayDelegateText
                    text: styleData.date.getDate()
                    anchors.centerIn: parent
                    color: {
                        if (styleData.valid) {
                            if (styleData.selected) return selectedDateTextColor;
                            return styleData.visibleMonth ? sameMonthDateTextColor : differentMonthDateTextColor;
                        }
                        return invalidDatecolor;
                    }
                }
            }
        }
    }
}
