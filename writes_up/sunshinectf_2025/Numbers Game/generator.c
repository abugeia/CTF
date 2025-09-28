#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <timestamp>\n", argv[0]);
        return 1;
    }

    long long timestamp = atoll(argv[1]);
    srand(timestamp);

    long long rand1 = rand();
    long long rand2 = rand();
    long long rand3 = rand();

    long long number_to_guess = (rand3 << 62) | (rand2 << 31) | rand1;

    printf("%lld\n", number_to_guess);

    return 0;
}