from django.contrib import admin

from models import FilmSearch, Films, Developers, Notes, ItemStorage


class FilmSearchAdmin(admin.ModelAdmin):
    list_display = (
        "Film", "Developer", "Dilution", "ASA_ISO", "create_timestamp", "last_update_timestamp",
    )

    list_filter = (
        "Film",
    )


class FilmsAdmin(admin.ModelAdmin):
    list_display = (
        "Film", "create_timestamp", "last_update_timestamp",
    )

    list_filter = (
        "Film",
    )


class DevelopersAdmin(admin.ModelAdmin):
    list_display = (
        "Developer", "create_timestamp", "last_update_timestamp",
    )

    list_filter = (
        "Developer",
    )


class NotesAdmin(admin.ModelAdmin):
    list_display = (
        "Notes", "Remark", "create_timestamp", "last_update_timestamp",
    )

    list_filter = (
        "Notes",
    )


class ItemStorageAdmin(admin.ModelAdmin):
    list_display = (
        "ItemTitle", "ItemShopName", "ItemPrice", "ItemTaoBaoPrice", "last_update_timestamp"
    )

    list_filter = (
        "ItemShopName",
    )


admin.site.register(FilmSearch, FilmSearchAdmin)
admin.site.register(Films, FilmsAdmin)
admin.site.register(Developers, DevelopersAdmin)
admin.site.register(Notes, NotesAdmin)
admin.site.register(ItemStorage, ItemStorageAdmin)
