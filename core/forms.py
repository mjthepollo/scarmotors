from django import forms
from django.utils.safestring import mark_safe


def change_input_to_readonly(div):
    changed_div = div
    input_index, input_finish_index = 0, 0
    while True:
        input_index = changed_div.find("<input", input_finish_index)
        if input_index == -1:
            break
        input_finish_index = changed_div.find(">", input_index)
        if 'type="checkbox"' in changed_div[input_index:input_finish_index]:
            changed_div = changed_div[:input_finish_index] + \
                " disabled" + changed_div[input_finish_index:]
        else:
            changed_div = changed_div[:input_finish_index] + \
                " readonly" + changed_div[input_finish_index:]

    return changed_div


def change_input_to_disabled(div):
    changed_div = div
    input_index, input_finish_index = 0, 0
    while True:
        input_index = changed_div.find("<input", input_finish_index)
        if input_index == -1:
            break
        input_finish_index = changed_div.find(">", input_index)
        changed_div = changed_div[:input_finish_index] + \
            " disabled" + changed_div[input_finish_index:]
    return changed_div


def change_textarea_to_readonly(div):
    changed_div = div
    textarea_index, textarea_finish_index = 0, 0
    while True:
        textarea_index = changed_div.find("<textarea", textarea_finish_index)
        if textarea_index == -1:
            break
        textarea_finish_index = changed_div.find(">", textarea_index)
        changed_div = changed_div[:textarea_finish_index] + \
            " readonly" + changed_div[textarea_finish_index:]
    return changed_div


def change_textarea_to_disabled(div):
    changed_div = div
    textarea_index, textarea_finish_index = 0, 0
    while True:
        textarea_index = changed_div.find("<textarea", textarea_finish_index)
        if textarea_index == -1:
            break
        textarea_finish_index = changed_div.find(">", textarea_index)
        changed_div = changed_div[:textarea_finish_index] + \
            " disabled" + changed_div[textarea_finish_index:]
    return changed_div


def change_select_to_readonly(div, form):
    changed_div = div
    select_index, select_finish_index = 0, 0
    while True:
        select_index = changed_div.find("<select", select_index+1)
        if select_index == -1:
            break
        name_tag = 'name="'
        name_index = changed_div.find(name_tag, select_index)
        name_finish_index = changed_div.find('"', name_index+len(name_tag))
        field_name = changed_div[name_index+len(name_tag):name_finish_index]
        for field in form.fields:
            if field in field_name:
                value = form[field].value() if form[field].value() else "-"
        replaced_field = f'<input type="text" value="{value}" readonly>'
        select_finish_index = changed_div.find(
            "</select>", select_index) + len("</select>")
        changed_div = changed_div[:select_index] + replaced_field +\
            changed_div[select_finish_index:]
    return changed_div


def changed_select_to_disabled(div):
    changed_div = div
    select_index, select_finish_index = 0, 0
    while True:
        select_index = changed_div.find("<select", select_finish_index)
        if select_index == -1:
            break
        select_finish_index = changed_div.find(">", select_index)
        changed_div = changed_div[:select_finish_index] + " disabled" +\
            changed_div[select_finish_index:]
    return changed_div


def make_disabled(form):
    changed_div = form.as_div()
    changed_div = change_input_to_disabled(changed_div)
    changed_div = change_textarea_to_disabled(changed_div)
    changed_div = changed_select_to_disabled(changed_div)
    return changed_div


def make_read_only(form):
    changed_div = form.as_div()
    changed_div = change_input_to_readonly(changed_div)
    changed_div = change_textarea_to_readonly(changed_div)
    changed_div = change_select_to_readonly(changed_div, form)
    return changed_div


class DetailableModelForm(forms.ModelForm):
    def detail_as_div(self, *args, **kwargs):
        return mark_safe(make_disabled(self))

    def get_div(self, user):
        if user.editable:
            return self.as_div()
        return self.detail_as_div()
