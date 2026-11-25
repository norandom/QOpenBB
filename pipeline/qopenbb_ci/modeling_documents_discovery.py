"""Describe the Workspace records returned by the modeling discovery routes."""

from pydantic import JsonValue, NonNegativeInt, PositiveInt, RootModel
from qopenbb_data.modeling.contracts.common import Contract, Description, Identifier


class GridSize(Contract):
    w: PositiveInt
    h: PositiveInt


class WidgetParameter(Contract):
    paramName: Identifier
    label: Description
    type: Identifier
    show: bool
    optional: bool
    value: str | None


class ColumnDefinition(Contract):
    field: Identifier
    headerName: Description
    cellDataType: Identifier
    chartDataType: Identifier
    formatterFn: Identifier


class WidgetTable(Contract):
    showAll: bool
    columnsDefs: tuple[ColumnDefinition, ...]


class WidgetData(Contract):
    dataKey: Identifier
    table: WidgetTable


class WidgetDefinition(Contract):
    widgetId: Identifier
    name: Description
    description: Description
    category: Identifier
    type: Identifier
    endpoint: Identifier
    runButton: bool
    gridData: GridSize
    params: tuple[WidgetParameter, ...]
    data: WidgetData


class LayoutState(Contract):
    params: dict[str, JsonValue]


class LayoutItem(GridSize):
    i: Identifier
    x: NonNegativeInt
    y: NonNegativeInt
    state: LayoutState


class AppTab(Contract):
    id: Identifier
    name: Description
    layout: tuple[LayoutItem, ...]


class AppDefinition(Contract):
    name: Description
    description: Description
    allowCustomization: bool
    tabs: dict[str, AppTab]


class WidgetDiscovery(RootModel[dict[str, WidgetDefinition]]):
    pass


class AppDiscovery(RootModel[tuple[AppDefinition, ...]]):
    pass
