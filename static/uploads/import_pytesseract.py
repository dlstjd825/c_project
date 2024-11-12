from PIL import Image, ImageDraw
import os

# A4 용지 크기 설정 (210mm x 297mm, 약 2480x3508 픽셀)
a4_width = 2480
a4_height = 3508

# 고정 가로 폭 설정
fixed_width = 1050  # 가로 크기 1100픽셀로 고정

# 각 이미지의 비율에 맞게 세로 길이를 자동으로 조정하는 함수
def resize_image(image, fixed_width):
    width_percent = (fixed_width / float(image.size[0]))
    height_size = int((float(image.size[1]) * float(width_percent)))
    return image.resize((fixed_width, height_size), Image.LANCZOS)

# 이미지를 한 페이지에 배치하는 함수 (좌우로 2개씩)
def create_a4_page(images):
    a4_image = Image.new('RGB', (a4_width, a4_height), 'white')
    if len(images) > 0:
        resized_left_image = resize_image(images[0], fixed_width)
        a4_image.paste(resized_left_image, (100, 100))
    if len(images) > 1:
        resized_right_image = resize_image(images[1], fixed_width)
        right_x_position = a4_width - resized_right_image.width - 100
        a4_image.paste(resized_right_image, (right_x_position, 100))
    return a4_image

# 여러 장의 이미지를 받아서 A4 크기의 페이지로 만들고, PDF로 저장하는 함수
def create_pdf_from_images(image_paths, output_pdf):
    images = [Image.open(image_path) for image_path in image_paths]
    a4_pages = []
    for i in range(0, len(images), 2):
        page_images = images[i:i + 2]
        a4_page = create_a4_page(page_images)
        a4_pages.append(a4_page)
    if a4_pages:
        a4_pages[0].save(
            output_pdf,
            save_all=True,
            append_images=a4_pages[1:],
            resolution=100.0
        )
    else:
        print("이미지 리스트가 비어 있습니다.")

# 예제 실행
image_folder = r"C:\Users\korea\OneDrive\바탕 화면\example_images"  # 이미지 폴더 경로
image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.lower().endswith(('jpg', 'png'))]

# 결과 PDF 파일 경로
output_pdf_path = "result_images.pdf"

# 이미지들을 PDF로 변환
create_pdf_from_images(image_files, output_pdf_path)

print(f"PDF 파일이 저장되었습니다: {output_pdf_path}")
