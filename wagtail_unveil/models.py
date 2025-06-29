from dataclasses import dataclass, field


@dataclass
class UrlEntry:
    """
    Base class for URL entries.

    Attributes:
        id: The ID of the URL entry.
        model_name: The name of the model.
        url_type: The type of URL.
        url: The URL.
    """
    id: int = field(default_factory=lambda: 0)
    model_name: str = field(default_factory=lambda: "")
    url_type: str = field(default_factory=lambda: "")
    url: str = field(default_factory=lambda: "")

    class Meta:
        abstract = True