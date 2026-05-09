"""Input validation cho form thêm/sửa (bản cơ bản)."""

from __future__ import annotations


def validate_row(payload: dict) -> tuple[bool, str, dict | None]:
    """
    Trả về (ok, message, cleaned_payload).
    cleaned: score(float), credits(float), age(int|None), gender chuẩn (Nam/Nữ/'').
    """
    sid = str(payload.get("student_id", "")).strip()
    name = str(payload.get("full_name", "")).strip()
    course = str(payload.get("course_code", "")).strip()
    gender_raw = str(payload.get("gender", "")).strip()
    notes = str(payload.get("notes", "")).strip()

    if not sid:
        return False, "Mời bạn nhập mã sinh viên.", None
    if not name:
        return False, "Mời bạn nhập họ tên.", None
    if not course:
        return False, "Mời bạn nhập mã môn học.", None

    score_s = str(payload.get("score", "")).strip()
    credits_s = str(payload.get("credits", "")).strip()
    age_s = str(payload.get("age", "")).strip()

    if not score_s:
        return False, "Mời bạn nhập điểm.", None
    if not credits_s:
        return False, "Mời bạn nhập tín chỉ.", None

    try:
        score = float(score_s.replace(",", "."))
    except ValueError:
        return False, "Sai kiểu dữ liệu: Điểm phải là số (vd 8.5).", None
    if score < 0 or score > 10:
        return False, "Điểm thang 10 phải trong khoảng 0–10.", None

    try:
        credits = float(credits_s.replace(",", "."))
    except ValueError:
        return False, "Sai kiểu dữ liệu: Tín chỉ phải là số.", None
    if credits <= 0:
        return False, "Tín chỉ phải lớn hơn 0.", None

    age_val: int | None
    if not age_s:
        age_val = None
    else:
        try:
            age_val = int(float(age_s.replace(",", ".")))
        except ValueError:
            return False, "Sai kiểu dữ liệu: Tuổi phải là số nguyên (vd 20).", None
        if age_val < 16 or age_val > 100:
            return False, "Tuổi hợp lệ từ 16 đến 100 (hoặc để trống).", None

    gender = ""
    if gender_raw:
        low = gender_raw.lower()
        if low == "nam":
            gender = "Nam"
        elif low in ("nữ", "nu"):
            gender = "Nữ"
        else:
            return False, "Giới tính chỉ nhập Nam hoặc Nữ (hoặc để trống).", None

    cleaned = {
        "student_id": sid,
        "full_name": name,
        "gender": gender,
        "age": "" if age_val is None else age_val,
        "course_code": course,
        "score": score,
        "credits": credits,
        "notes": notes,
    }
    return True, "OK", cleaned

