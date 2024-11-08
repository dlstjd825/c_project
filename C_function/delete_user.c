#define _CRT_SECURE_NO_WARNINGS
#include "user.h"

// delete_user �Լ��� DLL�� ��������
__declspec(dllexport) bool delete_user(const char* ID) {
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

    // CSV ������ ���� ������ ����ڸ� ������ ��� ����� �ٽ� ���
    FILE* temp_file = fopen("static/temp_user.csv", "w");  // 'w' ��� ���
    if (!temp_file) {
        perror("Failed to open temp CSV file");
        return false;
    }

    for (int i = 0; i < num_users; i++) {
        if (i != index) {  // ������ ID�� �ƴ� ����ڸ� ���
            fprintf(temp_file, "%s,%s,%s,%s,%s,%s,%s\n", users[i].id, users[i].pw, users[i].status,
                users[i].role, users[i].name, users[i].birthday, users[i].gender);
        }
    }

    fclose(temp_file);

    // ���� user.csv�� temp_user.csv�� ��ü
    remove("static/user.csv");
    rename("static/temp_user.csv", "static/user.csv");

    return true;
}
