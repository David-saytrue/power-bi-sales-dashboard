// Optional 7th query (Enable load ON). Name: ABC_Products. References loaded query Sales.
let
    Source = Sales,
    #"Grouped" = Table.Group(Source, {"Product"}, {{"Revenue", each List.Sum([Revenue]), type number}}),
    #"Sorted" = Table.Sort(#"Grouped", {{"Revenue", Order.Descending}}),
    Total = List.Sum(#"Sorted"[Revenue]),
    #"Added Index" = Table.AddIndexColumn(#"Sorted", "Rank", 1, 1),
    #"Added Running" = Table.AddColumn(
        #"Added Index",
        "Running",
        (row) => List.Sum(List.FirstN(#"Sorted"[Revenue], row[Rank])),
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
