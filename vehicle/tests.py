from django.test import TestCase
from .services import VehicleService
from driver.services import DriverService
from django.urls import reverse
import json


class DriverTests(TestCase):

    def setUp(self):
        DriverService.driver_create("Polina", "Semonova", '2021-12-04 19:02:16.192857', '2021-12-04 19:02:16.192857', )
        DriverService.driver_create("Ivan", "Ivanov", '2021-12-04 19:02:16.192857', '2021-12-04 19:02:16.192857', )
        VehicleService.vehicle_create("Audi", "Model1", "AA 1234 BB", 1,
                                      '2021-12-04 19:02:16.192857', '2021-12-04 19:02:16.192857', )
        VehicleService.vehicle_create("Toyota", "Model2", "AB 1234 BB", None,
                                      '2021-09-04 19:02:16.192857', '2021-12-04 19:02:16.192857')
        VehicleService.vehicle_create("Mercedes‑Benz", "Model3", "AC 1234 BB", None,
                                      '2021-06-04 19:02:16.192857', '2021-12-04 19:02:16.192857')

    def test_list_vehicles(self):
        response = self.client.get(reverse("vehicle-list"))
        content = json.loads(response.content)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        for vehicle in json.loads(response.content):
            self.assertEqual(sorted(list(vehicle.keys())),
                             ['created_at', 'driver_id', 'id', 'make', 'model', 'plate_number', 'updated_at'],
                             msg=content)
            self.assertIn(vehicle['driver_id'], [1, None], msg=content)

    def test_list_vehicles_with_drivers(self):
        response = self.client.get(reverse("vehicle-list"), {'with_drivers': 'yes'})
        content = json.loads(response.content)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        for vehicle in json.loads(response.content):
            self.assertEqual(vehicle['plate_number'], "AA 1234 BB", msg=content)
            self.assertEqual(vehicle['driver_id'], 1, msg=content)

    def test_list_vehicles_without_drivers(self):
        response = self.client.get(reverse("vehicle-list"), {'with_drivers': 'no'})
        content = json.loads(response.content)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(len(content), 2, msg=content)
        for vehicle in content:
            self.assertEqual(vehicle['driver_id'], None, msg=content)

    def test_list_vehicles_incorrect_with_drivers(self):
        response = self.client.get(reverse("vehicle-list"), {'with_drivers': 'incorrect'})
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400, msg=content)

    def test_retrieve_vehicle(self):
        response = self.client.get(reverse("vehicle-detail", kwargs={'pk': 1}))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)
        self.assertEqual(json.loads(response.content)['driver_id'], 1)

    def test_post_vehicle(self):
        response = self.client.post(reverse("vehicle-list"), {'make': 'Audi',
                                                              'model': 'Model4',
                                                              'plate_number': 'AE 1234 BB'})
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 201, msg=content)
        self.assertEqual(json.loads(response.content)['driver_id'], None, msg=content)

    def test_post_vehicle_with_driver_which_has_vehicle(self):
        response = self.client.post(reverse("vehicle-list"), {'make': 'Audi',
                                                              'driver_id': 1,
                                                              'model': 'Model4',
                                                              'plate_number': 'AE 1234 BB'})
        self.assertEqual(response.status_code, 400, msg=json.loads(response.content))

    def test_post_vehicle_with_driver(self):
        response = self.client.post(reverse("vehicle-list"), {'make': 'Audi',
                                                              'driver_id': 2,
                                                              'model': 'Model4',
                                                              'plate_number': 'AE 1234 BB'})
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 201, msg=content)
        self.assertEqual(content['driver_id'], 2, msg=content)

    def test_delete_vehicle(self):
        response = self.client.post(reverse("vehicle-list"), {'make': 'Audi',
                                                              'driver_id': 2,
                                                              'model': 'Model4',
                                                              'plate_number': 'AE 1234 BB'})
        vehicle = json.loads(response.content)
        self.assertEqual(response.status_code, 201, msg=vehicle)
        response = self.client.delete(reverse("vehicle-detail", kwargs={'pk': vehicle['id']}),
                                      content_type="application/json")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse("vehicle-detail", kwargs={'pk': 4}))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 404, msg=content)

    def test_set_driver_vehicle(self):
        response = self.client.post(reverse("set-driver", kwargs={'pk': 2}), {'driver_id': 2})
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)
        self.assertEqual(content['driver_id'], 2, msg=content)
        self.assertEqual(content['id'], 2, msg=content)

    def test_set_driver_null(self):
        response = self.client.post(reverse("set-driver", kwargs={'pk': 1}), {'driver_id': None},
                                    content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)
        self.assertEqual(content['driver_id'], None, msg=content)
        self.assertEqual(content['id'], 1, msg=content)

    def test_set_driver_vehicle_with_driver(self):
        response = self.client.post(reverse("set-driver", kwargs={'pk': 2}), {'driver_id': 1},
                                    content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 409, msg=content)

    def test_set_driver_vehicle_with_driver_in_another_vehicle(self):
        response = self.client.post(reverse("set-driver", kwargs={'pk': 1}), {'driver_id': 2},
                                    content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 409, msg=content)

    def test_put_vehicle(self):
        response = self.client.put(reverse("vehicle-detail", kwargs={'pk': 3}),
                                   {'make': 'Updated',
                                    'plate_number': 'AE 1234 BB'},
                                   content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400, msg=content)

        response = self.client.put(reverse("vehicle-detail", kwargs={'pk': 3}),
                                   {'make': 'Updated',
                                    'model': 'Updated',
                                    'plate_number': 'AE 1234 BB'},
                                   content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)
        self.assertEqual(content['model'], 'Updated', msg=content)
        self.assertEqual(content['make'], 'Updated', msg=content)

    def test_put_vehicle_validate(self):
        response = self.client.put(reverse("vehicle-detail", kwargs={'pk': 3}),
                                   {'make': 'Updated',
                                    'model': 'Updated',
                                    'plate_number': 'A2 1234 BB'},
                                   content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400, msg=content)
        response = self.client.put(reverse("vehicle-detail", kwargs={'pk': 3}),
                                   {'make': 'Updated',
                                    'model': 'Updated',
                                    'plate_number': 'AO 12b4 BB'},
                                   content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400, msg=content)
        response = self.client.put(reverse("vehicle-detail", kwargs={'pk': 3}),
                                   {'make': 'Updated',
                                    'model': 'Updated',
                                    'plate_number': 'AO 1234 bb'},
                                   content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)
        self.assertEqual(content["plate_number"], "AO 1234 BB", msg=content)

    def test_patch_vehicle(self):
        response = self.client.patch(reverse("vehicle-detail", kwargs={'pk': 3}),
                                     {'make': 'Updated',
                                      'plate_number': 'AF 1234 BB'},
                                     content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200, msg=content)
        self.assertEqual(content['model'], 'Model3', msg=content)
        self.assertEqual(content['make'], 'Updated', msg=content)
