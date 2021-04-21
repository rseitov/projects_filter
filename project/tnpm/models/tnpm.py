# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models


TNPM_DATABASE_ALIAS = 'tnpm'


class TnpmConnectManager(models.Manager):
    '''
    Uses TNPM_DATABASE_ALIAS for connection instead of default db
    '''

    def get_queryset(self):
        return super(TnpmConnectManager, self).get_queryset().using(TNPM_DATABASE_ALIAS)


class RefDesc(models.Model):
    ncl_idx_ind = models.IntegerField(primary_key=True)
    ncl_str_name = models.CharField(max_length=80, blank=True, null=True)
    ncl_str_type = models.CharField(max_length=32, blank=True, null=True)
    str_origin = models.CharField(max_length=80, blank=True, null=True)
    str_user = models.CharField(max_length=80, blank=True, null=True)
    ncl_str_oid = models.CharField(max_length=80, blank=True, null=True)

    objects = TnpmConnectManager()

    class Meta:
        managed = False
        db_table = 'ref_desc'
        unique_together = (('ncl_str_oid', 'ncl_str_name'),)


class ProbeType(models.Model):
    idx_ind = models.IntegerField(primary_key=True)
    str_name = models.CharField(max_length=80, blank=True, null=True)
    str_description = models.CharField(max_length=255, blank=True, null=True)
    str_invariant_def = models.CharField(
        max_length=1000, blank=True, null=True)
    str_class = models.CharField(max_length=30, blank=True, null=True)
    int_date = models.IntegerField(blank=True, null=True)
    str_origin = models.CharField(max_length=80, blank=True, null=True)
    str_user = models.CharField(max_length=80, blank=True, null=True)

    objects = TnpmConnectManager()

    class Meta:
        managed = False
        db_table = 'probe_type'


class ProbeDesc(models.Model):
    idx_ind = models.IntegerField(primary_key=True)
    idx_resource = models.ForeignKey(
        'SeDesc', models.DO_NOTHING, db_column='idx_resource', blank=True, null=True)
    str_invariant = models.CharField(max_length=255, blank=True, null=True)
    idx_probe_type = models.ForeignKey(
        'ProbeType', models.DO_NOTHING, db_column='idx_probe_type', blank=True, null=True)
    int_date = models.IntegerField(blank=True, null=True)
    str_origin = models.CharField(max_length=80, blank=True, null=True)
    str_user = models.CharField(max_length=80, blank=True, null=True)

    objects = TnpmConnectManager()

    class Meta:
        managed = False
        db_table = 'probe_desc'


class FrmlPropertyManager(TnpmConnectManager):
    '''
    Returns formulas for (sub)elemets properties only
    '''

    def get_queryset(self):
        return super(FrmlPropertyManager, self).get_queryset()\
            .filter(str_type='property')


class FrmlMetricManager(TnpmConnectManager):
    '''
    Returns formulas for (sub)elemets metrics (all except properties)
    '''

    def get_queryset(self):
        return super(FrmlMetricManager, self).get_queryset()\
            .exclude(str_type='property')

    def get_by_id(self, metric_id):
        '''
        Returns metric object or None if given ID does not exists
        '''
        try:
            return self.get_queryset().filter(idx_ind=metric_id)[0]
        except IndexError:
            return None

    def find_id_by_name(self, metric_name):
        '''
        Returns idx_ind of metric or -1 if metric with given name 
        does not exists
        '''
        try:
            metric_id = self.get_queryset()\
                .filter(str_name=metric_name)\
                .values_list('idx_ind', flat=True)[0]
        except IndexError:
            metric_id = -1

        return metric_id


class FrmlDesc(models.Model):
    '''
    Contains formula definitions - rules to fetch properties or metrics
    '''
    idx_ind = models.IntegerField(primary_key=True)
    str_name = models.CharField(max_length=80, blank=True, null=True)
    str_type = models.CharField(max_length=32, blank=True, null=True)

    objects = TnpmConnectManager()
    properties = FrmlPropertyManager()
    metrics = FrmlMetricManager()

    class Meta:
        managed = False
        db_table = 'frml_desc'


class ElmtDesc(models.Model):
    '''
    Contains elements - network devices
    '''
    idx_ind = models.IntegerField(primary_key=True)
    str_name = models.CharField(
        unique=True, max_length=80, blank=True, null=True)
    str_state = models.CharField(max_length=3, blank=True, null=True)
    str_origin = models.CharField(max_length=32, blank=True, null=True)
    int_date = models.IntegerField(blank=True, null=True)
    str_profile = models.CharField(max_length=255, blank=True, null=True)
    ncl_idx_ind = models.ForeignKey(
        'RefDesc', models.DO_NOTHING, db_column='ncl_idx_ind', blank=True, null=True)
    str_type = models.CharField(max_length=32, blank=True, null=True)
    str_comment = models.CharField(max_length=4000, blank=True, null=True)
    str_user = models.CharField(max_length=32, blank=True, null=True)
    int_collector = models.IntegerField(blank=True, null=True)
    int_inv_miss_cnt = models.IntegerField(blank=True, null=True)

    objects = TnpmConnectManager()

    class Meta:
        managed = False
        db_table = 'elmt_desc'


