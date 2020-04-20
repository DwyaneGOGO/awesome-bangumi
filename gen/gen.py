from typing import Set, List, Dict, Optional

import yaml
import jinja2
import pydantic

category: Set[str] = set()
with open("./gen/a.jinja2", encoding="utf8") as f:
    template = jinja2.Template(f.read())


class Image(pydantic.BaseModel):
    description: str
    url: str


class Item(pydantic.BaseModel):
    name: str = ""
    url: pydantic.AnyHttpUrl
    description: str = ""
    repo: Optional[pydantic.AnyHttpUrl]

    @property
    def repo_url(self) -> Optional[pydantic.AnyHttpUrl]:
        if self.repo:
            return self.repo
        if self.url.host == "github.com":
            return self.url

    @property
    def badge(self):
        url = self.repo_url
        if not url:
            return ""
        return f"[![{url.path[1:]}](https://img.shields.io/github/last-commit{url.path})]({url})"


class Awesome(pydantic.BaseModel):
    items: Dict[str, List[Item]]


with open("./awesome.yaml", encoding="utf") as f:
    raw_data = yaml.safe_load(f)
    data = Awesome.parse_obj(raw_data)
    with open("./readme.md", "w", encoding="utf8") as f:
        f.write(template.render(data=data.items))
