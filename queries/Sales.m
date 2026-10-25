// Query name in Power Query: Sales
// Source tab id in the Google workbook (must match): Продажи
// Requires queries: Dates, Products, Customers, Managers, Shipping
let
    WebWorkbook = "https://docs.google.com/spreadsheets/d/1OObWrvhvYo5_PsLNpYN3ngbgXCMqc112TBvVsPGv9iY/export?format=xlsx",

    Source = Excel.Workbook(Web.Contents(WebWorkbook), null, true),
    Sheet = Source{[Item = "Продажи", Kind = "Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet, [PromoteAllScalars = true]),

    #"Added Revenue" = Table.AddColumn(
        #"Promoted Headers",
        "Revenue_num",
        each Number.FromText(Text.Replace(Text.Replace(Text.From([Выручка]), " ", ""), "#(00A0)", "")),
        type number
    ),
    #"Added Profit" = Table.AddColumn(
        #"Added Revenue",
        "Profit_num",
        each Number.FromText(Text.Replace(Text.Replace(Text.From([Прибыль]), " ", ""), "#(00A0)", "")),
        type number
    ),
    #"Removed Text Amounts" = Table.RemoveColumns(#"Added Profit", {"Выручка", "Прибыль"}),
    #"Renamed Core" = Table.RenameColumns(
        #"Removed Text Amounts",
        {
            {"Revenue_num", "Revenue"},
            {"Profit_num", "Profit"},
            {"Количество", "Quantity"},
            {"Приоритет", "Priority"},
            {"Метод доставки", "ShipMethod"},
            {"Покупатель", "Customer"},
            {"Регион", "Region"},
            {"Продукт", "Product"},
            {"Упаковка продукта", "Packaging"}
        },
        MissingField.Ignore
    ),
    #"Typed IDs" = Table.TransformColumnTypes(#"Renamed Core", {{"Order_ID", Int64.Type}, {"Quantity", Int64.Type}}),

    #"Merged Dates" = Table.NestedJoin(#"Typed IDs", {"Order_ID"}, Dates, {"Order_ID"}, "Dates", JoinKind.LeftOuter),
    #"Expanded Dates" = Table.ExpandTableColumn(#"Merged Dates", "Dates", {"Date"}, {"Date"}),

    #"Merged Products" = Table.NestedJoin(#"Expanded Dates", {"Product"}, Products, {"Product"}, "Products", JoinKind.LeftOuter),
    #"Expanded Products" = Table.ExpandTableColumn(
        #"Merged Products",
        "Products",
        {"Category", "Subcategory"},
        {"Category", "Subcategory"}
    ),

    #"Merged Customers" = Table.NestedJoin(#"Expanded Products", {"Customer"}, Customers, {"Customer"}, "Customers", JoinKind.LeftOuter),
    #"Expanded Customers" = Table.ExpandTableColumn(#"Merged Customers", "Customers", {"Segment"}, {"Segment"}),

    #"Merged Managers" = Table.NestedJoin(#"Expanded Customers", {"Region"}, Managers, {"Region"}, "Managers", JoinKind.LeftOuter),
    #"Expanded Managers" = Table.ExpandTableColumn(#"Merged Managers", "Managers", {"Manager"}, {"Manager"}),

    #"Merged Shipping" = Table.NestedJoin(#"Expanded Managers", {"ShipMethod"}, Shipping, {"ShipMethod"}, "Shipping", JoinKind.LeftOuter),
    #"Expanded Shipping" = Table.ExpandTableColumn(#"Merged Shipping", "Shipping", {"ShippingCost"}, {"ShippingCost"}),
    #"Removed Blank Rows" = Table.SelectRows(#"Expanded Shipping", each [Order_ID] <> null)
in
    #"Removed Blank Rows"
