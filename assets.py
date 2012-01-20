from flaskext.assets import Bundle

__all__ = ('register_assets',)


def register_assets(assets):
    core = Bundle(
        'js/src/core/jquery.js',
        'js/src/core/underscore.js',
        filters='yui_js',
        output='js/bundles/core.js'
    )

    app = Bundle(
        'js/src/app/*.js',
        filters='yui_js',
        output='js/bundles/app.js'
    )

    assets.register('core', core)
    assets.register('app', app)
