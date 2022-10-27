def test_load_admin(admin_client):
	response = admin_client.get("/admin/hype/")
	assert response.status_code == 200

	response = admin_client.get("/admin/hype/referrallink/")
	assert response.status_code == 200

	response = admin_client.get("/admin/hype/referralhit/")
	assert response.status_code == 200
