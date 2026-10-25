FIELDS = [
    {"name": name, "label": label, "integer": integer, "minimum": minimum}
    for name, label, integer, minimum in [
        ("RevolvingUtilizationOfUnsecuredLines", "Доля использованного кредитного лимита", False, 0),
        ("age", "Возраст (лет)", True, 18),
        ("NumberOfTime30-59DaysPastDueNotWorse", "Число просрочек на 30–59 дней", True, 0),
        ("DebtRatio", "Отношение ежемесячных долговых платежей к доходу", False, 0),
        ("MonthlyIncome", "Ежемесячный доход (в единицах исходного датасета)", False, 0),
        ("NumberOfOpenCreditLinesAndLoans", "Число открытых кредитных линий и займов", True, 0),
        ("NumberOfTimes90DaysLate", "Число просрочек на 90 дней и более", True, 0),
        ("NumberRealEstateLoansOrLines", "Число кредитов под недвижимость", True, 0),
        ("NumberOfTime60-89DaysPastDueNotWorse", "Число просрочек на 60–89 дней", True, 0),
        ("NumberOfDependents", "Число иждивенцев", True, 0),
    ]
]
OPTIONAL = {"MonthlyIncome", "NumberOfDependents"}
FIELD_HINTS = {
    "RevolvingUtilizationOfUnsecuredLines": "Доля от 0: 0 — лимит не использован, 0.5 — 50%, 1 — 100%. При превышении лимита допустимо больше 1, например 1.2.",
    "age": "Целое число от 18 до 120, например 45.",
    "NumberOfTime30-59DaysPastDueNotWorse": "Целое количество: 0 — не было, 1 — один случай, 2 — два и т. д.",
    "DebtRatio": "Число от 0: 0.3 — платежи составляют 30% дохода, 1 — 100%. Может быть больше 1.",
    "MonthlyIncome": "Сумма за месяц от 0, например 5000. Если доход неизвестен, оставьте поле пустым; 0 означает отсутствие дохода.",
    "NumberOfOpenCreditLinesAndLoans": "Целое количество: 0 — нет открытых кредитов, 1, 2, 3 и т. д.",
    "NumberOfTimes90DaysLate": "Целое количество: 0 — не было, 1 — один случай, 2 — два и т. д.",
    "NumberRealEstateLoansOrLines": "Целое количество: 0 — нет таких кредитов, 1, 2, 3 и т. д.",
    "NumberOfTime60-89DaysPastDueNotWorse": "Целое количество: 0 — не было, 1 — один случай, 2 — два и т. д.",
    "NumberOfDependents": "Целое количество: 0 — нет иждивенцев, 1, 2, 3 и т. д. Если неизвестно, оставьте поле пустым.",
}
