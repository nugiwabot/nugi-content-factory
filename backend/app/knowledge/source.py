"""
Knowledge source engine: reads business knowledge from the freelance
repository (freelance-nugi-software-engineer) on disk using the allow-list
manifest. Filesystem + simple keyword retrieval only - no vector database.

Private/sensitive paths are never read. Content is sanitized before use.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional

from app.core.config import settings
from app.core.logging import logger
from app.knowledge.manifest import category_for, tags_for, CORE, SUPPORTING, EXCLUDE

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"(?:\+?62|0)8\d{7,13}")
_CLIENT_NAMES = [
    "Yanproland",
    "GREN Propertykost",
    "GREN Property",
    "GREN",
]


class _KnowledgeIndex:
    """In-memory index of the external knowledge repository (built lazily)."""

    def __init__(self) -> None:
        self._source_dir: Optional[Path] = None
        self._core_docs: List[str] = []
        self._supporting: Dict[str, Dict[str, object]] = {}
        self._loaded = False

    def _sanitize(self, text: str) -> str:
        cleaned = _EMAIL_RE.sub("[email]", text)
        cleaned = _PHONE_RE.sub("[phone]", cleaned)
        for name in _CLIENT_NAMES:
            cleaned = cleaned.replace(name, "[client]")
        return cleaned

    def _read_markdown(self, root: Path) -> None:
        self._core_docs = []
        self._supporting = {}
        for md in root.rglob("*.md"):
            rel = md.relative_to(root).as_posix()
            category = category_for(rel)
            if category == EXCLUDE:
                continue
            try:
                raw = md.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                logger.warning(f"Knowledge source read failed for {rel}: {e}")
                continue
            content = self._sanitize(raw)
            if category == CORE:
                self._core_docs.append(f"### {rel}\n{content}")
            elif category == SUPPORTING:
                self._supporting[rel] = {"tags": tags_for(rel), "text": content}

    def load(self, force: bool = False) -> bool:
        source_dir = settings.knowledge_source_dir
        if source_dir is None:
            self._loaded = False
            return False
        if self._loaded and not force and self._source_dir == source_dir:
            return True
        self._source_dir = source_dir
        self._read_markdown(source_dir)
        self._loaded = True
        logger.info(
            f"Knowledge source indexed from '{source_dir}': "
            f"{len(self._core_docs)} core, {len(self._supporting)} supporting docs."
        )
        return True

    def clear(self) -> None:
        self._loaded = False
        self._source_dir = None
        self._core_docs = []
        self._supporting = {}

    def refresh(self) -> bool:
        self.clear()
        return self.load(force=True)

    @property
    def active(self) -> bool:
        return self._loaded and self._source_dir is not None

    @property
    def source_path(self) -> Optional[Path]:
        return self._source_dir if self._loaded else (settings.knowledge_source_dir)

    def core_context(self) -> str:
        if not self.load():
            return ""
        return "\n\n".join(self._core_docs)

    def supporting_for_topic(self, topic: str, pillar: Optional[str] = None, limit: int = 3) -> str:
        if not self.load():
            return ""
        topic_tokens = set(self._tokenize(topic))
        scored: List[tuple] = []
        for rel, entry in self._supporting.items():
            tags = entry["tags"] or []
            text = str(entry["text"])
            haystack_tokens = set(self._tokenize(" ".join(tags))) | set(self._tokenize(text))
            overlap = len(topic_tokens & haystack_tokens)
            if pillar and pillar.lower() in " ".join(tags).lower():
                overlap += 2
            scored.append((overlap, rel))
        scored.sort(key=lambda x: -x[0])
        chosen = [rel for ov, rel in scored[:limit] if ov > 0]
        if not chosen:
            return ""
        parts = []
        for rel in chosen:
            parts.append(f"### {rel}\n{self._supporting[rel]['text']}")
        return "\n\n".join(parts)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return [t for t in re.findall(r"[a-zA-Z0-9]+", (text or "").lower()) if len(t) > 2]


_index = _KnowledgeIndex()


class KnowledgeSource:
    """Public facade for the external business knowledge repository."""

    @staticmethod
    def refresh() -> bool:
        return _index.refresh()

    @staticmethod
    def clear() -> None:
        _index.clear()

    @staticmethod
    def status() -> Dict[str, object]:
        _index.load()
        return {
            "active": _index.active,
            "source_path": str(_index.source_path) if _index.source_path else None,
            "core_docs": len(_index._core_docs),
            "supporting_docs": len(_index._supporting),
        }

    @staticmethod
    def set_source_path(path: str) -> None:
        p = Path(path).expanduser()
        if not p.is_dir():
            raise ValueError(f"Knowledge source path tidak ditemukan atau bukan folder: {path}")
        # Persist to a dedicated small file so Settings saving never clobbers it.
        from app.core.config import settings
        settings.KNOWLEDGE_SOURCE_PATH = str(p.resolve())
        cfg_file = settings.config_dir / "knowledge_source.json"
        import json
        cfg_file.write_text(json.dumps({"source_path": str(p.resolve())}), encoding="utf-8")
        _index.clear()

    @staticmethod
    def load_persisted() -> None:
        from app.core.config import settings
        cfg_file = settings.config_dir / "knowledge_source.json"
        import json
        if cfg_file.exists():
            try:
                data = json.loads(cfg_file.read_text(encoding="utf-8"))
                path = data.get("source_path")
                if path and Path(path).is_dir():
                    settings.KNOWLEDGE_SOURCE_PATH = path
            except Exception:
                pass

    @staticmethod
    def core_context() -> str:
        return _index.core_context()

    @staticmethod
    def supporting_for_topic(topic: str, pillar: Optional[str] = None, limit: int = 3) -> str:
        return _index.supporting_for_topic(topic, pillar, limit)
