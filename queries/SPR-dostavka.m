let
    WebWorkbook = "https://docs.google.com/spreadsheets/d/1OObWrvhvYo5_PsLNpYN3ngbgXCMqc112TBvVsPGv9iY/export?format=xlsx",
    Source = Excel.Workbook(Web.Contents(WebWorkbook), null, true),
    Sheet = Source{[Item = "СПР_стоимость_доставки", Kind = "Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet, [PromoteAllScalars = true]),
    #"Filtered Rows" = Table.SelectRows(#"Promoted Headers", each [Метод доставки] <> null and [Метод доставки] <> ""),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows", {{"Стоимость доставки", type number}})
in
    #"Changed Type"
