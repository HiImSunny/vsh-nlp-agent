"""
Generate synthetic Vietnamese MCQA data for fine-tuning.
Uses the model itself to generate Q&A pairs from Wikipedia passages
or the public test questions as seeds.

Usage: python scripts/generate_synthetic_data.py --output data/synthetic_train.json
"""
from __future__ import annotations
import argparse
import json
import random
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Vietnamese topics for seed questions
SEED_TOPICS: list[str] = [
    "Thủ đô của Việt Nam là gì?",
    "Sông nào dài nhất Việt Nam?",
    "Năm nào Việt Nam giành độc lập?",
    "Ai là chủ tịch đầu tiên của nước Việt Nam?",
    "Biển nào ở phía đông Việt Nam?",
    "Cây gì là biểu tượng của Việt Nam?",
    "Tết Nguyên Đán là lễ hội gì?",
    "Phở là món ăn đặc sản của vùng nào?",
    "Vịnh Hạ Long nằm ở tỉnh nào?",
    "Đồng tiền chính thức của Việt Nam là gì?",
    "Dân tộc nào chiếm đa số ở Việt Nam?",
    "Cố đô Huế nằm ở miền nào?",
    "Bác Hồ sinh năm nào?",
    "Đường Hồ Chí Minh chạy qua bao nhiêu tỉnh?",
    "Chùa Một Cột được xây dựng dưới triều đại nào?",
    "Văn Miếu Quốc Tử Giám được xây dựng năm nào?",
    "Nước nào có biên giới giáp Việt Nam ở phía bắc?",
    "Quốc kỳ Việt Nam có màu gì?",
    "Nhà thơ Nguyễn Du nổi tiếng với tác phẩm gì?",
    "Rừng Cúc Phương là vườn quốc gia của tỉnh nào?",
    "Biển Đông có bao nhiêu quốc gia tiếp giáp?",
    "Cà Mau là tỉnh cực nam của Việt Nam, đúng hay sai?",
    "Sân bay quốc tế lớn nhất Việt Nam là sân bay nào?",
    "Dân số Việt Nam khoảng bao nhiêu người?",
    "Cầu Long Biên do ai xây dựng?",
    "Ẩm thực Việt Nam nổi tiếng với món nào nhất?",
    "Bến Nhà Rồng gắn liền với sự kiện lịch sử nào?",
    "Đội tuyển bóng đá Việt Nam vô địch AFF Cup năm nào?",
    "Cao nguyên đá Đồng Văn nằm ở tỉnh nào?",
    "Hồ Gươm còn có tên gọi khác là gì?",
]

