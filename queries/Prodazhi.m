// Paste into query "Продажи" → Advanced Editor. Requires other 5 queries loaded (same workbook).
let
    WebWorkbook = "https://docs.google.com/spreadsheets/d/1OObWrvhvYo5_PsLNpYN3ngbgXCMqc112TBvVsPGv9iY/export?format=xlsx",

    Source = Excel.Workbook(Web.Contents(WebWorkbook), null, true),
    Sheet = Source{[Item = "Продажи", Kind = "Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Sheet, [PromoteAllScalars = true]),

    #"Added Revenue" = Table.AddColumn(
        #"Promoted Headers",
        "Выручка_num",
        each Number.FromText(Text.Replace(Text.Replace(Text.From([Выручка]), " ", ""), "#(00A0)", "")),
        type number
    ),
    #"Added Profit" = Table.AddColumn(
        #"Added Revenue",
        "Прибыль_num",
        each Number.FromText(Text.Replace(Text.Replace(Text.From([Прибыль]), " ", ""), "#(00A0)", "")),
        type number
    ),
    #"Removed Text Amounts" = Table.RemoveColumns(#"Added Profit", {"Выручка", "Прибыль"}),
    #"Renamed Amounts" = Table.RenameColumns(#"Removed Text Amounts", {{"Выручка_num", "Выручка"}, {"Прибыль_num", "Прибыль"}}),
    #"Typed IDs" = Table.TransformColumnTypes(#"Renamed Amounts", {{"Order_ID", Int64.Type}, {"Количество", Int64.Type}}),

    SprCustCols = Table.ColumnNames(#"СПР_покупатели"),
    CustKeySpr = if List.Contains(SprCustCols, "Покупатель") then "Покупатель" else "Column1",
    CustSegSpr =
        if List.Contains(SprCustCols, "Сегмент") then "Сегмент"
        else if List.Contains(SprCustCols, "Сегмент покупателя") then "Сегмент покупателя"
        else "Column2",
    SprMgrCols = Table.ColumnNames(#"СПР_Менеджеры"),
    MgrRegSpr = if List.Contains(SprMgrCols, "Регион") then "Регион" else "Column1",
    MgrNameSpr = if List.Contains(SprMgrCols, "Менеджер") then "Менеджер" else "Column2",

    #"Merged Dates" = Table.NestedJoin(#"Typed IDs", {"Order_ID"}, #"СПР_даты_заказа", {"Order_ID"}, "СПР_даты_заказа", JoinKind.LeftOuter),
    #"Expanded Dates" = Table.ExpandTableColumn(#"Merged Dates", "СПР_даты_заказа", {"Дата"}, {"Дата"}),

    #"Merged Products" = Table.NestedJoin(#"Expanded Dates", {"Продукт"}, #"СПР_продукты", {"Продукт"}, "СПР_продукты", JoinKind.LeftOuter),
    #"Expanded Products" = Table.ExpandTableColumn(
        #"Merged Products",
        "СПР_продукты",
        {"Категория продукта", "Подкатегория продукта"},
        {"Категория продукта", "Подкатегория продукта"}
    ),

    #"Merged Customers" = Table.NestedJoin(#"Expanded Products", {"Покупатель"}, #"СПР_покупатели", {CustKeySpr}, "СПР_покупатели", JoinKind.LeftOuter),
    #"Expanded Customers" = Table.ExpandTableColumn(#"Merged Customers", "СПР_покупатели", {CustSegSpr}, {"Сегмент"}),

    #"Merged Managers" = Table.NestedJoin(#"Expanded Customers", {"Регион"}, #"СПР_Менеджеры", {MgrRegSpr}, "СПР_Менеджеры", JoinKind.LeftOuter),
    #"Expanded Managers" = Table.ExpandTableColumn(#"Merged Managers", "СПР_Менеджеры", {MgrNameSpr}, {"Менеджер"}),

    #"Merged Shipping" = Table.NestedJoin(#"Expanded Managers", {"Метод доставки"}, #"СПР_стоимость_доставки", {"Метод доставки"}, "СПР_стоимость_доставки", JoinKind.LeftOuter),
    #"Expanded Shipping" = Table.ExpandTableColumn(#"Merged Shipping", "СПР_стоимость_доставки", {"Стоимость доставки"}, {"Стоимость доставки"}),
    #"Removed Blank Rows" = Table.SelectRows(#"Expanded Shipping", each [Order_ID] <> null)
in
    #"Removed Blank Rows"
