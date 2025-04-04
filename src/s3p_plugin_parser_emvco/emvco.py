import time

import dateparser
from s3p_sdk.exceptions.parser import S3PPluginParserOutOfRestrictionException, S3PPluginParserFinish
from s3p_sdk.plugin.payloads.parsers import S3PParserBase
from s3p_sdk.types import S3PRefer, S3PDocument, S3PPlugin, S3PPluginRestrictions
from s3p_sdk.types.plugin_restrictions import FROM_DATE
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class EMVCo(S3PParserBase):
    """
    Класс парсера плагина SPP

    :warning Все необходимое для работы парсера должно находится внутри этого класса

    :_content_document: Это список объектов документа. При старте класса этот список должен обнулиться,
                        а затем по мере обработки источника - заполняться.


    """

    HOST = "https://www.emvco.com/specifications/"

    def __init__(self,
                 refer: S3PRefer,
                 plugin: S3PPlugin,
                 restrictions: S3PPluginRestrictions,
                 web_driver: WebDriver
                 ):
        super().__init__(refer, plugin, restrictions)

        self._driver = web_driver
        self._wait = WebDriverWait(self._driver, timeout=20)
        ...

    def _parse(self):

        self._initial_access_source("https://www.emvco.com/specifications/", 3)

        while True:
            self.logger.debug('Загрузка списка элементов...')
            doc_table = self._driver.find_element(By.ID, 'filterable_search_results').find_elements(By.CSS_SELECTOR,
                                                                                                    'a.inner-table-sections.specifications')
            self.logger.debug('Обработка списка элементов...')

            # Цикл по всем строкам таблицы элементов на текущей странице
            for element in doc_table:

                available = len(element.find_elements(By.CLASS_NAME, 'available-download')) > 0

                try:
                    title = element.find_element(By.CLASS_NAME, 'title-name').text
                    date_text = element.find_element(By.CLASS_NAME, 'published').text
                    date = dateparser.parse(date_text)
                    web_link = element.get_attribute('data-post-link')
                except Exception as e:
                    self.logger.exception(f'Не удалось извлечь обязательные поля title, link, published. error: {e}')
                    continue

                try:
                    version = element.find_element(By.CLASS_NAME, 'version').text
                except:
                    self.logger.exception('Не удалось извлечь version')
                    version = ' '

                try:
                    tech = element.find_element(By.CLASS_NAME, 'tech-cat').text
                except:
                    self.logger.exception('Не удалось извлечь tech')
                    tech = ' '

                try:
                    doc_type = element.find_element(By.CLASS_NAME, 'spec-cat').text
                except:
                    self.logger.exception('Не удалось извлечь doc_type')
                    doc_type = ' '


                # Новый документ
                doc = S3PDocument(
                    id=None,
                    title=title,
                    abstract=None,
                    text=None,
                    link=web_link,
                    storage=None,
                    other={
                        'doc_type': doc_type,
                        'tech': tech,
                        'version': version,
                        'available': available,
                    },
                    published=date,
                    loaded=None,
                )

                try:
                    self._find(doc)
                except S3PPluginParserOutOfRestrictionException as e:
                    if e.restriction == FROM_DATE:
                        self.logger.debug(f'Document is out of date range `{self._restriction.from_date}`')
                        raise S3PPluginParserFinish(self._plugin,
                                                    f'Document is out of date range `{self._restriction.from_date}`', e)

            try:
                pagination_arrow = self._driver.find_element(By.XPATH, '//a[contains(@data-direction,\'next\')]')
                try:
                    arrow_style = pagination_arrow.get_attribute('style')
                    if arrow_style == 'display: none;':
                        self.logger.info(f'Достигнута последняя страница с невидимой стрелкой next. Прерывание цикла')
                        break
                except:
                    pass

                self._driver.execute_script('arguments[0].click()', pagination_arrow)
                time.sleep(3)
                pg_num = self._driver.find_element(By.ID, 'current_page').text
                self.logger.info(f'Выполнен переход на след. страницу: {pg_num}')
            except:
                self.logger.exception('Не удалось найти переход на след. страницу. Прерывание цикла обработки')
                break

    def _initial_access_source(self, url: str, delay: int = 2):
        self._driver.get(url)
        self.logger.debug('Entered on web page ' + url)
        time.sleep(delay)
        self._agree_cookie_pass()

    def _agree_cookie_pass(self):
        try:
            cookies_btn = self._driver.find_element(By.CLASS_NAME, 'ui-button').find_element(By.XPATH,
                                                                                             '//*[text() = \'Accept\']')
            self._driver.execute_script('arguments[0].click()', cookies_btn)
            self.logger.info('Cookies убран')
        except:
            self.logger.exception('Не найден cookies')

