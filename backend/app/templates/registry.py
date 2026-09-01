from typing import List, Optional, Dict
from app.templates.spec import TemplateSpecification
from app.templates.definitions import ALL_TEMPLATES
from app.core.errors import NotFoundError


class TemplateRegistry:
    """Registry maintaining all data-driven template specifications."""
    _templates: Dict[str, TemplateSpecification] = {t.template_id: t for t in ALL_TEMPLATES}

    @classmethod
    def list_all(cls) -> List[TemplateSpecification]:
        return list(cls._templates.values())

    @classmethod
    def get(cls, template_id: str) -> TemplateSpecification:
        if template_id not in cls._templates:
            raise NotFoundError("TemplateSpecification", template_id)
        return cls._templates[template_id]

    @classmethod
    def exists(cls, template_id: str) -> bool:
        return template_id in cls._templates
