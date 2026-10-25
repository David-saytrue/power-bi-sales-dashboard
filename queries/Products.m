// Query name in Power Query: Products
// Source tab id in the Google workbook (must match): СПР_продукты
let
    WebWorkbook = "https://docs.google.com/spreadsheets/d/1OObWrvhvYo5_PsLNpYN3ngbgXCMqc112TBvVsPGv9iY/export?format=xlsx",
    Source = Excel.Workbook(Web.Contents(WebWorkbook), null, true),
    Sheet = Source{[Item = "СПР_продукты", Kind = "Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet, [PromoteAllScalars = true]),
    #"Renamed" = Table.RenameColumns(
        #"Promoted Headers",
        {
            {"Продукт", "Product"},
            {"Категория продукта", "Category"},
            {"Подкатегория продукта", "Subcategory"}
        },
        MissingField.Ignore
    )
in
    #"Renamed"
