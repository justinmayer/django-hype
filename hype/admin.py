from django.contrib import admin

from . import models


@admin.register(models.ReferralLink)
class ReferralLinkAdmin(admin.ModelAdmin):
	list_display = ("identifier", "user", "disabled", "created", "updated")
	list_filter = ("disabled", )
	raw_id_fields = ("user", )
	search_fields = ("user__username", "identifier")


@admin.register(models.ReferralHit)
class ReferralHitAdmin(admin.ModelAdmin):
	list_display = (
		"id", "referral_link", "next", "hit_user", "authenticated", "ip", "created", "updated"
	)
	list_filter = ("authenticated", )
	raw_id_fields = ("referral_link", "hit_user")
	search_fields = ("id", "referral_link__identifier")

	def has_add_permission(self, request):
		return False
