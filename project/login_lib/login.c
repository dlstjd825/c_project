#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LINE_LENGTH 1024

// ���ڿ� ���� ���� ���� ���� �Լ�
void trim_newline(char* str) {
    str[strcspn(str, "\n")] = '\0';
}

__declspec(dllexport) bool login(const char* ID, const char* PW) {
    FILE* file = fopen("static/user.csv", "r");
    if (file == NULL) {
        perror("Failed to open file");  // ������ ���� ���� �� ���� �޽��� ���
        return false;
    }

    char line[MAX_LINE_LENGTH];
    char csvID[50] = { 0 };
    char csvPW[50] = { 0 };
    char csvName[50] = { 0 };  // �߰��� �ʵ�
    char csvGender[10] = { 0 }; // �߰��� �ʵ�

    // ������ �� ���� ����
    while (fgets(line, sizeof(line), file)) {
        // �� �ٿ��� ID, PW, �̸�, ������ ����
        if (sscanf(line, "%49[^,],%49[^,],%49[^,],%9[^\n]", csvID, csvPW, csvName, csvGender) == 4) {
            // ���� ���� ����
            trim_newline(csvID);
            trim_newline(csvPW);

            // ID�� PW�� ��ġ�ϴ��� Ȯ��
            if (strcmp(ID, csvID) == 0 && strcmp(PW, csvPW) == 0) {
                fclose(file);
                return true;  // �α��� ����
            }
        }
    }

    fclose(file);  // ���� �ݱ�
    return false;  // �α��� ����
}
