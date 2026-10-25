// Query name in Power Query: Dates
// Source tab id in the Google workbook (must match): СПР_даты_заказа
let
    WebWorkbook = "https://docs.google.com/spreadsheets/d/1OObWrvhvYo5_PsLNpYN3ngbgXCMqc112TBvVsPGv9iY/export?format=xlsx",
    Source = Excel.Workbook(Web.Contents(WebWorkbook), null, true),
    Sheet = Source{[Item = "СПР_даты_заказа", Kind = "Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet, [PromoteAllScalars = true]),
    #"Renamed" = Table.RenameColumns(#"Promoted Headers", {{"Дата", "Date"}}, MissingField.Ignore),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed", {{"Order_ID", Int64.Type}, {"Date", type date}})
in
    #"Changed Type"