class SeManager(TnpmConnectManager):
    '''
    Provides additional methods for SeDesc - ElmtDesc relation
    '''

    def get_se_profiles(self):
        '''
        Returns (resouceid, profile name) pairs for all SE
        '''
        return self.get_queryset().values_list('idx_ind', 'idx_host__str_profile')

    def iter_se_profiles(self):
        '''
        Returns iterator fr list of (resouceid, profile name) pairs (all SE)
        '''
        return self.get_queryset()\
            .values_list('idx_ind', 'idx_host__str_profile')\
            .iterator()


class SeDesc(models.Model):
    '''
    Contains subelements - interfaces or any other entity related to elements
    '''
    idx_ind = models.IntegerField(primary_key=True)
    idx_host = models.ForeignKey(
        ElmtDesc, models.DO_NOTHING, db_column='idx_host', blank=True, null=True)
    str_alias = models.CharField(max_length=255, blank=True, null=True)
    str_state = models.CharField(max_length=3, blank=True, null=True)
    str_name = models.CharField(max_length=255, blank=True, null=True)
    str_ulabel = models.CharField(max_length=255, blank=True, null=True)
    idx_formula = models.IntegerField(blank=True, null=True)
    idx_formula_group = models.IntegerField(blank=True, null=True)
    ncl_idx_ind = models.ForeignKey(
        RefDesc, models.DO_NOTHING, db_column='ncl_idx_ind', blank=True, null=True)
    str_type = models.CharField(max_length=80, blank=True, null=True)
    str_type_data = models.CharField(max_length=80, blank=True, null=True)
    str_instance = models.CharField(max_length=255, blank=True, null=True)
    int_date = models.IntegerField(blank=True, null=True)
    str_invariant = models.CharField(max_length=140, blank=True, null=True)
    str_profile = models.CharField(max_length=255, blank=True, null=True)
    idx_rule = models.IntegerField(blank=True, null=True)
    str_origin = models.CharField(max_length=80, blank=True, null=True)
    str_user = models.CharField(max_length=80, blank=True, null=True)
    str_comment = models.CharField(max_length=1000, blank=True, null=True)

    objects = SeManager()

    class Meta:
        managed = False
        db_table = 'se_desc'


class PropDesc(models.Model):
    '''
    Contains properties of all recources (elements and subelements).
    Each record is single property (name-value pair) related to resource
    '''
    idx_resource = models.IntegerField(primary_key=True)
    idx_metric = models.ForeignKey(
        FrmlDesc,
        models.DO_NOTHING,
        db_column='idx_metric',
        to_field='idx_ind',
    )
    str_origin = models.CharField(max_length=80, blank=True, null=True)
    str_user = models.CharField(max_length=80, blank=True, null=True)
    dte_date = models.IntegerField(blank=True, null=True)
    str_value = models.CharField(max_length=275, blank=True, null=True)

    objects = TnpmConnectManager()

    class Meta:
        managed = False
        db_table = 'prop_desc'
        unique_together = (('idx_resource', 'idx_metric'),)


class Mtrc001dra000h0Manager(TnpmConnectManager):
    '''
    Provides additional methods for working with aggregates
    '''

    def iter_avgbps_1d_metrics(self):
        '''
        Returns list of metric IDs (distinct) associated with IN/OUT traffic in Bps
        '''
        # TODO replace original table with matview,
        # so we could fetch all rows without any filter
        filters = {
            'idx_metric__in': (2208, 2209),
            'dte_max__gt': int(
                (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
            ),
            'dbl_max__gt': 1000000,
        }

        return self.get_queryset()\
            .filter(**filters)\
            .values_list('idx_metric', flat=True)\
            .distinct().iterator()


    def iter_avgbps_1d(self):
        '''
        Returns iterator, for IN and OUT traffic in Bps.
        Each record contains (resourceid, metricid, avgBps) values
        '''
        # TODO replace original table with matview,
        # so we could fetch all rows without any filter
        filters = {
            'idx_metric__in': (2208, 2209),
            'dte_max__gt': int(
                (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
            ),
            'dbl_max__gt': 1000000,
        }

        return self.get_queryset()\
            .filter(**filters)\
            .values_list('idx_resource', 'idx_metric', 'dbl_max')\
            .iterator()


class Mtrc001dra000h0(models.Model):
    '''
    Contains day agg metrics for resources
    '''
    idx_resource = models.IntegerField(primary_key=True)
    idx_metric = models.IntegerField()
    dbl_max = models.FloatField()
    dte_max = models.IntegerField()

    objects = Mtrc001dra000h0Manager()

    class Meta:
        managed = False
        db_table = '"PV_METRIC"."MTRC00_1DRA_000_H0"'
        unique_together = (('idx_resource', 'idx_metric'),)
