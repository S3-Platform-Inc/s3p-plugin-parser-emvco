# EMVco (S3 Platform Plugin)

[![Test Plugin](https://github.com/S3-Platform-Inc/s3p-plugin-parser-emvco/actions/workflows/plugin_test.yml/badge.svg)](https://github.com/S3-Platform-Inc/s3p-plugin-parser-emvco/actions/workflows/plugin_test.yml)
[![Release plugin](https://github.com/S3-Platform-Inc/s3p-plugin-parser-emvco/actions/workflows/build-release.yml/badge.svg)](https://github.com/S3-Platform-Inc/s3p-plugin-parser-emvco/actions/workflows/build-release.yml)
[![Sync plugin to S3](https://github.com/S3-Platform-Inc/s3p-plugin-parser-emvco/actions/workflows/sync-release.yml/badge.svg)](https://github.com/S3-Platform-Inc/s3p-plugin-parser-emvco/actions/workflows/sync-release.yml)

[//]: # (Если вы все еще не совсем понимаете, о чем идет речь, прочитайте наше введение: Что такое S3 Platform?)

# Содержание
- [Быстрый старт](#быстрый-старт)
- [Обновление зависимостей](#обновления-зависимостей)
- [Требования](#требования-к-разработке-плагина)
  - [Структура](#обязательная-структура)
  - [CI](#github-actions)
  - [Тесты](#тесты)
    - [Как запустить тесты](#запуск-тестов)
- [Правила написания парсера](#правила-написания-парсеров)
- [Пример конфигурации](#примеры-конфигурации)
  - [Конфигурация параметров запуска плагина](#пример-конфигурации-параметров-запуска-плагина)

## Быстрый старт

1. На GitHub:
   1. В GitHub выбрать `Use this template` для создания плагина.
   2. Назвать новый плагин в соответствии с [требованиями](#название-репозитория).
   3. **ПРОПУСТИТЬ ШАГ, ЕСЛИ РЕПОЗИТОРИЙ СОЗДАЕТСЯ В РАМКАХ [ОРГАНИЗАЦИИ](https://github.com/S3-Platform-Inc)**. Добавить секреты в репозиторий (см. [тут](#секреты)).
   4. Открыть новые issue (пример названия: `New plugin: xxx` или `add payload xxx`)
   5. Создать новую ветку в проекте, наследуемую от `main` (пример названия: `feature/{issue id}-new-plugin`).
2. В IDE:
   1. Скачаем новый репозиторий `git clone [repo name]`.
   2. Переключаемся в новую ветку `git checkout feature/{issue id}-new-plugin`.
   3. Прочитать [требования](#требования-к-разработке-плагина).
   4. Обновить Github Badges в начале файла `readme.md` (`s3-platform-plugin-template` на `название репозитория плагина`).
   5. Придумать название плагина в соответствии с [требованиями](#название-плагина). 
   6. Обновить [GitHub Actions](#обновление-cicd-).
   7. Обновить [декларацию плагина](#pluginxml).
   8. Обновить документация (`readme.md`): Заголовок, описание, характерные особенности парсера и логика работы, эксклюзивные начальные параметры парсера. 
   9. Написать логику плагина (см. [тут](#правила-написания-парсеров)). 
   10. Обновить конфигурацию плагина (см. [тут](https://github.com/S3-Platform-Inc/s3p-sdk/blob/main/docs/config.md)).
   11. Обновить тесты и дописать новые при необходимости (см. [тут](#тесты)).
   12. Запустить тесты (см. [тут](#запуск-тестов)).
   13. Если все тесты пройдены, сохраняем изменениями (`git commit ...` и `git pull`).
3. На GitHub:
   1. Создать pull request для ветки `feature/{issue id}-new-plugin`.
   2. Дождаться завершения `Checks` для PR.
   3. **ШАГ ОБЯЗАТЕЛЕН В РАМКАХ [ОРГАНИЗАЦИИ](https://github.com/S3-Platform-Inc)**. Указать в PR админа: `Assignees` -> `CuberHuber`
   4. **ПРОПУСТИТЬ ШАГ, ЕСЛИ РЕПОЗИТОРИЙ СОЗДАЕТСЯ В РАМКАХ [ОРГАНИЗАЦИИ](https://github.com/S3-Platform-Inc)**. Слить изменения и закрыть PR.

------------

## Обновления зависимостей
При работе над плагином важно поддерживать его версию в актуальном состоянии. Шаблон плагинов и версия SDK часто обновляются, из-за начальной стадии продукта.
Чтобы синхронизироваться с шаблоном можно выполнить следующие действия.

> [!NOTE]
> Рекомендуется выполнять синхронизацию мануально. Таким образом вы сможете исправить потенциальные конфликты при слиянии.

1. Нужно добавить шаблон в git
```shell
git remote add template https://github.com/S3-Platform-Inc/s3-platform-plugin-template.git
git fetch --all
```

2. Влить `main` ветку шаблона в `main` ветку репозитория плагина
> [!NOTE]
> Убедитесь, что важные изменения вашего проекта не будут удалены
```shell
git merge template/main --allow-unrelated-histories
```
3. При возникновении конфликтов, нужно принять все изменения из template, а затем подстраивать свой код.
> [!NOTE]
> После синхронизации с шаблоном, нужно обновить зависимости.
```shell
poetry install
# или, при ошибке установки можно обновить записимость вручную.
poetry add s3p-sdk@[relevant version]
```
4. Обновить код плагина и тестов при необходимости.


## Требования к разработке плагина

### Правила наименований

#### Название репозитория
Общий шаблон названия репозитория
```
s3p-plugin-[type]-[uniq_name]
```
Шаблон названия репозитория парсера
```
s3p-plugin-parser-[uniq_name]
```
Пример названия репозитория парсера
```
s3p-plugin-parser-emvco
```

#### Название плагина
Шаблон названия плагина схож с названием репозитория.
```
s3p_plugin_[type]_[uniq_name]
```
Пример названия репозитория парсера
```
s3p_plugin_parser_emvco
```

### Обязательная структура
Репозиторий плагина состоит из основных компонентов:

```markdown
my-plugin/                      # Репозиторий
│
├── .github/                    #
│   └── workflows/              # GitHub Actions 
│
├── src/                        # Основная директория разработки
│   └── <uniq plugin name>/     # Каталог с файлами плагина.
│       ├── config.py           # Конфигурация плагина
│       └── <some files>.*      # Файлы плагина (его payload)
│ 
├── tests/                      # Тесты для плагина
│
└── plugin.xml                  # Основной декларативный файл плагина
```

#### Plugin.xml
Стандартный вид `plugin.xml`:
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<project name="[ uniq plugin name ]">
    <version>[ version ]</version>
</project>
```
- уникальное имя плагина [`uniq plugin name`] см. [тут](#название-плагина). Используется как имя каталога с файлами плагина и в тестах.
- версия плагина [`version`]. Имеет формат `[N > 0].[N >= 0]`. Последняя стабильная версия по умолчанию - `3.0`.

#### src
В каталоге `src` должен обязательно находиться каталог, названный [`uniq plugin name`] (Такое же название, как и в [plugin.xml](#pluginxml)). 

##### uniq plugin name
- Каталог плагина должен обязательно содержать файл `repo/src/[uniq plugin name]/config.py`.
- Все дополнительные файлы плагина (парсер, вспомогательные файлы) должны быть расположены в этом разделе `repo/src/[uniq plugin name]/`.

##### config.py
Файл config.py - это обязательный файл плагина. 

> [!WARNING]
> Нужно просмотреть файл `config.py` и поля, связанные с уникальными названиями и файлами.

> [!TIP]
> Читайте комментарии в файле `config.py`


### GitHub Actions
В репозитории настроен CI/CD на GitHub Actions.
Для его полноценной работы необходимо добавить секреты в репозиторий на стороне GitHub (см. [раздел](https://github.com/S3-Platform-Inc/s3-platform-plugin-template/settings/secrets/actions)).

Если репозиторий с плагином создан в аккаунте организации [S3 Platform](https://github.com/S3-Platform-Inc), то можно воспользоваться секретами организации. В противном случае нужно создавать секреты репозитория.

#### Секреты

**CI/СD:**
- `PLUGIN_RELEASE_TOKEN`: создается в GitHub для работы с релизами репозиториев (см. [здесь](https://github.com/settings/personal-access-tokens)).

S3 Platform использует Amazon S3 в качестве [объектного хранилища](https://ru.wikipedia.org/wiki/Amazon_S3).
Следующие секреты требуются для подключения к нему (_Все 5 значений можно получить в панели администратора хранилища_):
- `S3_ACCESS_KEY_ID`
- `S3_SECRET_ACCESS_KEY`
- `S3_BACKET_NAME`
- `S3_REGION`
- `S3_SERVICE_URL`

#### Обновление CI/CD 

> [!IMPORTANT]
> После написание плагина от разработчика потребуется обновить некоторые поля в github actions yml файлах.

#### [Файл сборка](.github/workflows/build-release.yml)
Требуется обновить переменную `PATH_TO_CONFIG` в `env` на `src.[uniq plugin name].config`.


### Тесты

> [!WARNING]
> Требуется дополнить некоторые тесты, которые помечены отметкой `!WARNING`

В [тестах нагрузки](tests/payload/test_plugin_run.py) в функции `run_payload()` нужно обновить сигнатуру вызова (соответствие главному классу парсера).

> [!TIP]
> Последующие тесты с отметкой нужно просмотреть и обновить при необходимости. 

> [!TIP]
> Рекомендуется дополнять тесты для парсеров с необычной логикой.

#### Запуск тестов
```shell
poetry run pytest -v
```
or
```shell
pytest -v
```

## Правила написания парсеров

Ниже приведен пример парсера с подробным описанием.
```python
from s3p_sdk.plugin.payloads.parsers import S3PParserBase
from s3p_sdk.types import S3PRefer, S3PDocument, S3PPlugin

class MyTemplateParser(S3PParserBase):
    """
    Парсер плагина, который использует `S3PParserBase`
    """

    def __init__(self, refer: S3PRefer, plugin: S3PPlugin, web_driver: WebDriver, max_count_documents: int = None, last_document: S3PDocument = None):
        """
        Конструктор парсера плагина.
        
        Обязательные параметры (передаются платформой):
        :param:refer                    S3PRefer    -   источник, который обрабатывает плагин.
        :param:plugin                   S3PPlugin   -   метаданные плагина.
        
        Вариативные параметры (Требуюется указать эти параметры в src/<uniq plugin name>/config.py):
        :param:max_count_documents      int         -   максимальное число документов, которые должен собирать парсер.
        
        Остальные параметры могут не передаваться в конструктор класса. Они могут быть добавлены по желанию разработчика парсера. (Требуюется указать эти параметры в src/<uniq plugin name>/config.py).
        Но, стоит учитывать правило "все, что может быть параметризовано - должно быть параметризовано".  
        """
        super().__init__(refer, plugin, max_count_documents, last_document)

        # Тут должны быть инициализированы свойства, характерные для этого парсера. Например: WebDriver
        self._driver = web_driver
        self._wait = WebDriverWait(self._driver, timeout=20)

    def _parse(self) -> None:
        """
        Главные метод класса парсера, перегружающий метод класса `S3PParserBase`.
        
        Этот метод будет вызван платформой при запуске парсера.
        Это обязывает разработчика парсить источник в этом методе (безусловно, разработчик может создавать дополнительные методы внутри этого класса). 
        """
        for article in self.test_data():
            
            # Метод self._find(:S3PDocument) вызывается при парсинге для того, чтобы отдать найденный документ платформе.
            # Разработчик обязан использовать только этот метод при парсинге.
            # Разработчику не нужно думать над тем, что происходит дальше. Платформа сама остановит работу парсера при выполнении ряда условий: собрано нужное число документов. 
            self._find(article)
```

## Примеры конфигурации

### Пример конфигурации параметров запуска плагина
Ниже приведен пример конфигурации `payload.entry.params`. 
```python
from s3p_sdk.plugin.config import payload
from s3p_sdk.module import WebDriver

[
    payload.entry.ModuleParamConfig(key='web_driver', module_name=WebDriver, bus=True), # Передается модуль
    payload.entry.ConstParamConfig(key='url', value='url to the source page'), # Передается константа
]
```
