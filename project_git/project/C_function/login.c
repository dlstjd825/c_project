#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LINE_LENGTH 1024

// ���ڿ� ���� ���� ���� ���� �Լ�
void trim_newline(char* str) {
    str[strcspn(str, "\n")] = '\0';
}

__declspec(dllexport) int login(const char* ID, const char* PW) {
    FILE* file = fopen("static/user.csv", "r");
    if (file == NULL) {
        perror("Failed to open file");  // ������ ���� ���� �� ���� �޽��� ���
        return 0;
    }

    // ��, ���̵�, ����� ���� ���� ����
    char line[MAX_LINE_LENGTH];
    char csvID[50] = { 0 };
    char csvPW[50] = { 0 };

    // ������ �� ���� ����
    while (fgets(line, sizeof(line), file)) {
        // �� �ٿ��� ID, PW, Role�� ����
        if (sscanf(line, "%49[^,],%49[^,\n]", csvID, csvPW) == 2) {
            // ���� ���� ����
            trim_newline(csvID);
            trim_newline(csvPW);

            // ID�� PW�� ��ġ�ϴ��� Ȯ��
            if (strcmp(ID, csvID) == 0 && strcmp(PW, csvPW) == 0) {
                if (strcmp(ID, "admin") == 0)  return 2;    // ������ �α��� ����
                else return 1;      // �Ϲ� ����� �α��� ����
                fclose(file);
            }
        }
    }

    fclose(file);  // ���� �ݱ�
    return 0;  // �α��� ����
}
