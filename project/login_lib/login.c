#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_LINE_LENGTH 1024

// 문자열 끝의 개행 문자 제거 함수
void trim_newline(char* str) {
    str[strcspn(str, "\n")] = '\0';
}

__declspec(dllexport) bool login(const char* ID, const char* PW) {
    FILE* file = fopen("static/user.csv", "r");
    if (file == NULL) {
        perror("Failed to open file");  // 파일을 열지 못할 때 오류 메시지 출력
        return false;
    }

    char line[MAX_LINE_LENGTH];
    char csvID[50] = { 0 };
    char csvPW[50] = { 0 };
    char csvName[50] = { 0 };  // 추가된 필드
    char csvGender[10] = { 0 }; // 추가된 필드

    // 파일의 각 줄을 읽음
    while (fgets(line, sizeof(line), file)) {
        // 각 줄에서 ID, PW, 이름, 성별을 추출
        if (sscanf(line, "%49[^,],%49[^,],%49[^,],%9[^\n]", csvID, csvPW, csvName, csvGender) == 4) {
            // 개행 문자 제거
            trim_newline(csvID);
            trim_newline(csvPW);

            // ID와 PW가 일치하는지 확인
            if (strcmp(ID, csvID) == 0 && strcmp(PW, csvPW) == 0) {
                fclose(file);
                return true;  // 로그인 성공
            }
        }
    }

    fclose(file);  // 파일 닫기
    return false;  // 로그인 실패
}
