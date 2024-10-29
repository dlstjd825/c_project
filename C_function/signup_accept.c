#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#define MAX_LINE_LENGTH 1024

// signup_accept �Լ� ����
__declspec(dllexport) bool signup_accept(const char* ID) {
    char txt_filename[MAX_LINE_LENGTH];
    snprintf(txt_filename, sizeof(txt_filename), "static/users/%s_info.txt", ID);

    // txt ���� ����
    FILE* txt_file = fopen(txt_filename, "r");
    if (txt_file == NULL) {
        perror("Failed to open user info file");
        return false;
    }

    // user.csv ������ �߰� ���� ����
    FILE* csv_file = fopen("static/user.csv", "a");
    if (csv_file == NULL) {
        perror("Failed to open CSV file");
        fclose(txt_file);
        return false;
    }

    // txt ���Ͽ��� �����͸� �а�, csv �������� ��ȯ �� CSV ���Ͽ� ����
    char line[MAX_LINE_LENGTH];
    char id[50], pw[50], name[50], birthday[50], role[10], gender[2];

    while (fgets(line, sizeof(line), txt_file)) {
        if (sscanf(line, "ID: %49[^\n]", id) == 1) continue;
        if (sscanf(line, "PW: %49[^\n]", pw) == 1) continue;
        if (sscanf(line, "Role: %9[^\n]", role) == 1) continue;
        if (sscanf(line, "Name: %49[^\n]", name) == 1) continue;
        if (sscanf(line, "Birthday: %49[^\n]", birthday) == 1) continue;
        if (sscanf(line, "Gender: %9[^\n]", gender) == 1) continue;
    }

    // CSV ���Ͽ� �߰�
    fprintf(csv_file, "%s,%s,%s,%s,%s,%s\n", id, pw, role, name, birthday, gender);

    // ���� �ݱ�
    fclose(txt_file);
    fclose(csv_file);
    return true;
}
