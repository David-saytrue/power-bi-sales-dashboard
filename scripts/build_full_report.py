"""Build a complete TZ dashboard on top of the working test_task_1.pbix.

Keeps DataModel bytes untouched. Drops SecurityBindings so Desktop can open
the edited report (same trick as test_task_1_unsigned.pbix).
"""
from __future__ import annotations

import json
import os
import shutil
import zipfile

SCHEMA = (
    "https://developer.microsoft.com/json-schemas/fabric/item/report/"
    "definition/visualContainer/2.14.0/schema.json"
)
TABLE = "Продажи"
SRC_CANDIDATES = [
    r"c:\prep_for_job\power-bi\test_task_1.pbix",
    r"c:\Users\Admin\OneDrive\Рабочий стол\test_task_1.pbix",
]
OUT_EN = r"c:\prep_for_job\power-bi\sales-dashboard-en.pbix"
PAGE = "e0e0604a4d546abb9599"

LABELS_EN = {
    "page": "Sales",
    "hero": "Sales dashboard",
    "kpi_revenue": "Revenue",
    "kpi_profit": "Profit",
    "kpi_logistics": "Logistics",
    "kpi_margin": "Profitability",
    "kpi_customers": "Active customers",
    "kpi_aov": "Avg. order value",
    "line": "Revenue and profit over time",
    "bar": "Revenue by segment",
    "matrix": "Product hierarchy (category → product)",
    "map": "Revenue by region",
    "managers": "Managers: loss-making orders",
    "abc": "ABC: products by revenue (A ≤80%, B ≤95%, C rest)",
}
CONTENT_TYPES_OVERRIDE = (
    '<Override PartName="/SecurityBindings" ContentType="" />'
)


def lit(value: str) -> dict:
    return {"expr": {"Literal": {"Value": value}}}


def solid(hex_color: str) -> dict:
    return {"solid": {"color": lit(f"'{hex_color}'")}}


def col(name: str) -> dict:
    return {
        "field": {
            "Column": {
                "Expression": {"SourceRef": {"Entity": TABLE}},
                "Property": name,
            }
        },
        "queryRef": f"{TABLE}.{name}",
        "nativeQueryRef": name,
    }


def meas(name: str) -> dict:
    return {
        "field": {
            "Measure": {
                "Expression": {"SourceRef": {"Entity": TABLE}},
                "Property": name,
            }
        },
        "queryRef": f"{TABLE}.{name}",
        "nativeQueryRef": name,
    }


def meas_field(name: str) -> dict:
    return {
        "Measure": {
            "Expression": {"SourceRef": {"Entity": TABLE}},
            "Property": name,
        }
    }


def container(title: str | None, show_title: bool = True) -> dict:
    title_props = {
        "show": lit("true" if show_title and title else "false"),
        "titleWrap": lit("true"),
        "fontSize": lit("'12'"),
        "fontColor": solid("#1F2937"),
    }
    if title:
        title_props["text"] = lit(f"'{title}'")
    return {
        "title": [{"properties": title_props}],
        "background": [
            {
                "properties": {
                    "show": lit("true"),
                    "color": solid("#FFFFFF"),
                    "transparency": lit("0D"),
                }
            }
        ],
        "border": [
            {
                "properties": {
                    "show": lit("true"),
                    "color": solid("#E5E7EB"),
                    "radius": lit("8D"),
                    "width": lit("1D"),
                }
            }
        ],
        "padding": [
            {
                "properties": {
                    "top": lit("4D"),
                    "bottom": lit("4D"),
                    "left": lit("4D"),
                    "right": lit("4D"),
                }
            }
        ],
    }


def visual_base(
    name: str,
    visual_type: str,
    x: float,
    y: float,
    w: float,
    h: float,
    z: int,
    query_state: dict,
    title: str | None,
    extra_visual: dict | None = None,
    sort: dict | None = None,
    objects: dict | None = None,
    show_title: bool = True,
) -> dict:
    query: dict = {"queryState": query_state}
    if sort:
        query["sortDefinition"] = sort
    visual = {
        "visualType": visual_type,
        "query": query,
        "objects": objects or {},
        "visualContainerObjects": container(title, show_title=show_title),
        "drillFilterOtherVisuals": True,
    }
    if extra_visual:
        visual.update(extra_visual)
    return {
        "$schema": SCHEMA,
        "name": name,
        "position": {
            "x": x,
            "y": y,
            "z": z,
            "height": h,
            "width": w,
            "tabOrder": z,
        },
        "visual": visual,
    }


