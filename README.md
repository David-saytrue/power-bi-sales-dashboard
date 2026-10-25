# Sales dashboard (Power BI)

One-page sales report: web-sourced fact table, DAX KPIs, and standard analytics visuals (trend, segment, product drill-down, map, ABC, manager losses).

**Author:** [David-saytrue](https://github.com/David-saytrue) · Tbilisi, Georgia

**File:** [`sales-dashboard-en.pbix`](sales-dashboard-en.pbix)  
Open in **Power BI Desktop**. First open: **File → Options → Global → Security → Use Map and filled map visuals**.

Related prep repo: [data-engineer-prep](https://github.com/David-saytrue/data-engineer-prep)

![Sales dashboard](dashboard.png)

## What it shows

| Visual | Question it answers |
|--------|---------------------|
| 6 KPI cards | Revenue, profit, logistics cost, profitability, active customers, average order value |
| Line chart | Revenue and profit over time |
| Bar chart | Revenue by customer segment |
| Matrix | Product hierarchy: category → subcategory → product |
| Filled map | Revenue by region |
| Manager table | Loss-making order count and profit by manager |
| ABC table | Products ranked by revenue (Pareto: A ≤80%, B ≤95%, C rest) |
| Slicers | Date, region, segment |

## Model

Source is a Google Sheet workbook loaded with `Web.Contents` (not a local Excel file). Power Query flattens lookups into one **Продажи** (Sales) table:

| Join key | Lookup | Brought in |
|----------|--------|------------|
| `Order_ID` | Dates | `Дата` |
| `Продукт` | Products | category, subcategory |
| `Покупатель` | Customers | `Сегмент` |
| `Регион` | Managers | `Менеджер` |
| `Метод доставки` | Shipping rates | `Стоимость доставки` |

Blank `Order_ID` rows are dropped. Lookup queries are **Enable load OFF**; only Sales loads into the model.

M scripts: `queries/`. Column names stay in Russian (source headers). Report titles are English.

## DAX

Measures live on **Продажи**. Names differ from columns so Power BI does not reject them.

```dax
Сумма выручки = SUM('Продажи'[Выручка])
Сумма прибыли = SUM('Продажи'[Прибыль])
Затраты на логистику = SUM('Продажи'[Стоимость доставки])
Рентабельность = DIVIDE([Сумма прибыли], [Сумма выручки], 0)   -- format %
АКБ = DISTINCTCOUNT('Продажи'[Покупатель])
Средний чек = DIVIDE([Сумма выручки], DISTINCTCOUNT('Продажи'[Order_ID]), 0)
Заказы убыт =
CALCULATE(
    DISTINCTCOUNT('Продажи'[Order_ID]),
    'Продажи'[Прибыль] < 0
)
```

Full copy-paste: [`dax-measures.dax`](dax-measures.dax).

**Why these definitions**

- Profitability is a ratio, not a sum.
- Active customers is distinct buyers, not rows.
- Average order value is per **order**, not per line.
- Loss-making orders use `CALCULATE` + `Прибыль < 0`.
- Managers join on **region**, not customer.

## Rebuild notes

1. Paste each `queries/*.m` into Power Query Advanced Editor (same query names).
2. Close & Apply.
3. Recreate the 7 measures (or run `scripts/Create-All-Measures.csx` in Tabular Editor).
4. Optional ABC class column: `queries/ABC-Products.m` with Enable load ON.

## Portfolio note

This is a compact analytics case (course-style Superstore data), not a production semantic model. It shows web ingest, Power Query joins, reusable DAX, and a readable one-page report.
