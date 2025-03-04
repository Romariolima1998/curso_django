from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase, Recipe


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().tearDown()

    def test_recipe_title_raises_error_if_more_then_65_chars(self):
        self.recipe.title = 'a' * 70

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65)
        ])
    def test_recipe_fields_max_length(self, field, max):

        setattr(self.recipe, field, 'a' * (max + 1))

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()

        recipe.full_clean()
        recipe.save()

        self.assertFalse(recipe.preparation_steps_is_html)

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()

        recipe.full_clean()
        recipe.save()

        self.assertFalse(recipe.is_published, msg='is_published is not false ')

    def test_recipe_string_reprasentation(self):

        self.assertEqual(str(self.recipe), self.recipe.title, msg='Recipe __str__ method not return recipe title')