def card(
    name: str,
    measure: str,
    title: str,
    color: str,
    x: float,
    z: int,
    units: str | None,
    precision: str | None,
) -> dict:
    value_props = {
        "fontSize": lit("30D"),
        "bold": lit("true"),
        "color": solid(color),
    }
    if units is not None:
        value_props["labelDisplayUnits"] = lit(units)
    if precision is not None:
        value_props["labelPrecision"] = lit(precision)
    box = container(title, show_title=True)
    box["title"][0]["properties"]["fontSize"] = lit("'11'")
    box["title"][0]["properties"]["fontColor"] = solid("#6B7280")
    box["padding"] = [
        {
            "properties": {
                "top": lit("10D"),
                "bottom": lit("8D"),
                "left": lit("10D"),
                "right": lit("10D"),
            }
        }
    ]
    return {
        "$schema": SCHEMA,
        "name": name,
        "position": {
            "x": x,
            "y": 72,
            "z": z,
            "height": 108,
            "width": 298,
            "tabOrder": z,
        },
        "visual": {
            "visualType": "cardVisual",
            "query": {
                "queryState": {"Data": {"projections": [meas(measure)]}},
                "sortDefinition": {
                    "sort": [{"field": meas_field(measure), "direction": "Descending"}],
                    "isDefaultSort": True,
                },
            },
            "objects": {
                "layout": [{"properties": {"alignment": lit("'middle'")}}],
                "value": [
                    {
                        "properties": value_props,
                        "selector": {"metadata": f"{TABLE}.{measure}"},
                    }
                ],
                "label": [
                    {
                        "properties": {
                            "show": lit("false"),
                            "position": lit("'belowValue'"),
                        },
                        "selector": {"metadata": f"{TABLE}.{measure}"},
                    }
                ],
            },
            "visualContainerObjects": box,
            "drillFilterOtherVisuals": True,
        },
        "filterConfig": {
            "filters": [
                {
                    "name": name[-16:],
                    "field": meas_field(measure),
                    "type": "Advanced",
                }
            ]
        },
    }


def title_box(text: str) -> dict:
    return {
        "$schema": SCHEMA,
        "name": "txt001title000000001",
        "position": {
            "x": 24,
            "y": 12,
            "z": 0,
            "height": 48,
            "width": 900,
            "tabOrder": 0,
        },
        "visual": {
            "visualType": "textbox",
            "objects": {
                "general": [
                    {
                        "properties": {
                            "paragraphs": [
                                {
                                    "horizontalTextAlignment": "left",
                                    "textRuns": [
                                        {
                                            "value": text,
                                            "textStyle": {
                                                "fontWeight": "bold",
                                                "fontSize": "20pt",
                                                "color": "#111827",
                                            },
                                        }
                                    ],
                                }
                            ]
                        }
                    }
                ]
            },
            "visualContainerObjects": {
                "background": [
                    {
                        "properties": {
                            "show": lit("false"),
                            "transparency": lit("100D"),
                        }
                    }
                ],
                "border": [{"properties": {"show": lit("false")}}],
            },
        },
    }


def slicer(name: str, field: str, x: float, z: int, mode: str) -> dict:
    return visual_base(
        name,
        "slicer",
        x,
        16,
        250,
        48,
        z,
        {"Values": {"projections": [col(field)]}},
        None,
        objects={"data": [{"properties": {"mode": lit(f"'{mode}'")}}]},
        show_title=False,
    )


