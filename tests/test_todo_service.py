import unittest

from app.services.todo_service import TodoService


class TodoServiceTestCase(unittest.TestCase):
    def test_create_mark_done_and_delete(self) -> None:
        service = TodoService()

        created = service.create_item("Ship backend skill")
        self.assertEqual(created.title, "Ship backend skill")
        self.assertFalse(created.done)
        self.assertEqual(len(service.list_items()), 1)

        completed = service.mark_done(created.id)
        self.assertTrue(completed.done)

        service.delete_item(created.id)
        self.assertEqual(service.list_items(), [])


if __name__ == "__main__":
    unittest.main()
