from dataclasses import dataclass, asdict
from typing import Dict, Tuple

"""
theme.py

Project-level theme definitions and helpers for creating consistent UI styling.
Provides a Theme class that can emit Qt QSS (string) and a simple Tkinter style dict.

Usage examples:
- For PyQt/PySide:
    theme = Theme()
    app.setStyleSheet(theme.qss())

- For Tkinter:
    theme = Theme()
    styles = theme.tk_styles()
    # use styles to configure widget options like bg, fg, font, bd, relief, highlightthickness, padx, pady
"""



def _hex_to_rgba(hex_color: str, alpha: float = 1.0) -> Tuple[int, int, int, float]:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c*2 for c in hex_color)
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b, max(0.0, min(1.0, alpha))


@dataclass
class Theme:
    # Core colors
    primary: str = "#55B158"         # green
    primary_dark: str = "#388E3C"
    accent: str = "#FF6F00"          # amber/orange
    background: str = "#F5F7FA"      # light gray
    surface: str = "#FFFFFF"         # card background
    text: str = "#212121"            # primary text
    muted: str = "#6E6E6E"           # secondary text
    success: str = "#2E7D32"
    danger: str = "#D32F2F"

    # Layout tokens
    radius: int = 6                  # border radius px
    spacing: int = 8                 # base spacing px
    font_family: str = "Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    font_size: int = 12              # base font size px
    shadow: str = "0 2px 6px rgba(0,0,0,0.08)"

    def qss(self) -> str:
        qss_template = """
        displayText {{
            background-color: {background};
            color: {text};
            font-family: {font_family};
            font-size: {font_size}px;
        }}

        /* Buttons */
        QPushButton {{
            background-color: {primary};
            color: white;
            border-radius: {radius}px;
            padding: {padding}px {padding_double}px;
            border: none;
        }}
        QPushButton:hover {{
            background-color: {primary_dark};
        }}
        QPushButton:disabled {{
            background-color: {muted};
            color: #ffffffb3;
        }}

        /* Secondary (flat) buttons */
        QPushButton[flat="true"] {{
            background: transparent;
            color: {primary};
            border: 1px solid transparent;
        }}
        QPushButton[flat="true"]:hover {{
            background: rgba(0,0,0,0.03);
        }}

        /* Card-like frames */
        QFrame.card {{
            background: {surface};
            border-radius: {radius}px;
            padding: {padding}px;
            border: 1px solid rgba(0,0,0,0.06);
        }}

        /* Line edits / inputs */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background: {surface};
            border: 1px solid rgba(0,0,0,0.12);
            border-radius: {radius}px;
            padding: {padding}px;
            selection-background-color: {primary};
            selection-color: white;
        }}

        /* Tooltips */
        QToolTip {{
            background-color: {text};
            color: {surface};
            border-radius: {radius}px;
            padding: 4px 6px;
        }}
        """
        return qss_template.format(
            background=self.background,
            text=self.text,
            font_family=self.font_family,
            font_size=self.font_size,
            primary=self.primary,
            primary_dark=self.primary_dark,
            surface=self.surface,
            muted=self.muted,
            radius=self.radius,
            padding=max(4, int(self.spacing * 0.75)),
            padding_double=max(6, int(self.spacing * 1.5)),
        )

    def tk_styles(self) -> Dict[str, Dict[str, object]]:
        """
        Returns a dictionary of widget style presets suitable for use with Tkinter widget.config(**style).
        Keys represent common widget types: "button", "primary_button", "frame", "label", "entry".
        """
        base_font = (self.font_family.split(",")[0].strip(), self.font_size)
        return {
            "frame": {"bg": self.surface, "bd": 0, "highlightthickness": 0},
            "label": {"bg": self.surface, "fg": self.text, "font": base_font},
            "button": {
                "bg": self.surface,
                "fg": self.text,
                "bd": 0,
                "relief": "flat",
                "padx": self.spacing,
                "pady": max(4, int(self.spacing / 2)),
                "font": base_font,
            },
            "primary_button": {
                "bg": self.primary,
                "fg": "white",
                "bd": 0,
                "relief": "flat",
                "padx": self.spacing,
                "pady": max(6, int(self.spacing * 0.75)),
                "activebackground": self.primary_dark,
                "font": base_font,
            },
            "entry": {
                "bg": self.surface,
                "fg": self.text,
                "bd": 1,
                "relief": "solid",
                "highlightthickness": 0,
                "font": base_font,
            },

        }

    def color_rgba(self, name: str, alpha: float = 1.0) -> str:
        """
        Return CSS rgba() string for the named theme color.
        Example: theme.color_rgba('primary', 0.8) -> 'rgba(25,118,210,0.8)'
        """
        value = getattr(self, name, None)
        if not value or not isinstance(value, str):
            raise ValueError(f"No color named '{name}' in theme")
        r, g, b, _ = _hex_to_rgba(value, alpha)
        return f"rgba({r},{g},{b},{max(0.0,min(1.0,alpha))})"

    def as_dict(self) -> Dict[str, object]:
        """Return theme fields as a dictionary (useful for templating or serializing)."""
        return asdict(self)


# Minimal self-test when run directly (does not run on import)
if __name__ == "__main__":
    t = Theme()
    print("QSS preview:\n", t.qss()[:800])
    print("\nTk styles preview:\n", t.tk_styles())