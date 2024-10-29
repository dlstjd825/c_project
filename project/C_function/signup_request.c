#include <stdio.h>
#include <stdbool.h>

__declspec(dllexport) bool signup_request(const char* ID, const char* PW, const char* role, const char* name, const char* birthday,  const char* gender) {
    char txt_filename[256];
    snprintf(txt_filename, sizeof(txt_filename), "static/users/%s_info.txt", ID);

    FILE* txt_file = fopen(txt_filename, "w");
    if (txt_file == NULL) {
        printf("Failed to create user info file\n");
        return false;
    }

    // 비밀번호(PW) 포함하여 파일에 쓰기
    fprintf(txt_file, "ID: %s\nPW: %s\nRole: %s\nName: %s\nBirthday: %s\nGender: %s\n", ID, PW, role, name, birthday, gender );
    fclose(txt_file);

    return true;
}
