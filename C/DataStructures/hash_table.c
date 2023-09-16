// Hash Tables as taught by Harvard's 2023 CS50x, using chaining

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define HASH_MAX 10

typedef struct dllist
{
    int value;
    struct dllist *next;
    struct dllist *prev;
} dllnode;

// Doubly-Linked List methods declaration
dllnode *dllcreate(int value);
bool dllfind(dllnode *node, int value);
dllnode *dllinsert(dllnode *head, int value);
void dlldestroy_node(dllnode *node, int value);
void dllfree(dllnode *node);
dllnode *dllinsert_array(dllnode *head, int size, int arr[size]);
void dllprint(dllnode *node);
// Hash Table methods declaration
dllnode **create_hashtable();
unsigned int hash(int value);
void table_insert(dllnode **hashtable, int value);
void table_remove(dllnode **hashtable, int value);
void free_table(dllnode **hashtable);
void print_table(dllnode **hashtable);
void table_insert_array(dllnode **hashtable, int size, int arr[size]);
bool table_find(dllnode **hashtable, int value);

// Doubly-Linked List methods definition
dllnode *dllcreate(int value)
{
    dllnode *head = (dllnode *) malloc(sizeof(dllnode));
    head->value = value;
    head->next = NULL;
    head->prev = NULL;
    return head;
}

bool dllfind(dllnode *node, int value)
{
    // Base case
    if (node == NULL)
        return false;
    if (node->value == value)
        return true;
    // Recursion
    return dllfind(node->next, value);
}

dllnode *dllinsert(dllnode *head, int value)
{
    dllnode *new_head = dllcreate(value);
    new_head->next = head;
    head->prev = new_head;
    return new_head;
}

void dlldestroy_node(dllnode *node, int value)
{
    // Base case
    if (node == NULL)
        return;
    if (node->value == value)
    {
        dllnode *next = node->next;
        dllnode *prev = node->prev;
        next->prev = prev;
        prev->next = next;
        free(node);
        node = NULL;
        return;
    }
    // Recursion
    dlldestroy_node(node->next, value);
}

void dllfree(dllnode *node)
{
    // Base case
    if (node == NULL)
        return;
    // Recursion
    dllfree(node->next);
    free(node);
    node = NULL;
}

dllnode *dllinsert_array(dllnode *head, int size, int arr[size])
{
    dllnode *new_head = head;
    for (int i = 0; i < size; i++)
    {
        new_head = dllinsert(new_head, arr[i]);
    }
    return new_head;
}

void dllprint(dllnode *node)
{
    // Base case
    if (!node)
    {
        printf("\n");
        return;
    }
    // Recursion
    printf("%d\t", node->value);
    dllprint(node->next);
}

// Hash Table methods definition
dllnode **create_hashtable()
{
    dllnode **hashtable = (dllnode **) malloc(HASH_MAX * sizeof(dllnode *));
    for (int i = 0; i < HASH_MAX; i++)
    {
        hashtable[i] = NULL;
    }
    return hashtable;
}

unsigned int hash(int value)
{
    return value % HASH_MAX;
}

void table_insert(dllnode **hashtable, int value)
{
    unsigned int key = hash(value);
    if (hashtable[key] == NULL)
    {
        hashtable[key] = dllcreate(value);
    }
    else
    {
        hashtable[key] = dllinsert(hashtable[key], value);
    }
}

void table_remove(dllnode **hashtable, int value)
{
    unsigned int key = hash(value);
    dlldestroy_node(hashtable[key], value);
}

void free_table(dllnode **hashtable)
{
    for (int i = 0; i < HASH_MAX; i++)
    {
        dllfree(hashtable[i]);
    }
    free(hashtable);
    hashtable = NULL;
}

void print_table(dllnode **hashtable)
{
    for (int i = 0; i < HASH_MAX; i++)
    {
        dllprint(hashtable[i]);
    }
}

void table_insert_array(dllnode **hashtable, int size, int arr[size])
{
    for (int i = 0; i < size; i++)
    {
        table_insert(hashtable, arr[i]);
        // printf("Finished %dth insert\n", i + 1);
    }
}

bool table_find(dllnode **hashtable, int value)
{
    unsigned int key = hash(value);
    return dllfind(hashtable[key], value);
}

int main() {
    dllnode **hashtable = create_hashtable();
    int size = 20;
    int arr[20] = {2, 76, 68, 52, 142, 136, 101, 117, 29, 135, 179, 24, 67, 114, 198, 39, 159, 36, 153, 51};
    int fifth = arr[5];
    printf("Fifth element in array: %d\n", fifth);
    table_insert_array(hashtable, size, arr);
    printf("Finished table insertion\n");
    printf("%d in table? %s\n", fifth, table_find(hashtable, fifth)? "Yes" : "No");
    table_remove(hashtable, fifth);
    printf("%d in table? %s\n", fifth, table_find(hashtable, fifth)? "Yes" : "No");
    print_table(hashtable);
    free_table(hashtable);
    hashtable = NULL;
    
    return 0;
}