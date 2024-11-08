#define _CRT_SECURE_NO_WARNINGS
#include "user.h"

// reject_user 함수 DLL로 내보내기
__declspec(dllexport) bool signup_reject(const char* ID) {
    User users[MAX_USERS];
    int num_users = load_users(users, MAX_USERS);

    if (num_users == 0) {
        printf("No users loaded.\n");
        return false;
    }

    // 사용자 배열을 ID를 기준으로 정렬
    qsort(users, num_users, sizeof(User), compare_users);

    // 이진 탐색으로 거절할 사용자 찾기
    int index = binary_search(users, 0, num_users - 1, ID);
    if (index == -1) {
        printf("User not found.\n");
        return false;
    }

    // 찾은 사용자의 상태를 "rejected"로 변경
    strcpy(users[index].status, "rejected");

    // 변경된 데이터를 다시 CSV 파일에 저장
    FILE* csv_file = fopen("static/user.csv", "w");
    if (!csv_file) {
        perror("Failed to open CSV file for writing");
        return false;
    }

    for (int i = 0; i < num_users; i++) {
        fprintf(csv_file, "%s,%s,%s,%s,%s,%s,%s\n",
            users[i].id, users[i].pw, users[i].status,
            users[i].role, users[i].name, users[i].birthday, users[i].gender);
    }

    fclose(csv_file);
    return true;
}
