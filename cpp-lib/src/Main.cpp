# include <stdio.h>

/**
 * add 2 numbers
 * @param leftHand first
 * @param rightHand second
 */
extern "C" __attribute__((visibility("default"))) int add(int leftHand, int rightHand) {
  return leftHand + rightHand;
}

/**
 * subtract 2 numbers
 * @param leftHand first
 * @param rightHand second
 */
extern "C" __attribute__((visibility("default"))) void sub(int leftHand, int rightHand) {
  printf("%d\n", leftHand - rightHand);
}
