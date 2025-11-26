from django.db import migrations


def create_custom_fields(apps, schema_editor):
    CustomField = apps.get_model('extras', 'CustomField')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    custom_fields = [
        {
            'name': 'pam_ssh_keys',
            'type': 'json',
            'label': 'SSH Keys',
            'group_name': 'NetBox PAM',
            'description': 'List of public SSH keys attached to this Contact',
            'object_types': ['tenancy.contact'],
            'unique': False,
            'ui_editable': 'yes',
        },
        {
            'name': 'pam_jc_id',
            'type': 'text',
            'label': 'Jumpcloud ID',
            'group_name': 'NetBox PAM',
            'description': 'ID representation of this object in Jumpcloud',
            'object_types': [
                'dcim.device',
                'tenancy.contact',
                'netbox_pam.devicegroup',
                'netbox_pam.usergroup',
                'virtualization.virtualmachine',
            ],
            'unique': True,
            'ui_editable': 'no',
        },
    ]

    for field_def in custom_fields:
        cf, created = CustomField.objects.get_or_create(
            name=field_def['name'],
            defaults={
                'type': field_def['type'],
                'label': field_def['label'],
                'group_name': field_def['group_name'],
                'description': field_def['description'],
                'unique': field_def['unique'],
                'ui_editable': field_def['ui_editable'],
            },
        )

        cts = []
        for ot in field_def["object_types"]:
            app_label, model = ot.split(".")
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model)
                cts.append(ct.pk)
            except ContentType.DoesNotExist:
                print(f"Warning: ContentType {ot} not found, skipping")

        cf.object_types.set(cts)
        cf.save()

        print(f"{'Created' if created else 'Skipped existing'} custom field: {cf.name}")

def delete_custom_fields(apps, schema_editor):
    CustomField = apps.get_model('extras', 'CustomField')
    for name in ["pam_ssh_keys", "pam_jc_id"]:
        CustomField.objects.filter(name=name).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('netbox_pam', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_custom_fields, delete_custom_fields),
    ]