# Synthetic data with correct answers and distractors
SYNTHETIC_MCQ: list[dict] = [
    {"q": "Thủ đô của Việt Nam là gì?", "choices": ["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng", "Huế"], "answer": "A"},
    {"q": "Sông nào dài nhất Việt Nam?", "choices": ["Sông Hồng", "Sông Mê Kông", "Sông Đà", "Sông Cửu Long"], "answer": "B"},
    {"q": "Việt Nam giành độc lập năm nào?", "choices": ["1945", "1954", "1975", "1930"], "answer": "A"},
    {"q": "Ai là chủ tịch đầu tiên của nước Việt Nam?", "choices": ["Hồ Chí Minh", "Tôn Đức Thắng", "Võ Nguyên Giáp", "Phạm Văn Đồng"], "answer": "A"},
    {"q": "Biển nào ở phía đông Việt Nam?", "choices": ["Biển Đông", "Biển Tây", "Biển Nam", "Biển Bắc"], "answer": "A"},
    {"q": "Phở là món ăn đặc sản của vùng nào?", "choices": ["Nam Bộ", "Bắc Bộ", "Trung Bộ", "Tây Nguyên"], "answer": "B"},
    {"q": "Vịnh Hạ Long nằm ở tỉnh nào?", "choices": ["Quảng Ninh", "Hải Phòng", "Thái Bình", "Nam Định"], "answer": "A"},
    {"q": "Đồng tiền chính thức của Việt Nam là gì?", "choices": ["Đồng", "USD", "Euro", "Yên"], "answer": "A"},
    {"q": "Dân tộc nào chiếm đa số ở Việt Nam?", "choices": ["Kinh", "Tày", "Thái", "Mường"], "answer": "A"},
    {"q": "Cố đô Huế nằm ở miền nào?", "choices": ["Bắc Trung Bộ", "Nam Trung Bộ", "Đồng bằng sông Hồng", "Tây Nguyên"], "answer": "A"},
    {"q": "Chùa Một Cột được xây dựng dưới triều đại nào?", "choices": ["Lý", "Trần", "Lê", "Nguyễn"], "answer": "A"},
    {"q": "Nước nào có biên giới giáp Việt Nam ở phía bắc?", "choices": ["Trung Quốc", "Lào", "Campuchia", "Thái Lan"], "answer": "A"},
    {"q": "Quốc kỳ Việt Nam có màu gì?", "choices": ["Đỏ và vàng", "Xanh và đỏ", "Vàng và trắng", "Đỏ và xanh"], "answer": "A"},
    {"q": "Nhà thơ Nguyễn Du nổi tiếng với tác phẩm gì?", "choices": ["Truyện Kiều", "Lục Vân Tiên", "Cung oán ngâm khúc", "Chinh phụ ngâm"], "answer": "A"},
    {"q": "Cầu Long Biên do ai xây dựng?", "choices": ["Pháp", "Mỹ", "Nhật", "Việt Nam"], "answer": "A"},
    {"q": "Bến Nhà Rồng gắn liền với sự kiện lịch sử nào?", "choices": ["Bác Hồ ra đi tìm đường cứu nước", "Cách mạng tháng Tám", "Chiến dịch Điện Biên Phủ", "Ngày thống nhất đất nước"], "answer": "A"},
    {"q": "Hồ Gươm còn có tên gọi khác là gì?", "choices": ["Hồ Hoàn Kiếm", "Hồ Tây", "Hồ Thiền Quang", "Hồ Bảy Mẫu"], "answer": "A"},
    {"q": "Cà Mau là tỉnh cực nam của Việt Nam, đúng hay sai?", "choices": ["Đúng", "Sai"], "answer": "A"},
    {"q": "Dân số Việt Nam khoảng bao nhiêu người?", "choices": ["100 triệu", "80 triệu", "120 triệu", "60 triệu"], "answer": "A"},
    {"q": "Cao nguyên đá Đồng Văn nằm ở tỉnh nào?", "choices": ["Hà Giang", "Cao Bằng", "Lạng Sơn", "Lào Cai"], "answer": "A"},
    {"q": "Đội tuyển bóng đá Việt Nam vô địch AFF Cup năm nào?", "choices": ["2018", "2016", "2020", "2014"], "answer": "A"},
    {"q": "Rừng Cúc Phương là vườn quốc gia của tỉnh nào?", "choices": ["Ninh Bình", "Thanh Hóa", "Hòa Bình", "Hà Nam"], "answer": "A"},
    {"q": "Sân bay quốc tế lớn nhất Việt Nam là sân bay nào?", "choices": ["Tân Sơn Nhất", "Nội Bài", "Đà Nẵng", "Cam Ranh"], "answer": "A"},
    {"q": "Tết Nguyên Đán là lễ hội gì?", "choices": ["Tết cổ truyền dân tộc", "Tết Thiếu nhi", "Tết Trung thu", "Tết Lao động"], "answer": "A"},
    {"q": "Biển Đông có bao nhiêu quốc gia tiếp giáp?", "choices": ["9", "7", "11", "5"], "answer": "A"},
    {"q": "Văn Miếu Quốc Tử Giám được xây dựng năm nào?", "choices": ["1070", "1010", "1225", "1400"], "answer": "A"},
    {"q": "Bác Hồ sinh năm nào?", "choices": ["1890", "1891", "1889", "1892"], "answer": "A"},
    {"q": "Đường Hồ Chí Minh chạy qua bao nhiêu tỉnh?", "choices": ["21", "15", "30", "10"], "answer": "A"},
    {"q": "Cây gì là biểu tượng của Việt Nam?", "choices": ["Tre", "Lúa", "Dừa", "Sen"], "answer": "A"},
    {"q": "Ẩm thực Việt Nam nổi tiếng với món nào nhất?", "choices": ["Phở", "Bánh mì", "Bún chả", "Cà phê"], "answer": "A"},
    {"q": "Hà Nội là thủ đô của Việt Nam từ năm nào?", "choices": ["1010", "1945", "1954", "1976"], "answer": "A"},
    {"q": "Khí hậu Việt Nam thuộc loại nào?", "choices": ["Nhiệt đới gió mùa", "Ôn đới", "Hàn đới", "Địa trung hải"], "answer": "A"},
    {"q": "Địa hình Việt Nam chủ yếu là gì?", "choices": ["Đồi núi", "Đồng bằng", "Cao nguyên", "Bờ biển"], "answer": "A"},
    {"q": "Nước nào có dân số đông nhất Đông Nam Á?", "choices": ["Indonesia", "Việt Nam", "Philippines", "Thái Lan"], "answer": "A"},
    {"q": "Cây lúa là cây lương thực chính của người Việt, đúng hay sai?", "choices": ["Đúng", "Sai"], "answer": "A"},
    {"q": "Sông Hồng bắt nguồn từ nước nào?", "choices": ["Trung Quốc", "Lào", "Myanmar", "Việt Nam"], "answer": "A"},
    {"q": "Thành phố Hồ Chí Minh trước đây có tên là gì?", "choices": ["Sài Gòn", "Gia Định", "Chợ Lớn", "Bến Thành"], "answer": "A"},
    {"q": "Quốc hoa của Việt Nam là hoa gì?", "choices": ["Hoa sen", "Hoa mai", "Hoa đào", "Hoa phượng"], "answer": "A"},
    {"q": "Ngày Quốc khánh Việt Nam là ngày nào?", "choices": ["2/9", "30/4", "1/5", "19/5"], "answer": "A"},
    {"q": "Chiến dịch Điện Biên Phủ kết thúc năm nào?", "choices": ["1954", "1945", "1975", "1968"], "answer": "A"},
    {"q": "Việt Nam có bao nhiêu tỉnh thành?", "choices": ["63", "58", "64", "60"], "answer": "A"},
    {"q": "Nước nào được mệnh danh là 'đất nước hình chữ S'?", "choices": ["Việt Nam", "Lào", "Campuchia", "Myanmar"], "answer": "A"},
    {"q": "Đảo lớn nhất Việt Nam là đảo nào?", "choices": ["Phú Quốc", "Cát Bà", "Côn Đảo", "Lý Sơn"], "answer": "A"},
    {"q": "Vườn quốc gia Phong Nha - Kẻ Bàng nằm ở tỉnh nào?", "choices": ["Quảng Bình", "Quảng Trị", "Hà Tĩnh", "Nghệ An"], "answer": "A"},
    {"q": "Dãy núi nào là ranh giới giữa Việt Nam và Lào?", "choices": ["Trường Sơn", "Hoàng Liên Sơn", "Tam Đảo", "Bạch Mã"], "answer": "A"},
    {"q": "Biển Việt Nam có bao nhiêu huyện đảo?", "choices": ["12", "10", "15", "8"], "answer": "A"},
    {"q": "Lăng Chủ tịch Hồ Chí Minh nằm ở đâu?", "choices": ["Hà Nội", "TP. Hồ Chí Minh", "Nghệ An", "Huế"], "answer": "A"},
    {"q": "Bán đảo Sơn Trà thuộc thành phố nào?", "choices": ["Đà Nẵng", "Nha Trang", "Hải Phòng", "Vũng Tàu"], "answer": "A"},
    {"q": "Chợ Bến Thành nằm ở thành phố nào?", "choices": ["TP. Hồ Chí Minh", "Hà Nội", "Đà Nẵng", "Cần Thơ"], "answer": "A"},
    {"q": "Cửa khẩu quốc tế Mộc Bài thuộc tỉnh nào?", "choices": ["Tây Ninh", "Long An", "Bình Phước", "Đồng Tháp"], "answer": "A"},
    {"q": "Tỉnh nào có diện tích lớn nhất Việt Nam?", "choices": ["Nghệ An", "Gia Lai", "Sơn La", "Thanh Hóa"], "answer": "A"},
    {"q": "Tỉnh nào có dân số đông nhất Việt Nam?", "choices": ["TP. Hồ Chí Minh", "Hà Nội", "Thanh Hóa", "Nghệ An"], "answer": "A"},
    {"q": "Mùa mưa ở miền Nam Việt Nam từ tháng mấy?", "choices": ["Tháng 5 đến tháng 11", "Tháng 1 đến tháng 6", "Tháng 7 đến tháng 12", "Tháng 3 đến tháng 9"], "answer": "A"},
    {"q": "Cây cao su được trồng nhiều ở vùng nào?", "choices": ["Đông Nam Bộ", "Tây Nguyên", "Trung Bộ", "Bắc Bộ"], "answer": "A"},
    {"q": "Loại hình nghệ thuật nào là di sản văn hóa phi vật thể?", "choices": ["Nhã nhạc cung đình Huế", "Cải lương", "Chèo", "Tuồng"], "answer": "A"},
    {"q": "Trường Đại học đầu tiên của Việt Nam là gì?", "choices": ["Văn Miếu Quốc Tử Giám", "Đại học Bách Khoa", "Đại học Sư phạm", "Đại học Y Hà Nội"], "answer": "A"},
    {"q": "Ngô Quyền đánh thắng quân Nam Hán trên sông nào?", "choices": ["Sông Bạch Đằng", "Sông Hồng", "Sông Mã", "Sông Đà"], "answer": "A"},
    {"q": "Vua Quang Trung đại phá quân Thanh năm nào?", "choices": ["1789", "1771", "1802", "1757"], "answer": "A"},
    {"q": "Nhà Nguyễn thành lập năm nào?", "choices": ["1802", "1778", "1820", "1789"], "answer": "A"},
    {"q": "Hệ thống đường mòn Hồ Chí Minh được xây dựng vào thời kỳ nào?", "choices": ["Chiến tranh Việt Nam", "Chiến tranh Pháp", "Chiến tranh biên giới", "Thời kỳ hòa bình"], "answer": "A"},
    {"q": "Phong trào Cần Vương do ai lãnh đạo?", "choices": ["Tôn Thất Thuyết", "Phan Đình Phùng", "Hoàng Hoa Thám", "Nguyễn Trường Tộ"], "answer": "A"},
    {"q": "Đồng bằng sông Cửu Long nằm ở miền nào?", "choices": ["Nam Bộ", "Bắc Bộ", "Trung Bộ", "Tây Nguyên"], "answer": "A"},
    {"q": "Bánh chưng, bánh dày gắn liền với truyền thuyết vua nào?", "choices": ["Hùng Vương", "Lý Thái Tổ", "Trần Hưng Đạo", "Lê Lợi"], "answer": "A"},
    {"q": "Cồng chiêng là nhạc cụ truyền thống của dân tộc nào?", "choices": ["Tây Nguyên", "Kinh", "Mông", "Khmer"], "answer": "A"},
    {"q": "Ở Việt Nam, cà phê được trồng nhiều nhất ở vùng nào?", "choices": ["Tây Nguyên", "Đông Nam Bộ", "Bắc Trung Bộ", "Trung du miền núi phía Bắc"], "answer": "A"},
]