def build_visuals(labels: dict[str, str]) -> dict[str, dict]:
    cards = {
        "a7c570921e65c9682a8c": card(
            "a7c570921e65c9682a8c",
            "Сумма выручки",
            labels["kpi_revenue"],
            "#111827",
            24,
            1000,
            "1000000D",
            "1L",
        ),
        "d39922623370abc7c1c6": card(
            "d39922623370abc7c1c6",
            "Сумма прибыли",
            labels["kpi_profit"],
            "#047857",
            338,
            2000,
            "1000D",
            "1L",
        ),
        "0cda3581b0501f0e650d": card(
            "0cda3581b0501f0e650d",
            "Затраты на логистику",
            labels["kpi_logistics"],
            "#B45309",
            652,
            3000,
            "1000D",
            "2L",
        ),
        "576f5447dbb32e9d757e": card(
            "576f5447dbb32e9d757e",
            "Рентабельность",
            labels["kpi_margin"],
            "#6D28D9",
            966,
            4000,
            "1D",
            "1L",
        ),
        "b810ebe5ad7db1643f6e": card(
            "b810ebe5ad7db1643f6e",
            "АКБ",
            labels["kpi_customers"],
            "#1D4ED8",
            1280,
            5000,
            "1D",
            "0L",
        ),
        "f844233cfcdb620ccc0e": card(
            "f844233cfcdb620ccc0e",
            "Средний чек",
            labels["kpi_aov"],
            "#0F766E",
            1594,
            6000,
            "1000D",
            "2L",
        ),
    }

    line = visual_base(
        "line001dynamics00001",
        "lineChart",
        24,
        192,
        1100,
        360,
        7000,
        {
            "Category": {"projections": [col("Дата")]},
            "Y": {
                "projections": [meas("Сумма выручки"), meas("Сумма прибыли")]
            },
        },
        labels["line"],
        sort={
            "sort": [
                {
                    "field": {
                        "Column": {
                            "Expression": {"SourceRef": {"Entity": TABLE}},
                            "Property": "Дата",
                        }
                    },
                    "direction": "Ascending",
                }
            ],
            "isDefaultSort": True,
        },
        objects={
            "legend": [
                {
                    "properties": {
                        "show": lit("true"),
                        "position": lit("'Top'"),
                    }
                }
            ]
        },
    )

    bar = visual_base(
        "bar001segment0000001",
        "clusteredBarChart",
        1140,
        192,
        756,
        360,
        8000,
        {
            "Category": {"projections": [col("Сегмент")]},
            "Y": {"projections": [meas("Сумма выручки")]},
        },
        labels["bar"],
        sort={
            "sort": [
                {"field": meas_field("Сумма выручки"), "direction": "Descending"}
            ],
            "isDefaultSort": True,
        },
    )

    matrix = visual_base(
        "mtx001nomenklatura01",
        "pivotTable",
        24,
        568,
        620,
        488,
        9000,
        {
            "Rows": {
                "projections": [
                    col("Категория продукта"),
                    col("Подкатегория продукта"),
                    col("Продукт"),
                ]
            },
            "Values": {
                "projections": [meas("Сумма выручки"), meas("Сумма прибыли")]
            },
        },
        labels["matrix"],
        extra_visual={
            "expansionStates": [
                {
                    "roles": ["Rows"],
                    "levels": [
                        {
                            "queryRefs": [f"{TABLE}.Категория продукта"],
                            "identityKeys": [
                                {
                                    "Column": {
                                        "Expression": {
                                            "SourceRef": {"Entity": TABLE}
                                        },
                                        "Property": "Категория продукта",
                                    }
                                }
                            ],
                            "isPinned": True,
                        },
                        {
                            "queryRefs": [f"{TABLE}.Подкатегория продукта"],
                            "isCollapsed": True,
                            "identityKeys": [
                                {
                                    "Column": {
                                        "Expression": {
                                            "SourceRef": {"Entity": TABLE}
                                        },
                                        "Property": "Подкатегория продукта",
                                    }
                                }
                            ],
                            "isPinned": True,
                        },
                        {
                            "queryRefs": [f"{TABLE}.Продукт"],
                            "isCollapsed": True,
                            "identityKeys": [
                                {
                                    "Column": {
                                        "Expression": {
                                            "SourceRef": {"Entity": TABLE}
                                        },
                                        "Property": "Продукт",
                                    }
                                }
                            ],
                            "isPinned": True,
                        },
                    ],
                    "root": {},
                }
            ]
        },
        objects={
            "columnHeaders": [
                {
                    "properties": {
                        "autoSizeColumnWidth": lit("true"),
                        "columnAdjustment": lit("'growToFit'"),
                    }
                }
            ]
        },
    )

    fmap = visual_base(
        "map001region00000001",
        "filledMap",
        660,
        568,
        520,
        488,
        10000,
        {
            "Location": {"projections": [col("Регион")]},
            "Values": {"projections": [meas("Сумма выручки")]},
        },
        labels["map"],
    )

    managers = visual_base(
        "tbl001managers000001",
        "tableEx",
        1196,
        568,
        700,
        232,
        11000,
        {
            "Values": {
                "projections": [
                    col("Менеджер"),
                    meas("Заказы убыт"),
                    meas("Сумма прибыли"),
                ]
            }
        },
        labels["managers"],
        sort={
            "sort": [
                {"field": meas_field("Заказы убыт"), "direction": "Descending"}
            ],
            "isDefaultSort": True,
        },
        objects={
            "columnHeaders": [
                {
                    "properties": {
                        "autoSizeColumnWidth": lit("true"),
                        "columnAdjustment": lit("'growToFit'"),
                    }
                }
            ]
        },
    )

    abc = visual_base(
        "tbl002abcproducts001",
        "tableEx",
        1196,
        816,
        700,
        240,
        12000,
        {
            "Values": {
                "projections": [
                    col("Продукт"),
                    meas("Сумма выручки"),
                    meas("Сумма прибыли"),
                ]
            }
        },
        labels["abc"],
        sort={
            "sort": [
                {"field": meas_field("Сумма выручки"), "direction": "Descending"}
            ],
            "isDefaultSort": True,
        },
        objects={
            "columnHeaders": [
                {
                    "properties": {
                        "autoSizeColumnWidth": lit("true"),
                        "columnAdjustment": lit("'growToFit'"),
                    }
                }
            ]
        },
    )

    visuals = {
        **cards,
        "txt001title000000001": title_box(labels["hero"]),
        "slc001date0000000001": slicer(
            "slc001date0000000001", "Дата", 1100, 13000, "Between"
        ),
        "slc002region00000001": slicer(
            "slc002region00000001", "Регион", 1366, 14000, "Dropdown"
        ),
        "slc003segment0000001": slicer(
            "slc003segment0000001", "Сегмент", 1632, 15000, "Dropdown"
        ),
        "line001dynamics00001": line,
        "bar001segment0000001": bar,
        "mtx001nomenklatura01": matrix,
        "map001region00000001": fmap,
        "tbl001managers000001": managers,
        "tbl002abcproducts001": abc,
    }
    return visuals


