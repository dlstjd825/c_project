#ifndef USER_H
#define USER_H

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_LINE_LENGTH 1024
#define MAX_USERS 2048

typedef struct {
    char id[20];
    char pw[10];
    char status[10];
    char role[10];
    char name[30];
    char birthday[10];
    char gender[2];
} User;

int binary_search(User* users, int left, int right, const char* id);
int load_users(User* users, int max_users);
void trim_newline(char* str);
int compare_users(const void* a, const void* b);

#endif