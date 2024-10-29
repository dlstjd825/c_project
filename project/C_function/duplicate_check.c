#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#define MAX_LINE_LENGTH 1024

__declspec(dllexport) bool duplicate_check(const char* id) {
    FILE* file = fopen("static/user.csv", "r");
    if (file == NULL) {
        printf("파일을 열 수 없습니다.\n");
        return false;
    }

    char line[MAX_LINE_LENGTH];
    char existing_id[50];
    bool is_duplicate = false;  

    // CSV 파일에서 ID 확인
    while (fgets(line, sizeof(line), file)) {
        sscanf(line, "%49[^,]", existing_id);  // CSV 파일에서 첫 번째 값(ID)을 읽음
        if (strcmp(existing_id, id) == 0) {    // ID가 일치하는지 확인
            is_duplicate = true;
            break;
        }
    }

    fclose(file);
    return is_duplicate;
}
