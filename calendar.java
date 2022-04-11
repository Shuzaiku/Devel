// Group Members
// 1. [Ritvik Uppal]
// 2. [Emilio Osorio]

// Description: This program will show a calendar

// # Imports
import java.lang.Math;

// # Main class
class Main {
  private static Input input = new Input();
  public static void main(String[] args) {
    // level3();
		level4();
  }

  // # Calendar printing function for both levels
  private static void printCalendar(byte monthDays, byte firstIndex) {
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
    };
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
      
      if (i < rows-1) {
        System.out.println();
      }
    }
  }

  // # Level 3
  private static void level3() {
    // Declare weekdays
    String[] weekDays = {
      "sunday",
      "monday",
      "tuesday",
      "wednesday",
      "thursday",
      "friday",
      "saturday"
    };
    
    // Get days of month
    input.byteError = "Invalid entry, must be values 28 thru 31. Try again...";
    byte monthDays;
    
  	while (true) {
      monthDays = input.getByte("How many days in a month?\n");
      if (monthDays >= 28 && monthDays <= 31) {
         break;
      } else {
        System.out.println(input.byteError);
      }
    }

    // Get start of month
    String firstDay;
    byte firstIndex;
    while (true) {
      firstDay = input.getStr("On which day does the month start?\n").toLowerCase();
      boolean dayFound = false;

      for (firstIndex = 0; firstIndex < weekDays.length; firstIndex++) {
        if (firstDay.equals(weekDays[firstIndex])) {
          dayFound = true;
          break;
        }
      }

      if (dayFound) {
        break;
      } else {
        System.out.println("Invalid day of the week, Must be Sunday thru Saturday. Try again...");
      }
    }

    // Calendar
    printCalendar(monthDays, firstIndex);
  }

  // # Level 4
  private static void level4() {
    // Declare months
    String[] months = {
      "january", "february", "march",
      "april", "may", "june", "july",
      "august", "september", "october",
      "november", "december"
    };
    
  	// Get month
    String monthChoice;
    byte monthIndex = 0;
    while (true) {
      monthChoice = input.getStr("What is the month?\n").toLowerCase();

      // Attempt to get month by index
      boolean canIndex = false;
      try {
        monthIndex = Byte.parseByte(monthChoice);
        if (monthIndex > 0 && monthIndex <= 12) {
          canIndex = true;
          monthIndex--;
        }
      } catch (Exception e) {}

      boolean monthFound = false;
      if (canIndex) {
        monthFound = true;
        monthChoice = months[monthIndex];
      } else { // Get month by string name
        for (monthIndex = 0; monthIndex < months.length; monthIndex++) {
          if (monthChoice.equals(months[monthIndex])) {
            monthFound = true;
            break;
          }
        }
      }

      if (monthFound) {
        break;
      } else {
        System.out.println("Invalid entry. Must be a month of the year.");
      }
    }
    System.out.println();

    // Get year
    long year;
    input.longError = "Invalid year. Must be a positive integer. Try again...";
    while (true) {
      year = input.getLong("What is the year?\n");

      if (year < 1) {
        System.out.println(input.longError);
      } else {
        break;
      }
    }

    // Calendar formula
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

    // Days in months
    byte febLen = 28;
    if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) {
      febLen++;
    }
    
    byte[] monthLens = {
      31, febLen, 31, 30,
      31, 30, 31, 31,
      30, 31, 30, 31
    };

    short daysPassed = 0;
    byte monthDays = 0;
    for (byte i = 0; i < monthIndex; i++) {
      byte currVal = monthLens[i];
      daysPassed += currVal;
      if (i+1 == monthIndex) {
        monthDays = currVal;
      }
    }

    if (monthDays == 0) {
      monthDays = 31;
    }
    // firstIndex = (byte) ((firstIndex + daysPassed) % 7); work on this later
    
    // Calendar
    // printCalendar(monthDays, firstIndex);
  }
}
