from setuptools import setup

setup(
    name="mkdocs-pdoc-plugin",
    version="0.0.1",
    description="pdoc plugin for linking to API documentation",
    author="Ada Böhm",
    author_email="ada@kreatrix.org",
    url="https://github.com/spirali/mkdocs-pdoc-plugin",
    install_requires=["mkdocs>=1.2,<2"],
    packages=["mkdocs_pdoc_plugin"],
    entry_points={
        "mkdocs.plugins": [
            "pdoc = mkdocs_pdoc_plugin:PdocPlugin",
        ]
    },
)
