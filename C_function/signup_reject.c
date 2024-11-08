#define _CRT_SECURE_NO_WARNINGS
#include "user.h"

// reject_user �Լ� DLL�� ��������
__declspec(dllexport) bool signup_reject(const char* ID) {
    User users[MAX_USERS];
    int num_users = load_users(users, MAX_USERS);

    if (num_users == 0) {
        printf("No users loaded.\n");
        return false;
    }

    // ����� �迭�� ID�� �������� ����
    qsort(users, num_users, sizeof(User), compare_users);

    // ���� Ž������ ������ ����� ã��
    int index = binary_search(users, 0, num_users - 1, ID);
    if (index == -1) {
        printf("User not found.\n");
        return false;
    }

    // ã�� ������� ���¸� "rejected"�� ����
    strcpy(users[index].status, "rejected");

    // ����� �����͸� �ٽ� CSV ���Ͽ� ����
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
