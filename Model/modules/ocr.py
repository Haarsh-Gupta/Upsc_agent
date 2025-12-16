from paddleocr import PaddleOCR
ocr_model = PaddleOCR(use_angle_cls=True, lang="en")

def run_ocr(image_path):
    out = ocr_model.ocr(image_path, cls=True)
    lines = []
    for page in out:
        for line in page:
            lines.append(line[-1][0])
    return "\n".join(lines)
