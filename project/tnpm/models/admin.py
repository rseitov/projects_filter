# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import IntegerField
from django.db.models.functions import Cast

from .tnpm import PropDesc, SeDesc, ElmtDesc


CHOICE_IGNORE = None
CHIOCE_LIKE = 'LIKE'
CHOICE_LIKE_VALUE = 'LIKE.__icontains'

CHOICE_NOT_LIKE = 'NOT LIKE'
CHOICE_NOT_LIKE_VALUE = 'NOT LIKE.'
CHOICE_IN = 'IN'
CHOICE_NOT_IN = 'NOT IN'
CHOICE_EQUAL = '='
CHOICE_EQUAL_VALUE = '=.'
CHOICE_NOT_EQUAL = '!='
CHOICE_NOT_EQUAL_VALUE = '!=.'
CHOICE_GT = '>'
CHOICE_GT_VALUE = '>.__gt'
CHOICE_LT = '<'
CHOICE_LT_VALUE = '<.__lt'
IGNORE_CHOICE_LBL = 'Ignore'
IGNORE_CHOICE = (
    (CHOICE_IGNORE, IGNORE_CHOICE_LBL),
)
IN_CHOICES = (
    (CHOICE_IN, CHOICE_IN),
    (CHOICE_NOT_IN, CHOICE_NOT_IN),
)
EQUAL_CHOICES = (
    (CHOICE_EQUAL_VALUE, CHOICE_EQUAL),
    (CHOICE_NOT_EQUAL_VALUE, CHOICE_NOT_EQUAL),
)
GTLT_CHOICES = (
    (CHOICE_GT_VALUE, CHOICE_GT),
    (CHOICE_LT_VALUE, CHOICE_LT),
)
LIKE_CHOICES = (
    (CHOICE_LIKE_VALUE, CHIOCE_LIKE),
    (CHOICE_NOT_LIKE_VALUE, CHOICE_NOT_LIKE),
)

# Lookup scenario description
DISCARD_METRIC_NAME_HELP = '''Опционально, будут отброшены только трапы указанной метрики'''

LOOKUP_TYPE_DISCARD = 'discard'
LOOKUP_TYPE_LOW_TRAFFIC = 'low_traffic'
LOOKUP_TYPE_ENRICH_PROFILE = 'enrich_profile'
LOOKUP_TYPES = (
    (
        LOOKUP_TYPE_DISCARD,
        'Отброс трапов по выбранным ресурсам',
        '   Будут отброшены трапы от ресурсов, удовлетворябщих условиям фильтров',
    ),
    (
        LOOKUP_TYPE_LOW_TRAFFIC,
        'Обогащение/отброс трапов по условию "низкого трафика"',
        '   Выгрузка данных будет сформирована на основании таблицы VM_INTFWTRAFFIC. ' + \
        'Механизм сработает только для трапов, ID метрики которых содержится в выгрузке. ' + \
        'В событие будет добавлено значение среднесуточного трафика, IN/OUT в зависимости ' + \
        'от ID метрики. Если искомой комбинация ID ресурса + ID метрики нет в выгрузке, трап ' + \
        'будет отброшен.',
    ),
    (
        LOOKUP_TYPE_ENRICH_PROFILE,
        'Обогащение трапов данными о профиле',
        '   В событие будет добавлено имя профиля, к которому относится ресурс',
    ),
)
LOOKUP_TYPE_CHOICES = tuple(
    choice[:2] for choice in LOOKUP_TYPES
)
LOOKUP_TYPE_HELP = '\n\n'.join(
    '{}:\n{}'.format(choice[1], choice[2]) for choice in LOOKUP_TYPES
)

def filter_set(se_set, prop_fild, prop_exlud):
    all_idx_resource = set()
    if len(prop_fild) == 0 and len(prop_exlud) != 0:
        filter_and_extend = se_set - prop_exlud
        all_idx_resource = filter_and_extend
    elif len(prop_exlud) == 0 and len(prop_fild) != 0:
        filter_and_extend = se_set & prop_fild
        all_idx_resource = filter_and_extend
    elif len(prop_fild) != 0 and len(prop_exlud) != 0:
        filter_and_extend = prop_fild - prop_exlud
        filter_and_extend = se_set & filter_and_extend
        all_idx_resource = filter_and_extend

    return all_idx_resource


