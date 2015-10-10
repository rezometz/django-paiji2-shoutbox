from django.conf.urls import url, include

from modular_blocks import ModuleApp, TemplateTagBlock, modules

from . import urls


class ShoutboxModule(ModuleApp):
    app_name = 'bulletin_board'
    name = 'bulletin-board'
    urls = url(r'^shoutbox/', include(urls))
    templatetag_blocks = [
        TemplateTagBlock(
            name='bulletin-board',
            library='shoutbox',
            tag='display_bulletin_board',
            cache_time=0,
            kwargs={
                'nb': 10,
            },
        ),
    ]


modules.register(ShoutboxModule)
