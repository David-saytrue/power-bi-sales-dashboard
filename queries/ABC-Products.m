// Optional 7th query: enable load ON. Reference loaded table "Продажи".
let
    Source = Продажи,
    #"Grouped" = Table.Group(Source, {"Продукт"}, {{"Выручка", each List.Sum([Выручка]), type number}}),
    #"Sorted" = Table.Sort(#"Grouped", {{"Выручка", Order.Descending}}),
    Total = List.Sum(#"Sorted"[Выручка]),
    #"Added Index" = Table.AddIndexColumn(#"Sorted", "Rank", 1, 1),
    #"Added Running" = Table.AddColumn(
        #"Added Index",
        "Running",
        (row) => List.Sum(List.FirstN(#"Sorted"[Выручка], row[Rank])),
        type number
    ),
    #"Added Pct" = Table.AddColumn(#"Added Running", "RunningPct", each if Total = 0 then 0 else [Running] / Total, type number),
    #"Added Class" = Table.AddColumn(
        #"Added Pct",
        "ABC",
        each if [RunningPct] <= 0.8 then "A" else if [RunningPct] <= 0.95 then "B" else "C",
        type text
    )
in
    #"Added Class"