def page_json(display_name: str) -> dict:
    return {
        "$schema": (
            "https://developer.microsoft.com/json-schemas/fabric/item/"
            "report/definition/page/2.1.0/schema.json"
        ),
        "name": PAGE,
        "displayName": display_name,
        "displayOption": "FitToPage",
        "height": 1080,
        "width": 1920,
        "objects": {
            "background": [
                {
                    "properties": {
                        "color": solid("#F3F4F6"),
                        "transparency": lit("0D"),
                    }
                }
            ]
        },
    }


def find_src() -> str:
    for path in SRC_CANDIDATES:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError("test_task_1.pbix not found")


def dump(obj: dict) -> bytes:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def pack(src: str, dst: str, visuals: dict[str, dict], page_name: str) -> None:
    visual_prefix = f"Report/definition/pages/{PAGE}/visuals/"
    page_path = f"Report/definition/pages/{PAGE}/page.json"
    with zipfile.ZipFile(src, "r") as zin, zipfile.ZipFile(dst, "w") as zout:
        written = set()
        for info in zin.infolist():
            name = info.filename.replace("\\", "/")
            if name == "SecurityBindings":
                continue
            if name.startswith(visual_prefix) and name.endswith("/visual.json"):
                continue
            data = zin.read(info.filename)
            if name == "[Content_Types].xml":
                xml = data.decode("utf-8").replace(CONTENT_TYPES_OVERRIDE, "")
                data = xml.encode("utf-8")
            elif name == page_path:
                data = dump(page_json(page_name))
            zi = zipfile.ZipInfo(filename=info.filename, date_time=info.date_time)
            zi.compress_type = info.compress_type
            zi.external_attr = info.external_attr
            zout.writestr(zi, data, compress_type=info.compress_type)
            written.add(name)

        for vid, payload in visuals.items():
            path = f"{visual_prefix}{vid}/visual.json"
            zi = zipfile.ZipInfo(filename=path)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, dump(payload), compress_type=zipfile.ZIP_DEFLATED)


def copy_to_desktop(path: str) -> str | None:
    home = os.path.expanduser("~")
    onedrive = os.path.join(home, "OneDrive")
    if not os.path.isdir(onedrive):
        return None
    for item in os.listdir(onedrive):
        full = os.path.join(onedrive, item)
        if os.path.isdir(full) and ("стол" in item.lower() or item.lower() == "desktop"):
            dest = os.path.join(full, os.path.basename(path))
            shutil.copy2(path, dest)
            return dest
    return None


def main() -> None:
    src = find_src()
    visuals = build_visuals(LABELS_EN)
    pack(src, OUT_EN, visuals, LABELS_EN["page"])
    print("ok")
    print("en_bytes", os.path.getsize(OUT_EN))
    print("visuals", len(visuals))


if __name__ == "__main__":
    main()
