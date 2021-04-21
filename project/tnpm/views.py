from tnpm.models.tnpm import  SeDesc
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def create_sub(request, id):

    from tnpm.models import TnpmTrapLookupRules
    lookup = TnpmTrapLookupRules.objects.get(pk=id)

    prop_filter = lookup.get_resource_ids()

    if len(prop_filter) == 0:
        return render(request, 'subelement_list.html')

    selected_se_desc = SeDesc.objects.using('tnpm').filter(idx_ind__in=prop_filter)

    paginator = Paginator(selected_se_desc, 10)

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:

        contacts = paginator.page(1)
    except EmptyPage:

        contacts = paginator.page(paginator.num_pages)

    result_values = {
        'id':lookup.id,
        'contacts': contacts
    }
    args = {'values': result_values}

    return render(request, 'subelement_list.html', args)

