import os
import re
import jinja2

GO_PATH = os.getenv('GOPATH', '')
GO_ROOT = os.getenv('GOROOT', '')


def to_pascal(name: str) -> str:
    return "".join(x.title() for x in name.split('_'))


def detect_package(location: str) -> (str, str):
    sys_src = (os.path.join(GO_ROOT, "src"), os.path.join(GO_PATH, "src"))
    path = os.path.abspath(location).split(os.path.sep)
    n = len(path)
    for i in range(n, -1, -1):
        loc = "/".join(path[:i])
        pkg = "/".join(path[i:])
        mod_file = os.path.join(loc, "go.mod")
        try:
            with open(mod_file, 'rt') as f:
                pkg = next(f).split(' ')[-1].strip()
                r = os.path.relpath("/".join(path), loc)
                if r == ".":
                    return pkg, pkg
                return pkg, os.path.join(pkg, r)
        except FileNotFoundError:
            pass
        if loc in sys_src:
            return pkg, loc
    raise RuntimeError('package not detected')


def generate(name: str, section: str, *, method: str = 'GET', location: str = '.', templates_dir: str = 'templates'):
    assert method in ('GET', 'POST')
    assert name != ''
    assert section != ''
    assert re.match(r'[a-z0-9_]', name)
    assert re.match(r'[a-z0-9\-_]', section)
    root_pkg, our_pkg = detect_package(location)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
    env.filters['pascal'] = to_pascal
    env.filters['to_handler'] = lambda ct: "handle" + ct['method'].title() + to_pascal(ct['name'])
    env.filters['to_page'] = lambda ct: "page" + ct['method'].title() + to_pascal(ct['name'])

    p_name = to_pascal(name)
    package = os.path.basename(section)
    func_name = method.lower() + p_name
    handler_name = "handle" + method.title() + p_name
    print("package:", package)
    print("project package:", root_pkg)
    print("method:", func_name)

    views_dir = os.path.join(location, "templates", "views")
    view_name = os.path.join(section, method.lower() + "_" + name + ".gotemplate")
    view_file = os.path.join(views_dir, view_name)
    layouts_dir = os.path.join(location, "templates", "layouts")
    layout_name = os.path.join(section + ".gotemplate")
    layout_file = os.path.join(layouts_dir, layout_name)

    controller_root = os.path.join(location, "controller")
    controller_dir = os.path.join(controller_root, section)
    controller_file = os.path.join(controller_dir, method.lower() + "_" + name.lower() + ".go")
    section_controller_file = os.path.join(controller_dir, "section.go")

    services_dir = os.path.join(location, "service")
    service_file = os.path.join(services_dir, "app.go")

    utils_dir = os.path.join(location, 'utils')
    utils_file = os.path.join(utils_dir, 'utils.go')

    os.makedirs(os.path.dirname(layout_file), exist_ok=True)
    os.makedirs(os.path.dirname(view_file), exist_ok=True)
    os.makedirs(os.path.dirname(controller_file), exist_ok=True)
    os.makedirs(os.path.dirname(service_file), exist_ok=True)
    os.makedirs(os.path.dirname(utils_file), exist_ok=True)

    if not os.path.exists(layout_file):
        # render base layout template
        text = env.get_template('base.jinja2').render(
            package=package,
            name=name,
            func_name=func_name,
        )
        with open(layout_file, 'wt') as f:
            f.write(text)

    if not os.path.exists(view_file):
        # render method template
        text = env.get_template('view.jinja2').render(
            package=package,
            name=name,
            func_name=func_name,
        )
        with open(view_file, 'wt') as f:
            f.write(text)

    if not os.path.exists(controller_file):
        # render main controller code
        text = env.get_template('controller.jinja2').render(
            root_pkg=root_pkg,
            our_pkg=our_pkg,
            in_params=func_name + 'Params',
            out_params=func_name + 'Data',
            package=package,
            name=name,
            section=section,
            method=method,
            func_name=func_name,
            view_name=view_name,
            layout_name=layout_name,
            handler_name=handler_name,
            page_name=method.title() + p_name,
        )
        with open(controller_file, 'wt') as f:
            f.write(text)

    if not os.path.exists(service_file):
        # render service file (app)
        text = env.get_template('service.jinja2').render(
            package=package,
            our_pkg=our_pkg,
        )
        with open(service_file, 'wt') as f:
            f.write(text)

    controllers = [{'method': x[:x.index('_')], 'name': x[x.index('_') + 1:x.rindex('.')]} for x in
                   os.listdir(controller_dir) if '_' in x]
    # always re-render section controller code
    text = env.get_template('section_controller.jinja2').render(
        root_pkg=root_pkg,
        our_pkg=our_pkg,
        package=package,
        section=section,
        root_path=re.sub(r'[^/]+', '..', section),
        controllers=controllers,
    )
    with open(section_controller_file, 'wt') as f:
        f.write(text)

    sections = []
    for dirpath, dirnames, filenames in os.walk(controller_root):
        for file in filenames:
            if file == 'section.go':
                sections.append(os.path.join(our_pkg, 'controller', os.path.relpath(dirpath, controller_root)))

    # add utils
    text = env.get_template('utils.jinja2').render(
        root_pkg=root_pkg,
        our_pkg=our_pkg,
        sections=sections,
    )
    with open(utils_file, 'wt') as f:
        f.write(text)
