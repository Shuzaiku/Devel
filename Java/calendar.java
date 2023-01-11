// Calendar class
// Emilio Osorio
// 2022-04-10
// This class will give many calendar functionalities, including Conway's doomsday algorithm
// Doomsday methods will only work properly using the Gregorian calendar

// # Imports
import java.lang.Math;

// # Class
public class Calendar {
    // # Init
    public long year;

    Calendar(long year) {
        this.year = year;
    }

    // # Doomsday algorithm
    public byte getWeekdayIndex(byte monthIndex) {
        byte febLen = getFebLen();
        byte janDay = (byte) (3 + (febLen - 28));
        byte[] doomsdaysSet = { janDay, febLen, 7, 4, 9, 6, 11, 8, 5, 10, 7, 12 };

        // Get the weekday
        byte weekdayIndex = getCenturyDoomsday();

        for (byte i = doomsdaysSet[monthIndex]; i > 1; i--) {
            weekdayIndex--;
            if (weekdayIndex == -1) {
                weekdayIndex = 6;
            }
        }
        return weekdayIndex;
    }

    private byte getCenturyDoomsday() {
        long year = this.year;
        long firstDigits = year / 100;
        long lastDigits = year % 100;
        long fitTimes = lastDigits / 12;
        byte fitRemainder = (byte) (lastDigits % 12);
        byte remainderDiv = (byte) (fitRemainder / 4);

        byte anchor;
        if (firstDigits % 2 == 0) { // Even year
            if (firstDigits % 4 == 0) {
                anchor = 2;
            } else {
                anchor = 5;
            }
        } else { // Odd year
            if (firstDigits % 4 == 1) {
                anchor = 0;
            } else {
                anchor = 3;
            }
        }

        long add = fitTimes + fitRemainder + remainderDiv + anchor;
        byte doomsday = (byte) (add % 7);
        return doomsday;
    }

    // # Basic calendar
    private static String[] months = {
            "january", "february", "march",
            "april", "may", "june", "july",
            "august", "september", "october",
            "november", "december"
    };

    public String getMonth(byte index) {
        return months[index];
    }

    public byte getMonthIndex(String monthName) { // Will return -1 if not found
        byte monthIndex;
        boolean monthFound = false;
        for (monthIndex = 0; monthIndex < months.length; monthIndex++) {
            if (monthName.equals(months[monthIndex])) {
                monthFound = true;
                break;
            }
        }

        if (!monthFound) {
            return -1;
        } else {
            return monthIndex;
        }
    }

    public void printCalendar(byte monthDays, byte firstIndex) {
        byte rows = (byte) Math.ceil((monthDays + firstIndex) / 7.0);
        String[] shortWords = {
                "Sun", "Mon", "Tues",
                "Wed", "Thurs", "Fri",
                "Sat"
        };
        System.out.println();

        // Print day names
        for (byte i = 0; i < shortWords.length; i++) {
            System.out.print(shortWords[i] + "\t");
        }
        ;
        System.out.println();

        // Print day numbers
        byte currDay = 1;
        for (byte i = 0; i < rows; i++) {
            for (byte j = 0; j < 7; j++) {
                Object message = currDay;
                if (firstIndex > j && i == 0) {
                    message = "";
                } else if (currDay > monthDays) {
                    break;
                } else {
                    currDay++;
                }
                System.out.print(message + "\t");
            }

            if (i < rows - 1) {
                System.out.println();
            }
        }
    }

    public byte[] getDaysLen() {
        byte febLen = getFebLen();
        byte[] daysLen = {
                31, febLen, 31, 30,
                31, 30, 31, 31,
                30, 31, 30, 31
        };
        return daysLen;
    }

    private byte getFebLen() {
        long year = this.year;
        byte febLen = 28;
        if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) {
            febLen++;
        }
        return febLen;
    }
}
