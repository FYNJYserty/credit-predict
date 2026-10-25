import unittest
from unittest.mock import patch

from app.ml.predict import predict_risk
from app.routes import FIELDS, parse_form
from run import app


class PredictionPageTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.values = {
            "RevolvingUtilizationOfUnsecuredLines": "0.3",
            "age": "45",
            "NumberOfTime30-59DaysPastDueNotWorse": "0",
            "DebtRatio": "0.2",
            "MonthlyIncome": "5000",
            "NumberOfOpenCreditLinesAndLoans": "5",
            "NumberOfTimes90DaysLate": "0",
            "NumberRealEstateLoansOrLines": "1",
            "NumberOfTime60-89DaysPastDueNotWorse": "0",
            "NumberOfDependents": "2",
        }

    def test_get_shows_all_features(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        for field in FIELDS:
            self.assertIn(f'name="{field["name"]}"', response.text)

    def test_post_displays_model_prediction(self):
        expected = predict_risk(parse_form(self.values))
        response = self.client.post("/", data=self.values)
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'{expected["probability"] * 100:.1f}%', response.text)
        self.assertIn('value="5000"', response.text)

    def test_optional_missing_values(self):
        self.values["MonthlyIncome"] = ""
        self.values["NumberOfDependents"] = ""
        response = self.client.post("/", data=self.values)
        self.assertEqual(response.status_code, 200)
        self.assertIn('class="score"', response.text)

    def test_invalid_inputs_never_reach_model(self):
        for name, value in [
            ("age", ""), ("age", "17"), ("age", "121"),
            ("age", "45.5"), ("DebtRatio", "-1"),
            ("MonthlyIncome", "nan"), ("MonthlyIncome", "inf"),
            ("MonthlyIncome", "abc"), ("NumberOfDependents", "1.5"),
        ]:
            with self.subTest(name=name, value=value):
                with patch("app.routes.predict_risk") as predict:
                    response = self.client.post("/", data={**self.values, name: value})
                    self.assertEqual(response.status_code, 400)
                    self.assertIn('role="alert"', response.text)
                    predict.assert_not_called()

    def test_missing_model_shows_message(self):
        with patch("app.routes.predict_risk", side_effect=FileNotFoundError):
            response = self.client.post("/", data=self.values)
        self.assertEqual(response.status_code, 503)
        self.assertIn("Модель не найдена", response.text)


if __name__ == "__main__":
    unittest.main()
