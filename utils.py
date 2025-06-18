import importlib

def load_page(name):
    mod = importlib.import_module(f"pages.{name}")
    if hasattr(mod, 'render'):
        mod.render()