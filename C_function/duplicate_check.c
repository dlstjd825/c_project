//���̵� �ߺ� üũ
#include "user.h"

// �ߺ� Ȯ�� �Լ�
__declspec(dllexport) bool duplicate_check(const char* id) {
    User users[MAX_USERS];
    int num_users = load_users(users, MAX_USERS);

    // ���� (�ʿ��� ���)
    qsort(users, num_users, sizeof(User), (int (*)(const void*, const void*)) strcmp);

    // ���� Ž������ �ߺ� ���� Ȯ��
    return binary_search(users, 0, num_users - 1, id) != -1;
}
