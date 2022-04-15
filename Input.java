// Emilio Osorio
// Input class for easy, simplified input with python-inspired behaviour

// Imports
import java.io.BufferedReader;
import java.io.InputStreamReader;

// Base class
class Input {
  private static BufferedReader inputGetter = new BufferedReader(new InputStreamReader(System.in));
  public String charError = "Input was empty.";
  public String byteError = "Input must be a byte.";
  public String shortError = "Input must be a short.";
  public String intError = "Input must be an integer.";
  public String longError = "Input must be a long.";
  public String floatError = "Input must be a float.";
  public String doubleError = "Input must be a double.";

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
    printPrompt(prompt);

    while (true) {
      try {
        return getUnfilteredInput().charAt(0);
      } catch (Exception e) {
        System.out.println(this.charError);
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
    printPrompt(prompt);
    
    while (true) {
      try {
        return Byte.parseByte(getUnfilteredInput());
      } catch (Exception e) {
        System.out.println(this.byteError);
      }
    }
  }

  // Get short input
  public short getShort(String... prompt) {
    printPrompt(prompt);
    
    while (true) {
      try {
        return Short.parseShort(getUnfilteredInput());
      } catch (Exception e) {
        System.out.println(this.shortError);
      }
    }
  }

  // Get integer input
  public int getInt(String... prompt) {
    printPrompt(prompt);
    
    while (true) {
      try {
        return Integer.parseInt(getUnfilteredInput());
      } catch (Exception e) {
        System.out.println(this.intError);
      }
    }
  }

  // Get long input
  public long getLong(String... prompt) {
    printPrompt(prompt);
    
    while (true) {
      try {
        return Long.parseLong(getUnfilteredInput());
      } catch (Exception e) {
        System.out.println(this.longError);
      }
    }
  }

  // Get float input
  public float getFloat(String... prompt) {
    printPrompt(prompt);

    while (true) {
      try {
        return Float.parseFloat(getUnfilteredInput());
      } catch (Exception e) {
        System.out.println(this.floatError);
      }
    }
  }

  // Get double input
  public double getDouble(String... prompt) {
    printPrompt(prompt);

    while (true) {
      try {
        return Double.parseDouble(getUnfilteredInput());
      } catch (Exception e) {
        System.out.println(this.doubleError);
      }
    }
  }
}