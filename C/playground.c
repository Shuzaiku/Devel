#include <stdio.h>
#include <stdlib.h>

void free_arr(int **arr)
{
    free(*arr);
    *arr = NULL;
}

int main()
{
    int size = 10;
    int *arr = (int *) malloc(size * sizeof(int));
    for (int i = 0; i < size; i++)
    {
        arr[i] = i + 1;
    }

    for (int i = 0; i < size; i++)
    {
        printf("%d\n", arr[i]);
    }

    // free(arr);
    // arr = NULL;
    free_arr(&arr);
    return 0;
}