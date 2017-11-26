def test_load_admin(admin_client):
	response = admin_client.get("/admin/django_reflinks/")
	assert response.status_code == 200

	response = admin_client.get("/admin/django_reflinks/referrallink/")
	assert response.status_code == 200

	response = admin_client.get("/admin/django_reflinks/referralhit/")
	assert response.status_code == 200
