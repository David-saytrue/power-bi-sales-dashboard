// Query name in Power Query: Customers
// Source tab id in the Google workbook (must match): СПР_покупатели
let
    WebWorkbook = "https://docs.google.com/spreadsheets/d/1OObWrvhvYo5_PsLNpYN3ngbgXCMqc112TBvVsPGv9iY/export?format=xlsx",
    Source = Excel.Workbook(Web.Contents(WebWorkbook), null, true),
    Sheet = Source{[Item = "СПР_покупатели", Kind = "Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet, [PromoteAllScalars = true]),
    cols = Table.ColumnNames(#"Promoted Headers"),
    Step1 = if List.Contains(cols, "Column1") then Table.RenameColumns(#"Promoted Headers", {{"Column1", "Customer"}}) else #"Promoted Headers",
    cols2 = Table.ColumnNames(Step1),
    Step2 =
        if List.Contains(cols2, "Column2") then Table.RenameColumns(Step1, {{"Column2", "Segment"}})
        else if List.Contains(cols2, "Сегмент покупателя") then Table.RenameColumns(Step1, {{"Сегмент покупателя", "Segment"}})
        else if List.Contains(cols2, "Сегмент") then Table.RenameColumns(Step1, {{"Сегмент", "Segment"}})
        else Step1,
    Step3 = if List.Contains(Table.ColumnNames(Step2), "Покупатель") then Table.RenameColumns(Step2, {{"Покупатель", "Customer"}}) else Step2,
    #"Removed Nulls" = Table.SelectRows(Step3, each [Customer] <> null and [Customer] <> "")
in
    #"Removed Nulls"
