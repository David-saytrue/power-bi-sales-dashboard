// Tabular Editor 3 — C# Script → paste all → F5

var t = Model.Tables["Продажи"];

if (!t.Measures.Contains("Сумма выручки"))
    t.AddMeasure("Сумма выручки", "SUM('Продажи'[Выручка])");
else
    t.Measures["Сумма выручки"].Expression = "SUM('Продажи'[Выручка])";
t.Measures["Сумма выручки"].FormatString = "#,0.00";

if (!t.Measures.Contains("Сумма прибыли"))
    t.AddMeasure("Сумма прибыли", "SUM('Продажи'[Прибыль])");
else
    t.Measures["Сумма прибыли"].Expression = "SUM('Продажи'[Прибыль])";
t.Measures["Сумма прибыли"].FormatString = "#,0.00";

if (!t.Measures.Contains("Затраты на логистику"))
    t.AddMeasure("Затраты на логистику", "SUM('Продажи'[Стоимость доставки])");
else
    t.Measures["Затраты на логистику"].Expression = "SUM('Продажи'[Стоимость доставки])";
t.Measures["Затраты на логистику"].FormatString = "#,0.00";

if (!t.Measures.Contains("Рентабельность"))
    t.AddMeasure("Рентабельность", "DIVIDE([Сумма прибыли], [Сумма выручки], 0)");
else
    t.Measures["Рентабельность"].Expression = "DIVIDE([Сумма прибыли], [Сумма выручки], 0)";
t.Measures["Рентабельность"].FormatString = "0.00%";

if (!t.Measures.Contains("АКБ"))
    t.AddMeasure("АКБ", "DISTINCTCOUNT('Продажи'[Покупатель])");
else
    t.Measures["АКБ"].Expression = "DISTINCTCOUNT('Продажи'[Покупатель])";
t.Measures["АКБ"].FormatString = "#,0";

if (!t.Measures.Contains("Средний чек"))
    t.AddMeasure("Средний чек", "DIVIDE([Сумма выручки], DISTINCTCOUNT('Продажи'[Order_ID]), 0)");
else
    t.Measures["Средний чек"].Expression = "DIVIDE([Сумма выручки], DISTINCTCOUNT('Продажи'[Order_ID]), 0)";
t.Measures["Средний чек"].FormatString = "#,0.00";

if (!t.Measures.Contains("Заказы убыт"))
    t.AddMeasure("Заказы убыт", "CALCULATE(DISTINCTCOUNT('Продажи'[Order_ID]), 'Продажи'[Прибыль] < 0)");
else
    t.Measures["Заказы убыт"].Expression = "CALCULATE(DISTINCTCOUNT('Продажи'[Order_ID]), 'Продажи'[Прибыль] < 0)";
t.Measures["Заказы убыт"].FormatString = "#,0";

Info("OK: 7 measures on Продажи");
