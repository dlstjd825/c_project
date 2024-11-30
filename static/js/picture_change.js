// 선택된 사진을 모달에 표시
let selectedPhoto = "";

function openModal(photoName) {
    selectedPhoto = photoName; // 선택된 사진 경로 저장
    console.log("Selected photo:", selectedPhoto); // 디버그 로그 추가
    document.getElementById("modal-photo").src = selectedPhoto; // 모달에 선택된 사진 표시
    document.getElementById("photoModal").style.display = "block"; // 모달 열기
}

// 모달 닫기
function closeModal() {
    document.getElementById("photoModal").style.display = "none"; // 모달 닫기
}

function confirmPhotoChange() {
    if (selectedPhoto) {
        // 클라이언트에서 변경된 프로필 사진을 서버로 전송
        fetch('/update-profile-picture', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ photo: selectedPhoto }) // 선택된 사진 경로를 전송
        })
        .then(response => {
            if (response.ok) {
                document.getElementById("profile-picture").src = selectedPhoto;

                closeModal();
                alert("프로필 사진이 성공적으로 변경되었습니다!");
            } else {
                alert("프로필 사진 변경에 실패했습니다.");
            }
        })
         .catch((error) => {
             console.error("Error:", error);
             alert("서버 요청 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.");
         });
    } else {
        alert("사진을 선택해주세요.");
    }
}




// function confirmPhotoChange() {
//     console.log("Changing to photo:", selectedPhoto); // 디버그 로그 추가
//     if (selectedPhoto) {
//         document.getElementById("profile-picture").src = selectedPhoto;
//         closeModal();
//         alert("프로필 사진이 변경되었습니다!");
//     } else {
//         alert("사진을 선택해주세요.");
//     }
// }






// // 프로필 사진 변경 확인
// function confirmPhotoChange() {
//     // 서버 요청 보내기 (실제로는 확인 로그만 출력)
//     fetch("/update-profile-photo", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ photo: selectedPhoto }), // 선택된 사진 경로 전송
//     })
//         .then((response) => response.json())
//         .then((data) => {
//             if (data.success) {
//                 // HTML에서 프로필 사진 즉시 변경
//                 document.getElementById("profile-picture").src = selectedPhoto; 
//                 alert("프로필 사진이 변경되었습니다!");
//             } else {
//                 alert("프로필 사진 변경에 실패했습니다.");
//             }
//         })
//         .catch((error) => {
//             console.error("Error:", error);
//             alert("서버 요청 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.");
//         });

//     // 모달 닫기
//     closeModal();
// }


