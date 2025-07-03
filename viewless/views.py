from django.shortcuts import render
from django.conf import settings
from pathlib import Path
import os

def get_project_root_from_config():
    viewless_config = getattr(settings, 'VIEWLESS_CONFIG', None)
    if not viewless_config:
        return None, 'VIEWLESS_CONFIG must be set in your settings.'
    project_root = viewless_config.get('PROJECT_ROOT')
    if not isinstance(project_root, str):
        return None, 'PROJECT_ROOT must be set as a string in VIEWLESS_CONFIG.'
    return Path(project_root).resolve(), None

def get_template_paths(project_root: Path, absolute: bool = False):
    template_paths = []
    for root, dirs, files in os.walk(project_root):
        if os.path.basename(root) == 'templates':
            for dirpath, _, filenames in os.walk(root):
                for filename in filenames:
                    if filename.endswith('.html'):
                        abs_path = Path(dirpath, filename).resolve()
                        if absolute:
                            template_paths.append(str(abs_path))
                        else:
                            rel_path = abs_path.relative_to(project_root)
                            template_paths.append(str(rel_path))
    return template_paths

def show_templates_view(request):
    show_absolute = request.GET.get('absolute', '0') == '1'
    project_root, error = get_project_root_from_config()
    template_paths = []
    if not error:
        template_paths = get_template_paths(project_root, show_absolute)
    context = {
        'project_root': project_root,
        'template_paths': template_paths,
        'error': error,
        'show_absolute': show_absolute,
    }
    return render(request, 'viewless/show_templates.html', context)