def query_builder(query_array: list) -> dict:
    excluded = []
    filtered = []
    for query_element in query_array:
        for key, val in query_element.items():
            if 'NOT LIKE' in key or '!=' in key:
                excluded.append(val)
            else:
                filtered.append(val)

    excluded_query = {}
    filtered_query = {}
    for excluded_el in excluded:
        for key, val in excluded_el.items():
            new_key = key + '__in'

            if key in excluded_query:
                old_value = excluded_query[key]
                if isinstance(old_value, list):
                    if val not in old_value:
                        old_value.append(val)
                else:
                    if val != old_value:
                        new_val = [old_value, val]
                        excluded_query[new_key] = excluded_query.pop(key)
                        excluded_query[new_key] = new_val
            elif new_key in excluded_query:
                arr = filtered_query[new_key]
                arr.append(val)
                excluded_query[new_key] = arr
            else:
                excluded_query[key] = val

    for filtered_el in filtered:
        for key, val in filtered_el.items():
            new_key = key + '__in'
            if key in filtered_query:
                old_value = filtered_query[key]
                if isinstance(old_value, list):
                    if val not in old_value:
                        old_value.append(val)
                else:
                    if val != old_value:
                        new_val = [old_value, val]
                        filtered_query[new_key] = filtered_query.pop(key)
                        filtered_query[new_key] = new_val

            elif new_key in filtered_query:
                arr = filtered_query[new_key]
                arr.append(val)
                filtered_query[new_key] = arr
            else:
                filtered_query[key] = val

    queries = {
        'excluded': excluded_query,
        'filtered': filtered_query
    }
    return queries



class FormulaHelper(models.Model):
    str_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.str_name


class ProfileHelper(models.Model):
    '''
    Distinct TNPM profile names for drop-down list
    '''
    str_profile = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.str_profile


class TnpmTrapLookupRules(models.Model):
    '''
    Contains rules for generate Netcool probe lookup files.
    Each rule is set of element filters and check box to activate hardcoded lookup scenario
    '''

    name = models.CharField(
        max_length=200,
        verbose_name=('Имя правила'),
    )
    description = models.TextField(
        max_length=500,
        verbose_name=('Описание'),
    )
    is_enabled = models.BooleanField(
        verbose_name=('Включить'),
        default=False,
        help_text=('Включение/Выключение , для записи в lookup')
    )

    profile = models.ForeignKey(
        ProfileHelper,
        on_delete=models.CASCADE,
        verbose_name=('Выбор профиля'),
    )
    metric_name = models.CharField(
        verbose_name='Имя метрики',
        max_length=200,
        default=False,
        null=True,
        help_text=DISCARD_METRIC_NAME_HELP,
    )

    lookup_type = models.CharField(
        max_length=50,
        verbose_name=('Имя свойства'),
        choices=LOOKUP_TYPE_CHOICES,
        default=LOOKUP_TYPE_CHOICES[0],
        help_text=LOOKUP_TYPE_HELP,
    )

    _resouce_ids = None

    def get_resource_ids(self):
        '''
        Returns IDs (memoized) of TNPM resource that satisfy filter
        conditions of the current rule
        '''
        if self._resouce_ids is not None:
            return self._resouce_ids

        propertys = self.tnpmelementfilter_set.all()
        profile_name = self.profile
        element = ElmtDesc.objects.using('tnpm').filter(str_profile=profile_name)

        elementDesc = []
        for i in element:
            elementDesc.append(i.idx_ind)

        subElementList = set()
        selected_subelement = SeDesc.objects.using('tnpm').filter(idx_host__in=elementDesc)
        for sub in selected_subelement:
            subElementList.add(sub.idx_ind)
        query_options = []

        for i in propertys:
            query_options.append({
                "property": i.prop_name.str_name,
                "operator": i.prop_compare,
                "value": i.prop_value
            })

        generic_query = []
        generic_query2 = []
        prop_fild_set = set()
        prop_exlud_set = set()
        for el in query_options:
            value = el['value']
            property_name = el['property']
            operator_split = el['operator'].split('.')
            operator_name = operator_split[0]
            operator_field = operator_split[1]

            select_name = 'idx_metric__str_name'

            if value.isdigit():

                select_value = 'as_integer' + operator_field

                value = int(value)

                generic_value = {operator_name: {
                    select_name: property_name,
                    select_value: value
                }}
                generic_query.append(generic_value)
            else:
                select_value = 'str_value' + operator_field

                generic_value_2 = {
                    operator_name: {
                        select_name: property_name,
                        select_value: value
                    }
                }

                generic_query2.append(generic_value_2)

        new_generic_query = query_builder(generic_query)
        new_generic_query_2 = query_builder(generic_query2)

        selected = PropDesc.objects.using('tnpm').filter(str_value__iregex=r'^[0-9]*$')
        value = selected.annotate(as_integer=Cast('str_value', IntegerField()))

        if new_generic_query['filtered']:
            prop_filter = value.filter(**new_generic_query['filtered'])

            for i in prop_filter:
                prop_fild_set.add(i.idx_resource)

        if new_generic_query['excluded']:
            prop_excluded = value.filter(**new_generic_query['excluded'])
            for i in prop_excluded:
                prop_exlud_set.add(i.idx_resource)

        if new_generic_query_2['filtered']:
            prop_str = PropDesc.objects.using('tnpm').filter(**new_generic_query_2['filtered'])
            for i in prop_str:
                prop_fild_set.add(i.idx_resource)

        if new_generic_query_2['excluded']:
            prop_str_exlud = PropDesc.objects.using('tnpm').filter(**new_generic_query_2['excluded'])
            for i in prop_str_exlud:
                prop_exlud_set.add(i.idx_resource)

        prop_filter = filter_set(subElementList, prop_fild_set, prop_exlud_set)
        prop_filter = list(prop_filter)
        self._resouce_ids = set(prop_filter)
        return self._resouce_ids


