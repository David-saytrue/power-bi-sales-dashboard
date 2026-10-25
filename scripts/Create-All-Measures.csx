// Tabular Editor 3 — C# Script → paste all → F5

var t = Model.Tables["Sales"];

if (!t.Measures.Contains("Total Revenue"))
    t.AddMeasure("Total Revenue", "SUM('Sales'[Revenue])");
else
    t.Measures["Total Revenue"].Expression = "SUM('Sales'[Revenue])";
t.Measures["Total Revenue"].FormatString = "#,0.00";

if (!t.Measures.Contains("Total Profit"))
    t.AddMeasure("Total Profit", "SUM('Sales'[Profit])");
else
    t.Measures["Total Profit"].Expression = "SUM('Sales'[Profit])";
t.Measures["Total Profit"].FormatString = "#,0.00";

if (!t.Measures.Contains("Logistics Cost"))
    t.AddMeasure("Logistics Cost", "SUM('Sales'[ShippingCost])");
else
    t.Measures["Logistics Cost"].Expression = "SUM('Sales'[ShippingCost])";
t.Measures["Logistics Cost"].FormatString = "#,0.00";

if (!t.Measures.Contains("Profitability"))
    t.AddMeasure("Profitability", "DIVIDE([Total Profit], [Total Revenue], 0)");
else
    t.Measures["Profitability"].Expression = "DIVIDE([Total Profit], [Total Revenue], 0)";
t.Measures["Profitability"].FormatString = "0.00%";

if (!t.Measures.Contains("Active Customers"))
    t.AddMeasure("Active Customers", "DISTINCTCOUNT('Sales'[Customer])");
else
    t.Measures["Active Customers"].Expression = "DISTINCTCOUNT('Sales'[Customer])";
t.Measures["Active Customers"].FormatString = "#,0";

if (!t.Measures.Contains("Avg Order Value"))
    t.AddMeasure("Avg Order Value", "DIVIDE([Total Revenue], DISTINCTCOUNT('Sales'[Order_ID]), 0)");
else
    t.Measures["Avg Order Value"].Expression = "DIVIDE([Total Revenue], DISTINCTCOUNT('Sales'[Order_ID]), 0)";
t.Measures["Avg Order Value"].FormatString = "#,0.00";

if (!t.Measures.Contains("Loss Making Orders"))
    t.AddMeasure("Loss Making Orders", "CALCULATE(DISTINCTCOUNT('Sales'[Order_ID]), 'Sales'[Profit] < 0)");
else
    t.Measures["Loss Making Orders"].Expression = "CALCULATE(DISTINCTCOUNT('Sales'[Order_ID]), 'Sales'[Profit] < 0)";
t.Measures["Loss Making Orders"].FormatString = "#,0";

Info("OK: 7 measures on Sales");
