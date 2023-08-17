import os.path

import mkdocs
import re
import logging
from typing import Tuple

PDOC_LINK_REGEX = re.compile(r"\[([^]]*)]\(pdoc:([^)]*)\)")

QualName = Tuple[str]


class PdocPlugin(mkdocs.plugins.BasePlugin):
    """
    This plugin replaces link [Class](pdoc:somepackage.MyClass) to link into pdoc documentation
    """

    config_scheme = (("api_path", mkdocs.config.config_options.Type(str, default="")),)

    def __init__(self):
        self.api_path: str = ""
        self.docs_dir: str = ""
        self.site_url: str = ""
        self.logger = logging.getLogger(__name__)

    def _qualname_to_filename(self, qname: QualName) -> str:
        p = "/".join(qname)
        return os.path.join(self.api_path, f"{p}.html")

    def _resolve_link(self, qname: QualName) -> str:
        original_qname = qname
        while qname:
            path = self._qualname_to_filename(qname)
            filename = os.path.join(self.docs_dir, path)
            if os.path.isfile(filename):
                path = os.path.join(self.site_url, path)
                rest = original_qname[len(qname) :]
                if rest:
                    return path + "#" + ".".join(rest)
                else:
                    return path
            qname = qname[:-1]

        p = ".".join(original_qname)
        self.logger.debug(f"Invalid reference: {p}")
        return f"!!! Unresolved path to: {p}"

    def on_config(self, config, **kwargs):
        self.docs_dir = config["docs_dir"]
        self.site_url = config["site_url"]
        self.api_path = self.config.get("api_path") or ""

    def on_page_markdown(self, src: str, page, config, *args, **kwargs):
        links = []
        for match in PDOC_LINK_REGEX.finditer(src):
            links.append(match.groups())
        for name, path in links:
            qname = tuple(path.split("."))
            target_name = name or (qname[-1] if qname else "")
            src = src.replace(
                f"[{name}](pdoc:{path})",
                f"[{target_name}]({self._resolve_link(qname)})",
            )
        return src
