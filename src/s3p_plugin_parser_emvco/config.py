import datetime

from s3p_sdk.plugin.config import (
    PluginConfig,
    CoreConfig,
    TaskConfig,
    trigger,
    MiddlewareConfig,
    modules,
    payload, RestrictionsConfig
)
from s3p_sdk.plugin.types import SOURCE
from s3p_sdk.module import (
    WebDriver,
)

config = PluginConfig(
    plugin=CoreConfig(
        reference='emvco',         # уникальное имя источника
        type=SOURCE,                            # Тип источника (SOURCE, ML, PIPELINE)
        files=['emvco.py', ],        # Список файлов, которые будут использоваться в плагине (эти файлы будут сохраняться в платформе)
        is_localstorage=False,
        restrictions=RestrictionsConfig(
            maximum_materials=50,
            to_last_material=None,
            from_date=datetime.datetime(2025, 1, 1),
            to_date=None,
        )
    ),
    task=TaskConfig(
        trigger=trigger.TriggerConfig(
            type=trigger.SCHEDULE,
            interval=datetime.timedelta(days=4),    # Интервал перезапуска плагина
        )
    ),
    middleware=MiddlewareConfig(
        modules=[
            modules.TimezoneSafeControlConfig(order=1, is_critical=True),
            modules.FilterOnlyNewDocumentWithDB(order=2, is_critical=True),
            modules.DownloadDocumentsAssetWithSelenium(order=3, available_field='available', is_critical=True, cookie_selector='form > div > button'),
            modules.UploadToS3(order=4, is_critical=True),
            modules.SaveDocument(order=5, is_critical=True),
        ],
        bus=None,
    ),
    payload=payload.PayloadConfig(
        file='emvco.py',                 # python файл плагина (точка входа). Этот файл должен быть указан в `plugin.files[*]`
        classname='EMVCo',               # имя python класса в указанном файле
        entry=payload.entry.EntryConfig(
            method='content',
            params=[
                payload.entry.ModuleParamConfig(key='web_driver', module_name=WebDriver, bus=True),
            ] # Подробнее можно почитать [тут](./readme.md#пример-конфигурации-параметров-запуска-плагина
        )
    )
)

__all__ = ['config']
