from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from avangard.proxycard.models import PcOrder
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
    output_filename = str(instance.id) + "_" + "driver" + "_" + str(instance.sender_name) + ".docx"
    output_path = settings.MEDIA_ROOT + "tourticket_exported/" + output_filename
    document.write(output_path)
    return output_path


@login_required
def proxycard_index(request):
    if request.method == 'GET':
        all_pc = PcOrder.objects.all()
        context = {"all_pc": all_pc}
        return render(request, 'proxycards.html', context)


@login_required
def proxycard_edit(request, pc_id):
    if request.method == 'GET':
        instance = PcOrder.objects.get(id=pc_id)
        context = {"instance": instance}
        return render(request, 'edit_proxycard.html', context)
    elif request.method == 'POST':
        instance = PcOrder.objects.get(id=pc_id)
        context = {"instance": instance, "notification": "Информация о заявке была обновлена"}
        updated_status = request.POST.get("status")
        instance.status = updated_status
        instance.save()
        return render(request, 'edit_proxycard.html', context)


@login_required
def proxycard_create(request, pc_id):
    instance = get_object_or_404(PcOrder, id=pc_id)
    if request.method == "GET":
        context = {"instance": instance}
        return render(request, 'create_proxycard.html', context)
    elif request.method == "POST":
        tt_number = request.POST.get('tt_number', '')
        vessel = request.POST.get('vessel', '')
        service_dates = request.POST.get('arrival_date', '')
        instance.tt_number = tt_number
        instance.vessel = vessel
        instance.arrival_date = arrival_date
        instance.save()
        document_link = generate_documents(instance)
        context = {"document": document_link}
        return render(request, 'download_proxycard.html', context)


@login_required
def proxycard_delete(request, pc_id):
    isntance = PcOrder.objects.get(id=pc_id)
    isntance.delete()
    return redirect('proxycard_index')
