// #include <stdio.h>
// #include <string.h>
// #include <stdlib.h>
// #include "user.h"

// __declspec(dllexport) bool change_id(const char* old_id, const char* new_id) {
//     User* users = (User*)malloc(MAX_USERS * sizeof(User));
//     if (users == NULL) return false;

//     int num_users = load_users(users, MAX_USERS);

//     qsort(users, num_users, sizeof(User), compare_users);

//     int index = binary_search(users, 0, num_users - 1, old_id);
//     if (index == -1) {
//         free(users);
//         return false;
//     }

//     if (binary_search(users, 0, num_users - 1, new_id) != -1) {
//         free(users);
//         return false; // �ߺ� ID
//     }

//     // Correct usage of strcpy_s
//     strcpy_s(users[index].id, sizeof(users[index].id), new_id);

//     FILE* csv_file = fopen("static/user.csv", "w");
//     if (!csv_file) {
//         free(users);
//         return false;
//     }

//     for (int i = 0; i < num_users; i++) {
//         fprintf(csv_file, "%s,%s,%s,%s,%s,%s,%s\n",
//             users[i].id, users[i].pw, users[i].status,
//             users[i].role, users[i].name, users[i].birthday, users[i].gender);
//     }

//     fclose(csv_file);
//     free(users);
//     return true;
// }
///////////////////////////////////////////////////////////////////////////////////////////////////////
// #include <stdio.h>
// #include <string.h>
// #include <stdlib.h>
// #include "user.h"

// __declspec(dllexport) bool change_id(const char* old_id, const char* new_id) {
//     User* users = (User*)malloc(MAX_USERS * sizeof(User));
//     if (users == NULL) {
//         printf("메모리 할당에 실패했습니다.\n");
//         return false;
//     }

//     int num_users = load_users(users, MAX_USERS);
//     qsort(users, num_users, sizeof(User), compare_users);

//     int index = binary_search(users, 0, num_users - 1, old_id);
//     if (index == -1) {
//         printf("기존 아이디를 찾을 수 없습니다.\n");
//         free(users);
//         return false;
//     }

//     if (binary_search(users, 0, num_users - 1, new_id) != -1) {
//         printf("새 아이디가 이미 존재합니다.\n");
//         free(users);
//         return false; // 중복 ID
//     }

//     strcpy_s(users[index].id, sizeof(users[index].id), new_id);

//     FILE* csv_file = fopen("static/user.csv", "w");
//     if (!csv_file) {
//         printf("파일 열기에 실패했습니다.\n");
//         free(users);
//         return false;
//     }

//     for (int i = 0; i < num_users; i++) {
//         fprintf(csv_file, "%s,%s,%s,%s,%s,%s,%s\n",
//             users[i].id, users[i].pw, users[i].status,
//             users[i].role, users[i].name, users[i].birthday, users[i].gender);
//     }

//     fclose(csv_file);
//     free(users);
//     return true;
// }


#include "user.h"

__declspec(dllexport) bool change_id(const char* old_id, const char* new_id) {
    // 힙 메모리에 User 배열 할당
    User* users = (User*)malloc(MAX_USERS * sizeof(User));
    if (users == NULL) {
        printf("Memory allocation failed.\n");
        return false;
    }

    int num_users = load_users(users, MAX_USERS);

    if (num_users == 0) {
        printf("No users loaded.\n");
        free(users); // 메모리 해제
        return false;
    }

    // User 배열을 ID 기준으로 정렬
    qsort(users, num_users, sizeof(User), compare_users);

    // 기존 아이디가 있는지 확인
    int index = binary_search(users, 0, num_users - 1, old_id);
    if (index == -1) {
        printf("User not found.\n");
        free(users); // 메모리 해제
        return false;
    }

    // 새 아이디가 중복되는지 확인
    if (binary_search(users, 0, num_users - 1, new_id) != -1) {
        printf("New ID already exists.\n");
        free(users); // 메모리 해제
        return false;
    }

    // 아이디 변경
    strcpy(users[index].id, new_id);

    // 변경된 사용자 정보를 CSV 파일에 다시 저장
    FILE* csv_file = fopen("static/user.csv", "w");
    if (!csv_file) {
        perror("Failed to open CSV file for writing");
        free(users); // 메모리 해제
        return false;
    }

    for (int i = 0; i < num_users; i++) {
        fprintf(csv_file, "%s,%s,%s,%s,%s,%s,%s\n",
            users[i].id, users[i].pw, users[i].status,
            users[i].role, users[i].name, users[i].birthday, users[i].gender);
    }

    fclose(csv_file);
    free(users); // 메모리 해제

    return true;
}
