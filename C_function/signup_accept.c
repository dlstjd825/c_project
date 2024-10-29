#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#define MAX_LINE_LENGTH 1024

// signup_accept 함수 정의
__declspec(dllexport) bool signup_accept(const char* ID) {
    char txt_filename[MAX_LINE_LENGTH];
    snprintf(txt_filename, sizeof(txt_filename), "static/users/%s_info.txt", ID);

    // txt 파일 열기
    FILE* txt_file = fopen(txt_filename, "r");
    if (txt_file == NULL) {
        perror("Failed to open user info file");
        return false;
    }

    // user.csv 파일을 추가 모드로 열기
    FILE* csv_file = fopen("static/user.csv", "a");
    if (csv_file == NULL) {
        perror("Failed to open CSV file");
        fclose(txt_file);
        return false;
    }

    // txt 파일에서 데이터를 읽고, csv 형식으로 변환 후 CSV 파일에 쓰기
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

    // CSV 파일에 추가
    fprintf(csv_file, "%s,%s,%s,%s,%s,%s\n", id, pw, role, name, birthday, gender);

    // 파일 닫기
    fclose(txt_file);
    fclose(csv_file);
    return true;
}