class TnpmElementFilter(models.Model):
    '''
    Element filter conditions
    '''
    connect = models.ForeignKey(
        TnpmTrapLookupRules,
        on_delete=models.CASCADE
    )
    prop_name = models.ForeignKey(FormulaHelper, on_delete=models.CASCADE, verbose_name=('Поле автозаполнения'))

    prop_compare = models.CharField(
        max_length=50,
        verbose_name=('Условие сранения'),
        choices=IGNORE_CHOICE + EQUAL_CHOICES + LIKE_CHOICES + GTLT_CHOICES,
        default=CHOICE_IGNORE,
        null=True,
        blank=True,
    )
    prop_value = models.CharField(
        verbose_name=('Значение'),
        max_length=255,
        null=True,
        blank=True,
        help_text=('Значения поля')
    )

#для теста создан
class ProbeManager(models.Model):
    manager_name = models.CharField(max_length=64, db_column='Manager_Name', unique=True, verbose_name='Manager')
    manager_server = models.CharField(max_length=64, db_column='Manager_Server', null=False)
    filter_file_path = models.CharField(max_length=254, db_column='Filter_File_Path', null=False)
    sftp_user_name = models.CharField(max_length=64, db_column='Sftp_user_name', null=False)
    sftp_password = models.CharField(max_length=64, db_column='Sftp_password', null=False)
    backup_server_ip = models.CharField(max_length=64, db_column='Backup_Server_IP', blank=True)
    http_port = models.CharField(max_length=50, db_column='HTTP_Port', blank=False, null=False)
    http_username = models.CharField(max_length=50, db_column='HTTP_username', blank=False, null=False)
    http_password = models.CharField(max_length=50, db_column='HTTP_password', blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_updated = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(verbose_name=('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name=('last updated at'), auto_now=True, editable=False)

    class Meta:
        db_table = 'probemanager'
        verbose_name = ('probe manager')
        verbose_name_plural = ('probe managers')

    def __str__(self):
        return self.manager_name


class TnpmProbeManager(models.Model):
    manager = models.OneToOneField(ProbeManager, on_delete=models.CASCADE, primary_key=True, )
