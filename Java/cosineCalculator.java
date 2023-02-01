// Cosine law calculator
import java.lang.Math;

public class Main {
	public static void main(String[] args) {
		Input input = new Input();

		while (true) {
			char userResponse = input.getChar("What do you want to find?\n a) Missing side\tb) Missing angle\t c) Exit program\n");
			System.out.println("\033[H\033[2J");
			if (userResponse != 'a' && userResponse != 'b' && userResponse != 'c') {
				System.out.println("Invalid input!");
				continue;

			} else if (userResponse == 'a') {
				double side1 = input.getDouble("What's the value of side 1?\n");
				double side2 = input.getDouble("What's the value of side 2?\n");
				float theta = input.getFloat("What is the value of theta in degrees?\n");
				System.out.printf("The value of the missing side is %.1f.\n", getMissingSide(side1, side2, theta));

			} else if (userResponse == 'b') {
				double[] sides = new double[3];
				for (byte i = 0; i < sides.length; i++) {
					sides[i] = input.getDouble("What's the value of side " + (i + 1) + "?\n");
				}

				byte min = 1;
				byte max = 3;
				byte angleIdx;
				while (true) {
					angleIdx = input.getByte(String.format("What's the index of theta? (Min %d | Max %d)\n", min, max));
					if (angleIdx < min) {
						System.out.printf("Input cannot be smaller than %d!\n", min);
					} else if (angleIdx > max) {
						System.out.printf("Input cannot be bigger than %d!\n", max);
					} else {
						break;
					}
				}
				System.out.printf("The value of the missing angle is %.1f degrees.\n", getMissingAngle(sides, (byte) (angleIdx-1)));

			} else if (userResponse == 'c') {
				break;
			}
			System.out.println('\n');
		}
	}

	private static double getMissingSide(double side1, double side2, float theta) {
		double pow1 = Math.pow(side1, 2);
		double pow2 = Math.pow(side2, 2);
		double cosine = Math.cos(Math.toRadians(theta));
		return pow1 + pow2 - 2 * side1 * side2 * cosine;
	}

	private static double getMissingAngle(double[] sides, byte angleIdx) {
		//angleIdx ranges 0 - 2
		double angle = 0;
		double dividend = -2;

		for (byte sideIdx = 0; sideIdx < sides.length; sideIdx++) {
			double side = sides[sideIdx];
			side = Math.pow(side, 2);
			if (sideIdx != angleIdx) {
				side = -side;
				dividend *= side;
			}
			angle += side;
		}
		angle /= dividend;
		return Math.toDegrees(Math.acos(Math.toRadians(angle)));
	}
}
