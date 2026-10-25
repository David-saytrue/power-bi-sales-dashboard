// Query name in Power Query: Shipping
// Source tab id in the Google workbook (must match): СПР_стоимость_доставки
let
    WebWorkbook = "https://docs.google.com/spreadsheets/d/1OObWrvhvYo5_PsLNpYN3ngbgXCMqc112TBvVsPGv9iY/export?format=xlsx",
    Source = Excel.Workbook(Web.Contents(WebWorkbook), null, true),
    Sheet = Source{[Item = "СПР_стоимость_доставки", Kind = "Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet, [PromoteAllScalars = true]),
    #"Renamed" = Table.RenameColumns(
        #"Promoted Headers",
        {{"Метод доставки", "ShipMethod"}, {"Стоимость доставки", "ShippingCost"}},
        MissingField.Ignore
    ),
    #"Filtered Rows" = Table.SelectRows(#"Renamed", each [ShipMethod] <> null and [ShipMethod] <> ""),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Rows", {{"ShippingCost", type number}})
in
    #"Changed Type"
