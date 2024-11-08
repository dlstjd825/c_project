#include "user.h"

__declspec(dllexport) int login(const char* ID, const char* PW) {
    User users[MAX_USERS];
    int num_users = load_users(users, MAX_USERS);

    // User 배열을 ID 기준으로 정렬
    qsort(users, num_users, sizeof(User), compare_users);

    // 이진 탐색으로 ID 찾기
    int index = binary_search(users, 0, num_users - 1, ID);

    if (index != -1 && strcmp(users[index].pw, PW) == 0) {
        // 사용자의 상태 확인
        if (strcmp(users[index].status, "approved") == 0) {
            return strcmp(ID, "admin") == 0 ? 2 : 1;  // 로그인 성공 (관리자 또는 일반 사용자)
        }
        else if (strcmp(users[index].status, "pending") == 0) {
            return -1;  // 승인 대기 중인 사용자
        }
        else if (strcmp(users[index].status, "rejected") == 0) {
            return -2;  // 거절된 사용자
        }
    }

    return 0;  // 로그인 실패
}