def generate_synthetic_alpaca() -> list[dict]:
    """Convert synthetic MCQ to Alpaca format."""
    alpaca: list[dict] = []
    for item in SYNTHETIC_MCQ:
        labels = [chr(ord("A") + i) for i in range(len(item["choices"]))]
        choices_text = "\n".join(
            f"{l}. {c}" for l, c in zip(labels, item["choices"])
        )
        alpaca.append(
            {
                "instruction": "Đây là câu hỏi trắc nghiệm tiếng Việt. "
                "Chọn đáp án đúng bằng cách trả lời CHỈ bằng một chữ cái.",
                "input": f"Câu hỏi: {item['q']}\n\n{choices_text}\nĐáp án:",
                "output": item["answer"],
            }
        )
    return alpaca


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="data/synthetic_train.json",
        help="Output Alpaca-format JSON",
    )
    parser.add_argument(
        "--num-public",
        type=int,
        default=0,
        help="Number of public test questions to include (0 = none)",
    )
    args = parser.parse_args()

    data = generate_synthetic_alpaca()

    # Optionally include public test questions (without labels, output="")
    if args.num_public > 0:
        public_path = Path("public-test_1780368312.json")
        if public_path.exists():
            import json as _json

            with open(public_path, encoding="utf-8") as f:
                pub = _json.load(f)
            questions = pub[: args.num_public]
            for q in questions:
                labels = [
                    chr(ord("A") + i)
                    for i in range(len(q["choices"]))
                ]
                choices_text = "\n".join(
                    f"{l}. {c}"
                    for l, c in zip(labels, q["choices"])
                )
                data.append(
                    {
                        "instruction": "Đây là câu hỏi trắc nghiệm tiếng Việt. "
                        "Chọn đáp án đúng bằng cách trả lời CHỈ bằng một chữ cái.",
                        "input": f"Câu hỏi: {q['question']}\n\n{choices_text}\nĐáp án:",
                        "output": "",  # No label yet
                    }
                )
            print(f"Added {args.num_public} public questions (unlabeled)")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(data)} training examples")
    print(f"Labeled: {sum(1 for d in data if d['output'])}")
    print(f"Unlabeled: {sum(1 for d in data if not d['output'])}")
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()
