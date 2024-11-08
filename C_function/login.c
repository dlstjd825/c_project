#include "user.h"

__declspec(dllexport) int login(const char* ID, const char* PW) {
    User users[MAX_USERS];
    int num_users = load_users(users, MAX_USERS);

    // User �迭�� ID �������� ����
    qsort(users, num_users, sizeof(User), compare_users);

    // ���� Ž������ ID ã��
    int index = binary_search(users, 0, num_users - 1, ID);

    if (index != -1 && strcmp(users[index].pw, PW) == 0) {
        // ������� ���� Ȯ��
        if (strcmp(users[index].status, "approved") == 0) {
            return strcmp(ID, "admin") == 0 ? 2 : 1;  // �α��� ���� (������ �Ǵ� �Ϲ� �����)
        }
        else if (strcmp(users[index].status, "pending") == 0) {
            return -1;  // ���� ��� ���� �����
        }
        else if (strcmp(users[index].status, "rejected") == 0) {
            return -2;  // ������ �����
        }
    }

    return 0;  // �α��� ����
}