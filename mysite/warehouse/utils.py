from django.utils.text import slugify
from django.core.exceptions import ValidationError
from time import time
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.utils import timezone

from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger

def gen_slug(s):
    s.lower() 
    format_string = slugify(s, allow_unicode=True)
    s_translate = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', '0': '0', '1': '1', '2': '2',
        '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'
        }

    s_encode = []

    for i in format_string:
        try:
            if i == '-' or i == '_':
                s_encode.append(i)
            s_encode.append(s_translate.get(i, i))
                #s_encode.append(s_translate[i])
        except:
            raise ValidationError("Slug can't be generated!")
    new_slug = ''.join(map(str, s_encode))
    return new_slug + '-' + str(int(time()))


class PaginatorMixin:
    def create_pagination(self, **kwargs):
        kwargs = kwargs.get('kwargs')
        
        paginator = Paginator(kwargs.get('object'), 25)
        pages = kwargs.get('request').GET.get('page')
        pag_range = paginator.page_range

        try:
            count_objects = paginator.page(pages)

        except PageNotAnInteger:
            count_objects = paginator.page(1)

        values = {
            'counter': count_objects,
            'pag_range': pag_range,
        }

        return values


class ObjectCreateMixin:

    model_form = None
    model = None
    template = None
    war_model = None

    def get(self, request):
        warehouses = self.war_model.objects.all()
        main_object = self.model.objects.filter(date_pub__lte=timezone.now()).order_by('-date_pub')
        form = self.model_form

        
        return render(request, self.template, context={
            "object_create_form": form,
            self.model.__name__.lower(): main_object,
            self.war_model.__name__.lower(): warehouses
        })

    def post(self, request):
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            new_object = bound_form.save()
            request.session.update({
                'success_update': True
            })

            print("SESSION ADD SUCCESS: ", request.session.get('success_update'))

            return redirect(new_object)

        return render(request, self.template, context={"object_create_form": bound_form})


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):

        object = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=object)
        all_warehouses = self.model.objects.filter(date_pub__lte=timezone.now()).order_by('-date_pub')

        return render(request, self.template, context={
            'war_create_form': bound_form,
            self.model.__name__.lower(): all_warehouses,
        })
    

    def post(self, request, slug):
        old_object = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=old_object)

        if bound_form.is_valid():
            new_object = bound_form.save()

            return redirect(new_object)

        return render(request, self.template, context={"war_create_form": bound_form})


class ObjectDeleteMixin:
    template = None

    def get_to_delete(self, request, slug, model):
        get_object = get_object_or_404(model, slug__iexact=slug)

        return render(request, self.template, locals())


    def post_to_delete(self, request, slug, model):

        if request.POST:
            if request.POST.get('delete_confirm') == 'Delete':
                get_object = get_object_or_404(model, slug__iexact=slug)
                get_object.delete()

            else:
                model_str = model.__name__.lower()
                # request.POST.update({'model': model_str})
        
                return render(request, self.template, context={
                    'not_delete': True
                })

        # get_object.save()

        return redirect('my_warehouse_url')