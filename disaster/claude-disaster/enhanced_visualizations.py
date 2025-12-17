#!/usr/bin/env python3
"""
Enhanced Visualizations for Emergency Preparedness System
Provides interactive charts with multiple backend support (Plotly, Matplotlib, ASCII)
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

# Try to import visualization libraries
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logger.info("Plotly not available")

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    logger.info("Matplotlib not available")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


@dataclass
class ChartData:
    """Container for chart data"""
    title: str
    labels: List[str]
    values: List[float]
    colors: Optional[List[str]] = None
    secondary_values: Optional[List[float]] = None
    chart_type: str = "bar"
    metadata: Dict[str, Any] = None


class ChartRenderer(ABC):
    """Abstract base class for chart renderers"""

    @abstractmethod
    def render_bar_chart(self, data: ChartData, output_path: Optional[str] = None) -> str:
        """Render a bar chart"""
        pass

    @abstractmethod
    def render_pie_chart(self, data: ChartData, output_path: Optional[str] = None) -> str:
        """Render a pie chart"""
        pass

    @abstractmethod
    def render_line_chart(self, data: ChartData, output_path: Optional[str] = None) -> str:
        """Render a line chart"""
        pass

    @abstractmethod
    def render_heatmap(self, data: List[List[float]], labels: Tuple[List[str], List[str]],
                      title: str, output_path: Optional[str] = None) -> str:
        """Render a heatmap"""
        pass

    @abstractmethod
    def render_gauge(self, value: float, max_value: float, title: str,
                    thresholds: Optional[List[Tuple[float, str]]] = None,
                    output_path: Optional[str] = None) -> str:
        """Render a gauge chart"""
        pass


class ASCIIRenderer(ChartRenderer):
    """ASCII-based chart renderer (always available fallback)"""

    def __init__(self, width: int = 60, height: int = 20):
        self.width = width
        self.height = height

    def render_bar_chart(self, data: ChartData, output_path: Optional[str] = None) -> str:
        """Render ASCII bar chart"""
        lines = []
        lines.append(f"\n{'='*self.width}")
        lines.append(f" {data.title}")
        lines.append(f"{'='*self.width}")

        if not data.values:
            return "\n".join(lines) + "\n  No data available\n"

        max_val = max(data.values) if data.values else 1
        bar_width = self.width - 20  # Leave room for labels

        for label, value in zip(data.labels, data.values):
            bar_length = int((value / max_val) * bar_width) if max_val > 0 else 0
            bar = '█' * bar_length
            lines.append(f"  {label[:12]:12} |{bar} {value:.1f}")

        lines.append(f"{'='*self.width}\n")

        result = "\n".join(lines)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(result)

        return result

    def render_pie_chart(self, data: ChartData, output_path: Optional[str] = None) -> str:
        """Render ASCII pie representation"""
        lines = []
        lines.append(f"\n{'='*self.width}")
        lines.append(f" {data.title}")
        lines.append(f"{'='*self.width}")

        total = sum(data.values) if data.values else 1
        symbols = ['█', '▓', '▒', '░', '▪', '▫', '◆', '◇']

        for i, (label, value) in enumerate(zip(data.labels, data.values)):
            pct = (value / total * 100) if total > 0 else 0
            sym = symbols[i % len(symbols)]
            bar_length = int(pct / 100 * 30)
            bar = sym * bar_length
            lines.append(f"  {sym} {label[:15]:15} {bar} {pct:.1f}%")

        lines.append(f"{'='*self.width}\n")

        result = "\n".join(lines)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(result)

        return result

    def render_line_chart(self, data: ChartData, output_path: Optional[str] = None) -> str:
        """Render ASCII line chart"""
        lines = []
        lines.append(f"\n{'='*self.width}")
        lines.append(f" {data.title}")
        lines.append(f"{'='*self.width}")

        if not data.values:
            return "\n".join(lines) + "\n  No data available\n"

        min_val = min(data.values)
        max_val = max(data.values)
        range_val = max_val - min_val if max_val != min_val else 1

        chart_height = 10
        chart_width = min(len(data.values), self.width - 10)

        # Build chart grid
        grid = [[' ' for _ in range(chart_width)] for _ in range(chart_height)]

        # Plot points
        step = max(1, len(data.values) // chart_width)
        for x in range(chart_width):
            idx = min(x * step, len(data.values) - 1)
            y = int((data.values[idx] - min_val) / range_val * (chart_height - 1))
            y = chart_height - 1 - y  # Flip Y axis
            grid[y][x] = '●'

        # Draw grid
        for row in grid:
            lines.append(f"  {''.join(row)}")

        # X-axis labels
        if data.labels and len(data.labels) >= 2:
            lines.append(f"  {data.labels[0][:10]:10}{'':>{chart_width-20}}{data.labels[-1][-10:]:>10}")

        lines.append(f"  Min: {min_val:.1f}  Max: {max_val:.1f}")
        lines.append(f"{'='*self.width}\n")

        result = "\n".join(lines)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(result)

        return result

    def render_heatmap(self, data: List[List[float]], labels: Tuple[List[str], List[str]],
                      title: str, output_path: Optional[str] = None) -> str:
        """Render ASCII heatmap"""
        lines = []
        lines.append(f"\n{'='*self.width}")
        lines.append(f" {title}")
        lines.append(f"{'='*self.width}")

        if not data or not data[0]:
            return "\n".join(lines) + "\n  No data available\n"

        # Normalize data for intensity mapping
        all_vals = [v for row in data for v in row]
        min_val = min(all_vals)
        max_val = max(all_vals)
        range_val = max_val - min_val if max_val != min_val else 1

        intensity_chars = ' ░▒▓█'

        row_labels, col_labels = labels

        # Header
        header = "        "
        for col in col_labels[:8]:
            header += f"{col[:5]:^6}"
        lines.append(header)

        # Data rows
        for i, row in enumerate(data[:12]):
            row_label = row_labels[i][:6] if i < len(row_labels) else f"R{i}"
            line = f"  {row_label:6}"

            for val in row[:8]:
                intensity = int((val - min_val) / range_val * (len(intensity_chars) - 1))
                char = intensity_chars[intensity]
                line += f"  {char}{char}  "

            lines.append(line)

        lines.append(f"\n  Legend: {' '.join(intensity_chars)} (low → high)")
        lines.append(f"{'='*self.width}\n")

        result = "\n".join(lines)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(result)

        return result

    def render_gauge(self, value: float, max_value: float, title: str,
                    thresholds: Optional[List[Tuple[float, str]]] = None,
                    output_path: Optional[str] = None) -> str:
        """Render ASCII gauge"""
        lines = []
        lines.append(f"\n{'='*self.width}")
        lines.append(f" {title}")
        lines.append(f"{'='*self.width}")

        pct = min(100, max(0, value / max_value * 100)) if max_value > 0 else 0
        bar_width = 40
        filled = int(pct / 100 * bar_width)

        # Determine color/status
        status = "OK"
        if thresholds:
            for threshold, label in sorted(thresholds, reverse=True):
                if pct >= threshold:
                    status = label
                    break

        # Draw gauge
        gauge = '█' * filled + '░' * (bar_width - filled)
        lines.append(f"\n  [{gauge}]")
        lines.append(f"  {' '*((bar_width-10)//2)}{pct:.1f}% / {max_value:.0f}")
        lines.append(f"  Status: {status}")
        lines.append(f"\n{'='*self.width}\n")

        result = "\n".join(lines)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(result)

        return result


class PlotlyRenderer(ChartRenderer):
    """Plotly-based interactive chart renderer"""

    def __init__(self, theme: str = "plotly_white"):
        if not PLOTLY_AVAILABLE:
            raise ImportError("Plotly is not available")
        self.theme = theme

    def render_bar_chart(self, data: ChartData, output_path: Optional[str] = None) -> str:
        """Render interactive bar chart"""
        colors = data.colors or px.colors.qualitative.Set2

        fig = go.Figure(data=[
            go.Bar(
                x=data.labels,
                y=data.values,
                marker_color=colors[:len(data.values)],
                text=[f"{v:.1f}" for v in data.values],
                textposition='auto'
            )
        ])

        if data.secondary_values:
            fig.add_trace(go.Bar(
                x=data.labels,
                y=data.secondary_values,
                marker_color='rgba(100, 100, 100, 0.5)',
                name='Secondary'
            ))

        fig.update_layout(
            title=data.title,
            template=self.theme,
            xaxis_title="Category",
            yaxis_title="Value",
            showlegend=bool(data.secondary_values)
        )

        if output_path:
            fig.write_html(output_path)
            return output_path
        else:
            return fig.to_html(include_plotlyjs='cdn')

    def render_pie_chart(self, data: ChartData, output_path: Optional[str] = None) -> str:
        """Render interactive pie chart"""
        colors = data.colors or px.colors.qualitative.Set2

        fig = go.Figure(data=[
            go.Pie(
                labels=data.labels,
                values=data.values,
                marker_colors=colors[:len(data.values)],
                textinfo='label+percent',
                hole=0.3  # Donut style
            )
        ])

        fig.update_layout(
            title=data.title,
            template=self.theme
        )

        if output_path:
            fig.write_html(output_path)
            return output_path
        else:
            return fig.to_html(include_plotlyjs='cdn')

    def render_line_chart(self, data: ChartData, output_path: Optional[str] = None) -> str:
        """Render interactive line chart"""
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=data.labels,
            y=data.values,
            mode='lines+markers',
            name='Primary',
            line=dict(width=2),
            marker=dict(size=8)
        ))

        if data.secondary_values:
            fig.add_trace(go.Scatter(
                x=data.labels,
                y=data.secondary_values,
                mode='lines+markers',
                name='Secondary',
                line=dict(width=2, dash='dash')
            ))

        fig.update_layout(
            title=data.title,
            template=self.theme,
            xaxis_title="Time/Category",
            yaxis_title="Value",
            hovermode='x unified'
        )

        if output_path:
            fig.write_html(output_path)
            return output_path
        else:
            return fig.to_html(include_plotlyjs='cdn')

    def render_heatmap(self, data: List[List[float]], labels: Tuple[List[str], List[str]],
                      title: str, output_path: Optional[str] = None) -> str:
        """Render interactive heatmap"""
        row_labels, col_labels = labels

        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=col_labels,
            y=row_labels,
            colorscale='RdYlGn',
            reversescale=True,
            text=[[f"{v:.1f}" for v in row] for row in data],
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))

        fig.update_layout(
            title=title,
            template=self.theme,
            xaxis_title="",
            yaxis_title=""
        )

        if output_path:
            fig.write_html(output_path)
            return output_path
        else:
            return fig.to_html(include_plotlyjs='cdn')

    def render_gauge(self, value: float, max_value: float, title: str,
                    thresholds: Optional[List[Tuple[float, str]]] = None,
                    output_path: Optional[str] = None) -> str:
        """Render interactive gauge"""
        pct = min(100, max(0, value / max_value * 100)) if max_value > 0 else 0

        # Define color ranges
        steps = [
            {'range': [0, 30], 'color': "#ff4444"},
            {'range': [30, 60], 'color': "#ffaa00"},
            {'range': [60, 80], 'color': "#88cc00"},
            {'range': [80, 100], 'color': "#00cc44"}
        ]

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pct,
            title={'text': title},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#333"},
                'steps': steps,
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': pct
                }
            }
        ))

        fig.update_layout(template=self.theme)

        if output_path:
            fig.write_html(output_path)
            return output_path
        else:
            return fig.to_html(include_plotlyjs='cdn')


class MatplotlibRenderer(ChartRenderer):
    """Matplotlib-based chart renderer"""

    def __init__(self, style: str = "seaborn-v0_8-whitegrid"):
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("Matplotlib is not available")
        try:
            plt.style.use(style)
        except Exception:
            pass  # Use default style

    def render_bar_chart(self, data: ChartData, output_path: Optional[str] = None) -> str:
        """Render bar chart"""
        fig, ax = plt.subplots(figsize=(10, 6))

        colors = data.colors or plt.cm.Set2.colors
        bars = ax.bar(data.labels, data.values, color=colors[:len(data.values)])

        ax.set_title(data.title)
        ax.set_xlabel("Category")
        ax.set_ylabel("Value")

        # Add value labels
        for bar, val in zip(bars, data.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                   f'{val:.1f}', ha='center', va='bottom')

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            # Return base64 encoded image
            import io
            import base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"

    def render_pie_chart(self, data: ChartData, output_path: Optional[str] = None) -> str:
        """Render pie chart"""
        fig, ax = plt.subplots(figsize=(10, 8))

        colors = data.colors or plt.cm.Set2.colors
        wedges, texts, autotexts = ax.pie(
            data.values,
            labels=data.labels,
            colors=colors[:len(data.values)],
            autopct='%1.1f%%',
            startangle=90
        )

        ax.set_title(data.title)
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            import io
            import base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"

    def render_line_chart(self, data: ChartData, output_path: Optional[str] = None) -> str:
        """Render line chart"""
        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(data.labels, data.values, 'o-', linewidth=2, markersize=8, label='Primary')

        if data.secondary_values:
            ax.plot(data.labels, data.secondary_values, 's--', linewidth=2,
                   markersize=6, label='Secondary')
            ax.legend()

        ax.set_title(data.title)
        ax.set_xlabel("Time/Category")
        ax.set_ylabel("Value")

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            import io
            import base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"

    def render_heatmap(self, data: List[List[float]], labels: Tuple[List[str], List[str]],
                      title: str, output_path: Optional[str] = None) -> str:
        """Render heatmap"""
        import numpy as np

        fig, ax = plt.subplots(figsize=(12, 8))

        row_labels, col_labels = labels
        im = ax.imshow(data, cmap='RdYlGn_r', aspect='auto')

        ax.set_xticks(range(len(col_labels)))
        ax.set_yticks(range(len(row_labels)))
        ax.set_xticklabels(col_labels)
        ax.set_yticklabels(row_labels)

        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

        # Add colorbar
        cbar = ax.figure.colorbar(im, ax=ax)

        # Add text annotations
        for i in range(len(row_labels)):
            for j in range(len(col_labels)):
                if i < len(data) and j < len(data[i]):
                    ax.text(j, i, f'{data[i][j]:.1f}',
                           ha='center', va='center', fontsize=8)

        ax.set_title(title)
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            import io
            import base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"

    def render_gauge(self, value: float, max_value: float, title: str,
                    thresholds: Optional[List[Tuple[float, str]]] = None,
                    output_path: Optional[str] = None) -> str:
        """Render gauge (as a horizontal bar for matplotlib)"""
        fig, ax = plt.subplots(figsize=(10, 3))

        pct = min(100, max(0, value / max_value * 100)) if max_value > 0 else 0

        # Background
        ax.barh(0, 100, color='#e0e0e0', height=0.5)

        # Value bar with color based on percentage
        if pct < 30:
            color = '#ff4444'
        elif pct < 60:
            color = '#ffaa00'
        elif pct < 80:
            color = '#88cc00'
        else:
            color = '#00cc44'

        ax.barh(0, pct, color=color, height=0.5)

        # Add markers
        ax.axvline(x=30, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=60, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=80, color='gray', linestyle='--', alpha=0.5)

        ax.set_xlim(0, 100)
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([])
        ax.set_xlabel('Percentage')
        ax.set_title(f'{title}: {pct:.1f}%')

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            return output_path
        else:
            import io
            import base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"


class VisualizationManager:
    """
    High-level visualization manager that selects the best available renderer
    """

    def __init__(self, preferred_backend: str = "auto",
                output_dir: str = "visualizations"):
        """
        Initialize visualization manager

        Args:
            preferred_backend: 'plotly', 'matplotlib', 'ascii', or 'auto'
            output_dir: Directory for saving visualizations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Select renderer
        self.renderer = self._select_renderer(preferred_backend)
        logger.info(f"Using {self.renderer.__class__.__name__} for visualizations")

    def _select_renderer(self, preferred: str) -> ChartRenderer:
        """Select the best available renderer"""
        if preferred == "plotly" and PLOTLY_AVAILABLE:
            return PlotlyRenderer()
        elif preferred == "matplotlib" and MATPLOTLIB_AVAILABLE:
            return MatplotlibRenderer()
        elif preferred == "ascii":
            return ASCIIRenderer()
        elif preferred == "auto":
            if PLOTLY_AVAILABLE:
                return PlotlyRenderer()
            elif MATPLOTLIB_AVAILABLE:
                return MatplotlibRenderer()
            else:
                return ASCIIRenderer()
        else:
            return ASCIIRenderer()

    def create_risk_dashboard(self, risk_data: Dict[str, float],
                            output_file: str = "risk_dashboard") -> str:
        """
        Create a comprehensive risk visualization dashboard

        Args:
            risk_data: Dictionary mapping risk categories to scores (0-100)
            output_file: Base name for output file

        Returns:
            Path to generated visualization or HTML string
        """
        labels = list(risk_data.keys())
        values = list(risk_data.values())

        data = ChartData(
            title="Emergency Risk Assessment Dashboard",
            labels=labels,
            values=values,
            chart_type="bar"
        )

        output_path = self.output_dir / f"{output_file}.html"
        if isinstance(self.renderer, ASCIIRenderer):
            output_path = self.output_dir / f"{output_file}.txt"

        return self.renderer.render_bar_chart(data, str(output_path))

    def create_supply_status(self, supplies: Dict[str, Dict[str, float]],
                           output_file: str = "supply_status") -> str:
        """
        Create supply inventory visualization

        Args:
            supplies: Dict with supply name -> {current, target} values
            output_file: Base name for output file
        """
        labels = list(supplies.keys())
        current = [s.get("current", 0) for s in supplies.values()]
        target = [s.get("target", 100) for s in supplies.values()]

        # Calculate percentages
        percentages = [
            (c / t * 100) if t > 0 else 0
            for c, t in zip(current, target)
        ]

        data = ChartData(
            title="Supply Inventory Status",
            labels=labels,
            values=percentages,
            secondary_values=[100] * len(labels),  # Target line
            chart_type="bar"
        )

        output_path = self.output_dir / f"{output_file}.html"
        if isinstance(self.renderer, ASCIIRenderer):
            output_path = self.output_dir / f"{output_file}.txt"

        return self.renderer.render_bar_chart(data, str(output_path))

    def create_preparedness_gauge(self, score: float,
                                 output_file: str = "preparedness") -> str:
        """
        Create preparedness score gauge

        Args:
            score: Overall preparedness score (0-100)
            output_file: Base name for output file
        """
        thresholds = [
            (80, "Excellent"),
            (60, "Good"),
            (40, "Fair"),
            (0, "Needs Work")
        ]

        output_path = self.output_dir / f"{output_file}.html"
        if isinstance(self.renderer, ASCIIRenderer):
            output_path = self.output_dir / f"{output_file}.txt"

        return self.renderer.render_gauge(
            score, 100, "Overall Preparedness Score",
            thresholds, str(output_path)
        )

    def create_drill_performance(self, drill_history: List[Dict[str, Any]],
                                output_file: str = "drill_performance") -> str:
        """
        Create drill performance trend chart

        Args:
            drill_history: List of drill results with date and score
            output_file: Base name for output file
        """
        if not drill_history:
            drill_history = [{"date": "No data", "score": 0}]

        labels = [d.get("date", "N/A")[:10] for d in drill_history[-10:]]
        values = [d.get("score", 0) for d in drill_history[-10:]]

        data = ChartData(
            title="Drill Performance Trend",
            labels=labels,
            values=values,
            chart_type="line"
        )

        output_path = self.output_dir / f"{output_file}.html"
        if isinstance(self.renderer, ASCIIRenderer):
            output_path = self.output_dir / f"{output_file}.txt"

        return self.renderer.render_line_chart(data, str(output_path))

    def create_risk_heatmap(self, scenarios: List[str], categories: List[str],
                           risk_matrix: List[List[float]],
                           output_file: str = "risk_heatmap") -> str:
        """
        Create risk assessment heatmap

        Args:
            scenarios: List of disaster scenarios (rows)
            categories: List of risk categories (columns)
            risk_matrix: 2D matrix of risk values
            output_file: Base name for output file
        """
        output_path = self.output_dir / f"{output_file}.html"
        if isinstance(self.renderer, ASCIIRenderer):
            output_path = self.output_dir / f"{output_file}.txt"

        return self.renderer.render_heatmap(
            risk_matrix,
            (scenarios, categories),
            "Risk Assessment Matrix",
            str(output_path)
        )


# Convenience function
def get_visualization_manager(backend: str = "auto") -> VisualizationManager:
    """Get a visualization manager with the best available backend"""
    return VisualizationManager(preferred_backend=backend)


if __name__ == "__main__":
    # Demo
    vm = get_visualization_manager()

    # Risk dashboard
    risk_data = {
        "Earthquake": 75,
        "Flood": 45,
        "Fire": 60,
        "Power Outage": 82,
        "Tornado": 30
    }
    print(vm.create_risk_dashboard(risk_data))

    # Supply status
    supplies = {
        "Water": {"current": 15, "target": 20},
        "Food": {"current": 8, "target": 14},
        "First Aid": {"current": 1, "target": 1},
        "Batteries": {"current": 12, "target": 24}
    }
    print(vm.create_supply_status(supplies))

    # Preparedness gauge
    print(vm.create_preparedness_gauge(67.5))
