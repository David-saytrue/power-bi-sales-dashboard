let
    WebWorkbook = "https://docs.google.com/spreadsheets/d/1OObWrvhvYo5_PsLNpYN3ngbgXCMqc112TBvVsPGv9iY/export?format=xlsx",
    Source = Excel.Workbook(Web.Contents(WebWorkbook), null, true),
    Sheet = Source{[Item = "СПР_Менеджеры", Kind = "Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet, [PromoteAllScalars = true]),
    cols = Table.ColumnNames(#"Promoted Headers"),
    Step1 = if List.Contains(cols, "Column1") then Table.RenameColumns(#"Promoted Headers", {{"Column1", "Регион"}}) else #"Promoted Headers",
    cols2 = Table.ColumnNames(Step1),
    Step2 = if List.Contains(cols2, "Column2") then Table.RenameColumns(Step1, {{"Column2", "Менеджер"}}) else Step1
in
    Step2
