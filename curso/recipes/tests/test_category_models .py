from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category()
        return super().tearDown()

    def test_category_name_raises_error_if_more_then_65_chars(self):
        self.category.name = 'a' * 70

        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_category_string_reprasentation(self):

        self.assertEqual(
            str(self.category), self.category.name,
            msg='Category __str__ method not return category name')
