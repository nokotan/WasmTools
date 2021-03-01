/**
 * add 2 numbers
 * @param leftHand first
 * @param rightHand second
 */
extern "C" __attribute__((used)) int add(int leftHand, int rightHand) {
  return leftHand + rightHand;
}

/**
 * subtract 2 numbers
 * @param leftHand first
 * @param rightHand second
 */
extern "C" __attribute__((used)) int sub(int leftHand, int rightHand) {
  return leftHand - rightHand;
}
