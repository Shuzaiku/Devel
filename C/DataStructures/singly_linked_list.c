// Singly-Linked List data structure as taught by Harvard's 2023 CS50x,
// only works with int

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct sllist
{
    int value;
    struct sllist *next;
} sllnode;

sllnode* create(int value);
bool find(sllnode *node, int value);
sllnode* insert(sllnode *head, int value);
void destroy(sllnode *node);
sllnode* insert_array(sllnode *head, int size, int array[]);
void print_list(sllnode *node);

// Create: Dynamically allocates space in memory to create an sllnode head
sllnode* create(int value)
{
    sllnode *head = (sllnode *) malloc(sizeof(sllnode));
    head->value = value;
    return head;
}

// Find: Returns true or false if a value can be found in the list
bool find(sllnode *node, int value)
{
    // Base case
    if (!node)
        return false;
    if (node->value == value)
        return true;
    // Recursion
    return find(node->next, value);
}

// Insert: Inserts a new element to the list returning a new head
sllnode* insert(sllnode *head, int value)
{
    sllnode* new_head = create(value);
    new_head->next = head;
    return new_head;
}

// Destroy: Recursively destroys the entire list
void destroy(sllnode *node)
{
    // Base case
    if (!node)
        return;
    // Recursion
    destroy(node->next);
    free(node);
}

// Insert array: performs insert function on every element of array argument
sllnode* insert_array(sllnode *head, int size, int array[])
{
    sllnode *new_head = head;
    for (int i = 0; i < size; i++)
    {
        new_head = insert(new_head, array[i]);
    }
    return new_head;
}

// Print list: prints all the elements in linked list starting from the head
void print_list(sllnode *node)
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
    sllnode *head = create(6);
    int size = 5;
    int array[5] = {5, 4, 3, 2, 1};
    head = insert_array(head, size, array);
    print_list(head);
    printf("Is 7 in the array? %s\n", find(head, 7)? "Yes" : "No");
    destroy(head);
    
    return 0;
}
