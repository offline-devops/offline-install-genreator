from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("autoinstall"),
    autoescape=select_autoescape()
)


def render():
    template = env.get_template('build.nsi.jinja2')
    print(template.render(menu_tree=[
            {
                "name": "1",
                "groups": [
                    {
                        "name": "2",
                        "groups": [
                            {
                                "name": "left-3-1",
                                "path": "hi"
                            }
                        ]
                    },
                    {
                        "name": "3",
                        "id": "dddd",
                        "sec": {
                            "extract_folder": "/ssdfadf",
                            "exe_name": "sdfadf",
                            "exe_path": "/sadfa/adsfad/fasf/adf.exe"
                        }
                    }
                ]
            },
        {
            "name": "3",
            "id": "dddd",
            "sec": {
                "extract_folder": "/ssdfadf",
                "exe_name": "sdfadf",
                "exe_path": "/sadfa/adsfad/fasf/adf.exe"
            }
        }
        ]
    ))