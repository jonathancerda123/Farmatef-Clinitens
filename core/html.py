"""Allowlist de contenido de CKEditor; también se aplica al mostrar datos antiguos."""
import nh3


def sanitizar_html(valor):
    return nh3.clean(
        valor or "", tags={"p", "br", "b", "strong", "i", "em", "u", "s",
                           "h2", "h3", "h4", "ul", "ol", "li", "blockquote", "a"},
        attributes={"a": {"href", "title"}},
        clean_content_tags={"script", "style", "iframe", "object", "svg", "math"},
        url_schemes={"https", "http", "mailto"}, link_rel="noopener noreferrer",
    )
