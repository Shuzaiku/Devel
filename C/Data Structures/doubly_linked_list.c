// Doubly-Linked Lists as taught by Harvard's 2023 CS50x

#include <stdio.h>
#include <stdlib.h>

typedef struct dllist
{
    int value;
    struct dllist *next = NULL;
    struct dllist *prev = NULL;
} dllnode;

dllnode *create(int value);
bool find(dllnode *node, int value);
dllnode *insert(dllnode *head, int value);
void destroy_node(dllnode *node, int value);
void destroy_list(dllnode *node);
dllnode *insert_array(dllnode *head, int size, int arr[size]);
void print_list(dllnode *node);

dllnode *create(int value)
{
    dllnode *head = (dllnode *) malloc(sizeof(dllnode));
    head->value = value;
    return head;
}

bool find(dllnode *node, int value)
{
    // Base case
    if (!node)
        return false;
    if (node->value == value)
        return true;
    // Recursion
    return find(node->next, value);
}

dllnode *insert(dllnode *head, int value)
{
    dllnode *new_head = create(value);
    new_head->next = head;
    head->prev = new_head;
    return new_head;
}

void destroy_node(dllnode *node, int value)
{
    // Base case
    if (!node)
        return;
    if (node->value == value)
    {
        dllnode *next = node->next;
        dllnode *prev = node->prev;
        next->prev = prev;
        prev->next = next;
        free(node);
    }
    // Recursion
    destroy_node(node->next, value);
}

void destroy_list(dllnode *node)
{
    // Base case
    if (!node)
        return;
    // Recursion
    destroy_list(node->next);
    free(node);
}

dllnode *insert_array(dllnode *head, int size, int arr[size])
{
    dllnode *new_head = head;
    for (int i = 0; i < size; i++)
    {
        new_head = insert(new_head, arr[i]);
    }
    return new_head;
}

void print_list(dllnode *node)
{
    // Base case
    if (!node)
    {
        printf("\n");
        return;
    }
    // Recursion
    printf("%d\t", node->value);
    print_list(node->next);
}

int main() {
    dllnode *list = create(6);
    int size = 5;
    int arr[5] = {5, 4, 3, 2, 1};
    list = insert_array(list, size, arr);
    print_list(list);
    destroy_node(list, 3);
    print_list(list);
    printf("Is 2 on the list? %s\n", find(list, 2)? "Yes" : "No");
    destroy_list(list);
    
    return 0;
}
