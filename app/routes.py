from math import isfinite

from flask import Blueprint, render_template, request

from app.form_fields import FIELDS, FIELD_HINTS, OPTIONAL
from app.ml.predict import predict_risk

bp = Blueprint("main", __name__)


def parse_form(values):
    features = {}
    for field in FIELDS:
        name = field["name"]
        raw = values.get(name, "").strip()
        if not raw and name in OPTIONAL:
            features[name] = float("nan")
            continue
        try:
            number = float(raw)
        except ValueError:
            raise ValueError(f"{field['label']}: введите число.") from None
        maximum = 120 if name == "age" else 1_000_000_000_000
        if not isfinite(number) or not field["minimum"] <= number <= maximum:
            raise ValueError(f"{field['label']}: допустимо от {field['minimum']} до {maximum}.")
        if field["integer"] and not number.is_integer():
            raise ValueError(f"{field['label']}: введите целое число.")
        features[name] = number
    return features


@bp.route("/", methods=["GET", "POST"])
def index():
    values = request.form.to_dict() if request.method == "POST" else {}
    result = None
    error = None
    status = 200
    if request.method == "POST":
        try:
            result = predict_risk(parse_form(values))
        except ValueError as exc:
            error = str(exc)
            status = 400
        except FileNotFoundError:
            error = "Модель не найдена. Сначала запустите app/ml/train.py."
            status = 503
    return render_template(
        "index.html", fields=FIELDS, optional=OPTIONAL,
        values=values, result=result, error=error, hints=FIELD_HINTS,
    ), status
