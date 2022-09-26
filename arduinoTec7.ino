// # Startup
int forwardLeftMotor = 13;
int backwardLeftMotor = 12;
int backwardRightMotor = 11;
int forwardRightMotor = 10;

int sensorSignal = 3;
bool isManualMode = true;
char state;

int timeInSeconds(int milliseconds) {
  int seconds = milliseconds * 1000;
  return seconds;
}

// # Setup
void setup() {
  Serial.begin(9600);

  pinMode(forwardLeftMotor, OUTPUT);
  pinMode(backwardLeftMotor, OUTPUT);
  pinMode(forwardRightMotor, OUTPUT);
  pinMode(backwardRightMotor, OUTPUT);
  pinMode(sensorSignal, INPUT);
}

// # Motor functionality
void overrideMotor(int motor, int digitalState) {
  if (digitalRead(motor) != digitalState) {
    digitalWrite(motor, digitalState);
  }
}

void performMovement(int movement[4]) {
  int currentMotor = forwardLeftMotor;
  for (int digitalState = 0; digitalState <= 3; digitalState++) {
    overrideMotor(currentMotor, movement[digitalState]);
    currentMotor -= 1;
  }
}

int movements[5][4] = {
  // forward
  {
    HIGH,
    LOW,
    LOW,
    HIGH 
  },

  // backward
  {
    LOW,
    HIGH,
    HIGH,
    LOW
  },

  // leftward
  {
    LOW,
    LOW,
    LOW,
    HIGH
  },

  // rightward
  {
    HIGH,
    LOW,
    LOW,
    LOW
  },

  // stop
  {
    LOW,
    LOW,
    LOW,
    LOW
  }
};

// # Stored movements
int forward = 0;
int backward = 1;
int leftward = 2;
int rightward = 3;
int stopMovement = 4;

// # Loop
void loop() {
  if (Serial.available() > 0) { // if there is a bluetooth signal...
    state = Serial.read(); // receive bluetooth message
  }

  switch (state) {
  // -- Control -- //
  case 'F': // forward
    performMovement(movements[forward]);
    break;
  
  case 'B': // backward
    performMovement(movements[backward]);
    break;

  case 'R': // rightward
    performMovement(movements[rightward]);
    break;

  case 'L': // leftward
    performMovement(movements[leftward]);
    break;

  case 'S': // stop
    performMovement(movements[stopMovement]);
    break;

  // -- Driving modes -- //
  case 'A': // turn on automatic mode
    isManualMode = false;
    break;

  case 'M': // manual mode
    performMovement(movements[stopMovement]);
    isManualMode = true;
    break;
  }

  if (isManualMode == false) { // automatic mode functionality
    if (digitalRead(sensorSignal) == HIGH) { // drive normally
        performMovement(movements[forward]);
    }
    else { // perform obstacle avoid maneuver
      performMovement(movements[stopMovement]);
      delay(timeInSeconds(1));
      performMovement(movements[backward]);
      delay(timeInSeconds(1));

      overrideMotor(forwardRightMotor, HIGH);
      overrideMotor(backwardRightMotor, LOW);
      delay(timeInSeconds(1));

      overrideMotor(backwardLeftMotor, LOW);
      overrideMotor(forwardLeftMotor, HIGH);
    }
  }

  delay(10); // for better performance
}
