from django_cron import CronJobBase, Schedule

from tnpm.models.admin import ProfileHelper,FormulaHelper
from tnpm.models.tnpm import ElmtDesc,FrmlDesc


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'

    def do(self):
        obj_profile = {obj.str_profile for obj in ElmtDesc.objects.using('tnpm').all()}
        profile_list = {profile.str_profile for profile in ProfileHelper.objects.all()}

        obj_formuls = {obj.str_name for obj in FrmlDesc.objects.using('tnpm').all()}
        formuls_list = {fm.str_name for fm in FormulaHelper.objects.all()}

        add_new = [val for val in obj_profile if val not in profile_list]
        remove_old = [val for val in profile_list if val not in obj_profile]

        add_new_fm = [val for val in obj_formuls if val not in formuls_list]
        remove_old_fm = [val for val in formuls_list if val not in formuls_list]

        for prof in add_new:
            ProfileHelper(str_profile=prof).save()

        for prof in remove_old:
            ProfileHelper.objects.get(str_profile=prof).delete()

        for name in add_new_fm:
            FormulaHelper(str_name=name).save()

        for name in remove_old_fm:
            FormulaHelper.objects.get(str_name=name).delete()


        theJob()