"""Declare the curated commodities versus technology research App."""

RENDERER_ID = "research_story"
TITLE = "Commodities versus Technology"
QUESTION = (
    "Did the selected commodity proxy outperform the selected technology proxy "
    "over the 63 trading sessions ending at the observation date?"
)


def default_state() -> dict:
    return {
        "version": 1,
        "selection": {
            "commodity_symbol": "DBC",
            "technology_symbol": "XLK",
            "observation_date": "2026-11-13",
        },
        "schedule": None,
        "cutoff": None,
        "run_refs": {"comparison": None, "regime": None},
        "charts": {
            "returns": {
                "input": {
                    "chart_type": "line",
                    "series": ["left_close", "right_close"],
                    "x_axis": "date",
                    "y_axis": "price_usd",
                },
                "result": {
                    "chart_type": "bar",
                    "series": ["left_momentum", "right_momentum"],
                    "x_axis": "proxy",
                    "y_axis": "percent",
                },
            },
            "risk": {
                "input": {
                    "chart_type": "line",
                    "series": ["left_daily_return", "right_daily_return"],
                    "x_axis": "date",
                    "y_axis": "percent",
                },
                "result": {
                    "chart_type": "bar",
                    "series": ["left_volatility", "right_volatility"],
                    "x_axis": "proxy",
                    "y_axis": "percent",
                },
            },
            "real_yields": {
                "input": {
                    "chart_type": "line",
                    "series": ["dfii10"],
                    "x_axis": "date",
                    "y_axis": "percent",
                },
                "result": {
                    "chart_type": "bar",
                    "series": ["change"],
                    "x_axis": "window",
                    "y_axis": "percentage_points",
                },
            },
        },
    }


def story_app(widgets: dict) -> dict:
    grid = {"w": 40, "h": 24}
    widgets[RENDERER_ID] = {
        "widgetId": RENDERER_ID,
        "type": RENDERER_ID,
        "name": TITLE,
        "description": "Compare proxy price returns, realized volatility and the change in real yields.",
        "category": "Research",
        "gridData": grid,
        "params": [],
    }
    layout = {
        "i": RENDERER_ID,
        "x": 0,
        "y": 0,
        **grid,
        "view_order": ["question", "returns", "risk", "real_yields", "conclusion"],
        "state": {"storage": {"researchStory": default_state()}},
    }
    return {
        "name": TITLE,
        "description": QUESTION,
        "allowCustomization": True,
        "tabs": {"Research": {"id": "Research", "name": "Research", "layout": [layout]}},
    }
