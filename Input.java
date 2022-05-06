// Emilio Osorio
// Input class for easy, simplified input with python-inspired behaviour

// Imports
import java.io.BufferedReader;
import java.io.InputStreamReader;

// Base class
class Input {
  private static BufferedReader inputGetter = new BufferedReader(new InputStreamReader(System.in));
  public String charExceptionMsg = "Input was empty.";
  public String byteExceptionMsg = "Input must be a byte.";
  public String shortExceptionMsg = "Input must be a short.";
  public String intExceptionMsg = "Input must be an integer.";
  public String longExceptionMsg = "Input must be a long.";
  public String floatExceptionMsg = "Input must be a float.";
  public String doubleExceptionMsg = "Input must be a double.";

  // Main input receiver
  private static String getUnfilteredInput() {
    try {
      return inputGetter.readLine();
    } catch (Exception e) {
      return "";
    }
  }

  // Prompt
  private static void printPrompt(String... prompt) {
    if (prompt.length > 0) { // there is a prompt
      String promptStr = String.valueOf(prompt[0]);
      System.out.print(promptStr);
    }
  }

  // Get character input
  public char getChar(String... prompt) {
    while (true) {
      try {
        printPrompt(prompt);
        return getUnfilteredInput().charAt(0);
      } catch (Exception e) {
        System.out.println(this.charExceptionMsg);
      }
    }
  }
  
  // Get string input
  public String getString(String... prompt) {
    printPrompt(prompt);
    return getUnfilteredInput();
  }
  
  // Get byte input
  public byte getByte(String... prompt) {
    while (true) {
      try {
        printPrompt(prompt);
        return Byte.parseByte(getUnfilteredInput());
      } catch (Exception e) {
        System.out.println(this.byteExceptionMsg);
      }
    }
  }

  // Get short input
  public short getShort(String... prompt) {
    while (true) {
      try {
        printPrompt(prompt);
        return Short.parseShort(getUnfilteredInput());
      } catch (Exception e) {
        System.out.println(this.shortExceptionMsg);
      }
    }
  }

  // Get integer input
  public int getInt(String... prompt) {
    while (true) {
      try {
        printPrompt(prompt);
        return Integer.parseInt(getUnfilteredInput());
      } catch (Exception e) {
        System.out.println(this.intExceptionMsg);
      }
    }
  }

  // Get long input
  public long getLong(String... prompt) {
    while (true) {
      try {
        printPrompt(prompt);    
        return Long.parseLong(getUnfilteredInput());
      } catch (Exception e) {
        System.out.println(this.longExceptionMsg);
      }
    }
  }

  // Get float input
  public float getFloat(String... prompt) {
    while (true) {
      try {
        printPrompt(prompt);    
        return Float.parseFloat(getUnfilteredInput());
      } catch (Exception e) {
        System.out.println(this.floatExceptionMsg);
      }
    }
  }

  // Get double input
  public double getDouble(String... prompt) {
    while (true) {
      try {
        printPrompt(prompt);    
        return Double.parseDouble(getUnfilteredInput());
      } catch (Exception e) {
        System.out.println(this.doubleExceptionMsg);
      }
    }
  }
}
