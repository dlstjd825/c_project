#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#define MAX_LINE_LENGTH 1024

__declspec(dllexport) bool duplicate_check(const char* id) {
    FILE* file = fopen("static/user.csv", "r");
    if (file == NULL) {
        printf("������ �� �� �����ϴ�.\n");
        return false;
    }

    char line[MAX_LINE_LENGTH];
    char existing_id[50];
    bool is_duplicate = false;  

    // CSV ���Ͽ��� ID Ȯ��
    while (fgets(line, sizeof(line), file)) {
        sscanf(line, "%49[^,]", existing_id);  // CSV ���Ͽ��� ù ��° ��(ID)�� ����
        if (strcmp(existing_id, id) == 0) {    // ID�� ��ġ�ϴ��� Ȯ��
            is_duplicate = true;
            break;
        }
    }

    fclose(file);
    return is_duplicate;
}
