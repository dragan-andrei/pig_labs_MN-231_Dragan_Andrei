"""Concrete presenter implementing chart functionality."""

from __future__ import annotations

from typing import ClassVar, Dict, Optional, Tuple

from model.charting.chart_data_provider import IChartDataProvider
from model.charting.chart_series import ChartSeries
from model.exceptions import DomainError
from model.sorting.direction import SortDirection
from presenter.chart_presenter_interface import IChartPresenter
from view.chart_view_interface import IChartView
from view.chart_view_model import ChartViewModel
from view.theme import PurpleTheme


class ChartPresenter(IChartPresenter):
    """Requests chart series from the model and converts them into ``ChartViewModel``.

    Holds only presentation state (selected metric and sort direction);
    all data is computed by the model.
    """

    _CATEGORY_COLORS: ClassVar[Dict[str, str]] = {
        "PC": PurpleTheme.BADGE_PC_TEXT,
        "Laptop": PurpleTheme.BADGE_LAPTOP_TEXT,
        "Server": PurpleTheme.BADGE_SERVER_TEXT,
    }

    def __init__(self, model: IChartDataProvider, view: IChartView, default_metric: str = "cpu") -> None:
        """Initialize chart presenter.

        Args:
            model: Chart data provider abstraction.
            view: Chart view abstraction.
            default_metric: Metric displayed on first render.
        """
        self._model = model
        self._view = view
        self._metric_key = default_metric
        self._direction: Optional[SortDirection] = None

    @property
    def metric_key(self) -> str:
        """Return currently plotted metric key."""
        return self._metric_key

    @property
    def direction(self) -> Optional[SortDirection]:
        """Return current chart ordering."""
        return self._direction

    def initialize(self) -> None:
        """Populate metric selector and draw initial chart."""
        options = self._model.get_chart_metrics()
        if self._metric_key not in options and options:
            self._metric_key = next(iter(options))
        self._view.set_metric_options(options, self._metric_key)
        self._render()

    def handle_metric_selected(self, metric_key: str) -> None:
        """Switch metric and redraw."""
        self._metric_key = metric_key
        self._render()

    def handle_refresh_requested(self) -> None:
        """Reload data from the model and redraw."""
        self._render()

    def handle_sort_requested(self) -> None:
        """Cycle ordering None -> DESC -> ASC -> None and redraw."""
        if self._direction is None:
            self._direction = SortDirection.DESCENDING
        elif self._direction == SortDirection.DESCENDING:
            self._direction = SortDirection.ASCENDING
        else:
            self._direction = None
        self._render()

    def handle_close_requested(self) -> None:
        """Close the chart view."""
        self._view.close()

    def is_active(self) -> bool:
        """Return True while the chart view is open."""
        return self._view.is_open()

    def _render(self) -> None:
        """Fetch series from model, convert it and push to the view."""
        try:
            series = self._model.get_chart_series(self._metric_key, self._direction)
            self._view.render_chart(self._to_view_model(series))
            self._view.update_sort_state(self._direction.arrow if self._direction else None)
        except DomainError as err:
            self._view.show_error(f"Ошибка построения графика: {err}")

    def _to_view_model(self, series: ChartSeries) -> ChartViewModel:
        """Convert model series into presentation model.

        Args:
            series: Series produced by the model.

        Returns:
            Formatted ``ChartViewModel``.
        """
        colors = tuple(self._color_for(category) for category in series.categories)
        legend: Tuple[Tuple[str, str], ...] = tuple(
            (category, self._color_for(category)) for category in dict.fromkeys(series.categories)
        )
        order = f" | {series.direction.label}" if series.direction else " | Порядок каталога"
        summary = (
            f"{series.title}: устройств {len(series)}, "
            f"среднее {series.average:.1f} {series.unit}, макс. {series.maximum:g} {series.unit}{order}"
        )
        return ChartViewModel(
            title=f"{series.title} по устройствам",
            y_label=f"{series.title}, {series.unit}",
            labels=series.labels,
            values=series.values,
            bar_colors=colors,
            average=series.average,
            summary_text=summary,
            legend=legend,
            sort_arrow=series.direction.arrow if series.direction else None,
        )

    def _color_for(self, category: str) -> str:
        """Return bar color for a device category."""
        return self._CATEGORY_COLORS.get(category, PurpleTheme.CHART_DEFAULT_BAR)

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(metric={self._metric_key!r}, direction={self._direction!r})"
