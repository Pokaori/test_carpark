from django.test import TestCase
from .services import DriverService
from django.urls import reverse
import json


class DriverTests(TestCase):

    def setUp(self):
        DriverService.driver_create("Polina", "Semonova", '2021-12-04 19:02:16.192857', '2021-12-04 19:02:16.192857', )
        DriverService.driver_create("Petro", "Petrov", '2021-09-04 19:02:16.192857', '2021-12-04 19:02:16.192857')
        DriverService.driver_create("Ivan", "Ivanov", '2021-06-04 19:02:16.192857', '2021-12-04 19:02:16.192857')

    def test_list_drivers(self):
        response = self.client.get(reverse("driver-list"))
        self.assertEqual(response.headers["Content-Type"], "application/json")
        for driver in json.loads(response.content):
            self.assertEqual(list(driver.keys()), ['id', 'first_name', 'last_name', 'created_at', 'updated_at'])

    def test_list_drivers_with_created_at__gte(self):
        response = self.client.get(reverse("driver-list"), {'created_at__gte': '10-11-2021'})
        content = json.loads(response.content)
        for driver in content:
            self.assertEqual(driver['first_name'], "Polina", msg=content)

    def test_list_drivers_with_created_at__lte(self):
        response = self.client.get(reverse("driver-list"), {'created_at__lte': '10-11-2021'})
        content = json.loads(response.content)
        for driver in content:
            self.assertIn(driver['first_name'], ["Petro", "Ivan"], msg=content)

    def test_list_drivers_with_created_at__gte_and_lte(self):
        response = self.client.get(reverse("driver-list"), {'created_at__lte': '10-11-2021',
                                                            'created_at__gte': '10-08-2021'})
        content = json.loads(response.content)
        for driver in content:
            self.assertEqual(driver['first_name'], "Petro", msg=content)

    def test_list_drivers_with_created_at__and_lte_incorrect_form(self):
        response = self.client.get(reverse("driver-list"), {'created_at__lte': '09-07'})
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400, msg=content)
        response = self.client.get(reverse("driver-list"), {'created_at__gte': '09-07'})
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400, msg=content)

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("driver-detail", args=[2]))
        driver = json.loads(response.content)
        self.assertEqual(driver['first_name'], "Petro", msg=driver)

    def test_post_drivers(self):
        response = self.client.post(reverse("driver-list"), data={"first_name": "Alex",
                                                                  "last_name": "Alexeyev"})
        self.assertEqual(response.status_code, 201)
        driver = json.loads(response.content)
        self.assertEqual(driver['first_name'], "Alex", msg=driver)

    def test_put_drivers_requires_all_fields(self):
        response = self.client.put(reverse("driver-detail", args=[3]), data={"first_name": "Update"},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response = self.client.put(reverse("driver-detail", args=[3]), data={"last_name": "Updated"},
                                   content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400, msg=content)

    def test_put_drivers_validate_all_fields(self):
        response = self.client.put(reverse("driver-detail", args=[3]),
                                   data={"first_name": "Update123", "last_name": "Updated123"},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 400)
        error = json.loads(response.content)
        self.assertEqual(sorted(list(error.keys())), ["first_name", "last_name"], msg=error)
        response = self.client.put(reverse("driver-detail", args=[3]),
                                   data={"first_name": "update", "last_name": "updated-up"},
                                   content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)
        self.assertEqual(content["first_name"], "Update", msg=content)
        self.assertEqual(content["last_name"], "Updated-Up", msg=content)

    def test_patch_drivers(self):
        first_name = "Update"
        last_name = "Updated"
        response = self.client.patch(reverse("driver-detail", args=[3]), data={"first_name": first_name},
                                     content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)

        response = self.client.patch(reverse("driver-detail", args=[3]), data={"last_name": last_name},
                                     content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)

        response = self.client.get(reverse("driver-detail", args=[3]),
                                   content_type="application/json")
        driver = json.loads(response.content)
        self.assertEqual(driver['first_name'], first_name, msg=driver)
        self.assertEqual(driver['last_name'], last_name, msg=driver)

    def test_delete_drivers(self):
        response = self.client.delete(reverse("driver-detail", args=[3]),
                                      content_type="application/json")
        self.assertEqual(response.status_code, 204)
        response = self.client.delete(reverse("driver-detail", args=[3]))
        self.assertEqual(response.status_code, 404)
