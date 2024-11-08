//아이디 중복 체크
#include "user.h"

// 중복 확인 함수
__declspec(dllexport) bool duplicate_check(const char* id) {
    User users[MAX_USERS];
    int num_users = load_users(users, MAX_USERS);

    // 정렬 (필요할 경우)
    qsort(users, num_users, sizeof(User), (int (*)(const void*, const void*)) strcmp);

    // 이진 탐색으로 중복 여부 확인
    return binary_search(users, 0, num_users - 1, id) != -1;
}
