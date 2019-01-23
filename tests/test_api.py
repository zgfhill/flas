class APITestCase(unittest.TestCase):
	def get_api_headers(self, username, password):
		return {'Authorization': 'Basic' + b64encode((username + ':' + password).encode()).decode(), 'Accept': 'application/json', 'Content-Type': 'application/json'}

	def test_no_auth(self):
		response = self.client.get(url_for('api.get_posts'), content_type='application/json')
		self.assertEqual(response.status_code, 401)
	
	def test_posts(self):
		r = Role.query.filter_by(name='User').first()
		self.assertIsNotNone(r)
		u = User(email='john@example.com', password='cat', confirmed=True, role=r)
		db.session.add(u)
		db.session.commit()

		response = self.client.post('/api/v1/posts/', headers=self.get_api_headers('john@example.com','cat'), data=json.dumps({'body': 'body of the blog post'}))
		self.assertEqual(response.status_code, 201)
		url = response.headers.get('Location')
		self.assertIsNotNone(url)

		response = self.client.get(url, headers=self.get_api_headers('john@example.com', 'cat'))
		self.assertEqual(response.status_code, 200)
		json_response = json.loads(response.get_data(as_text=True))
		self.assertEqual('http://localhost' + json_response['url'], url)
		self.assertEqual(json_response['body'], 'body of the *blog* post')
		self.assertEqual(json_response['body_html'], '<p>body of the <em>blog</em> post</p>')

