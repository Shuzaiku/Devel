//Group Members
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
    byte monthIndex;
    while (true) {
      monthChoice = input.getStr("What is the month?\n").toLowerCase();
      boolean monthFound = false;

      for (monthIndex = 0; monthIndex < months.length; monthIndex++) {
        if (monthChoice.equals(months[monthIndex])) {
          monthFound = true;
          break;
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
    long century = year / 100;
    System.out.println("Cent: " + century);
    byte firstIndex = (byte) ((
      1 + (short) (2.6 * (monthIndex + 1) - 0.2)
      - 2 * century + year + year / 4 + century / 4
    ) % 7);
    System.out.println("Index: " + firstIndex);

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

    byte monthDays = 0;
    for (byte i = 0; i < monthIndex; i++) {
      byte currVal = monthLens[i];
      if (i+1 == monthIndex) {
        System.out.println(true + "burhh");
        monthDays = currVal;
      }
    }

    if (monthDays == 0) {
      monthDays = 31;
    }
    
    // Calendar
    printCalendar(monthDays, firstIndex);
  }
}
