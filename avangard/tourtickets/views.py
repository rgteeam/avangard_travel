from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from avangard.tourtickets.models import TtOrder
from mailmerge import MailMerge
from avangard import settings


def generate_documents(instance):
    template_filename = "Tourticket_template.docx"
    template = settings.MEDIA_ROOT + "/tourticket_template/" + template_filename
    document = MailMerge(template)
    data_list = list()
    count = 1
    for i in instance.passenger:
        data = {
            'date': i['date'],
            'name': i['name'],
            'citizenship': i['citizenship'],
            'passport': i['passport'],
            'vessel': instance.vessel,
            'tt_number': str(instance.tt_number) + "/" + str(count),
            'service_dates': instance.service_dates
        }
        data_list.append(data)
        count += 1
    document.merge_pages(data_list)
    output_filename = str(instance.id) + "_" + str(instance.sender_name) + ".docx"
    output_path = settings.MEDIA_ROOT + "tourticket_exported/" + output_filename
    document.write(output_path)
    return output_path


@login_required
def tourtickets_index(request):
    if request.method == 'GET':
        all_tt = TtOrder.objects.all()
        context = {"all_tt": all_tt}
        return render(request, 'tourtickets.html', context)


@login_required
def tourtickets_edit(request, tt_id):
    if request.method == 'GET':
        instance = TtOrder.objects.get(id=tt_id)
        context = {"instance": instance}
        return render(request, 'edit_tourticket.html', context)
    elif request.method == 'POST':
        instance = TtOrder.objects.get(id=tt_id)
        context = {"instance": instance, "notification": "Информация о заявке была обновлена"}
        updated_status = request.POST.get("status")
        instance.status = updated_status
        instance.save()
        return render(request, 'edit_tourticket.html', context)


@login_required
def tourtickets_create(request, tt_id):
    instance = get_object_or_404(TtOrder, id=tt_id)
    if request.method == "GET":
        context = {"instance": instance}
        return render(request, 'create.html', context)
    elif request.method == "POST":
        tt_number = request.POST.get('tt_number', '')
        vessel = request.POST.get('vessel', '')
        service_dates = request.POST.get('service_dates', '')
        instance.tt_number = tt_number
        instance.vessel = vessel
        instance.service_dates = service_dates
        instance.save()
        document_link = generate_documents(instance)
        context = {"document": document_link}
        return render(request, 'download_tourticket.html', context)


@login_required
def tourtickets_delete(request, tt_id):
    isntance = TtOrder.objects.get(id=tt_id)
    isntance.delete()
    return redirect('tourtickets_index')
