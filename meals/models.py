from django.db import models


class MacroGoal(models.Model):
    """
    Rather than potentially store the macro goals for each day, with the day itself
    being an object, we can remove a lot of complexity by storing the actual macro
    goals themselves, while keeping the day as a purely client side concept

    For example, we might store the last period as 2020-01-01 - 2020-04-01 where
    the goals were (200, 100, 50) being carbs, protein and fat respectively

    We would check each day to see what today's goals are, and if they've changed
    from yesterday, we would:

        - Set the end date for the period ending yesterday
        - Create a new goal with today's date as the start date and a null end date
        - Save the new goals

    It might seem a bit weird, but we only need this information, as it pertains to
    each specific day, in order to calculate how we're progressing (ie % of goal met)

    At first it was tempting to capture each day as an object, with the goal attached
    as well as fields for current progress but we can infer that information by comparing
    tracked food items to the macro goals for the day (or specifically, the period which
    the day we're viewing falls under)

    If we go back in time, we don't want to just show today's goals and they're not
    historically accurate and would skew the data (ie showing 80% instead of 100% or more)

    Lastly, it also keeps the amount of data we need to store to a minimum.

    Storing each day in a database would consist of 365 day entries, with 365 * 6 = 2190
    rows a year, per user just to store each segment uniquely. Visually, that's how a day
    is represented anyway. Going this route reduces it to perhaps no more than 12 entries a year?

    Realistically, someone would be doing a review every 3 months so it's more like 4 fields.
    """
    user = models.ForeignKey(to='lobby.User', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    target_carbs = models.IntegerField()
    target_protein = models.IntegerField()
    target_fat = models.IntegerField()

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"

    def __repr__(self):
        return self.__str__()


class Food(models.Model):
    """
    This represents a unit of food (or drink) such as its metadata (name, brand, serving size)
    but tells you nothing about when (or if) it has ever been eaten, or by who.

    When searching the food database, and adding an item, it makes sense to save a copy for
    use in caching. We can assume that someone is likely to prepare a recurring meal than
    they are to try something totally new.

    That's an assumption of course but for me, it holds true anyway.

    In order to reduce the fetching of blocking information every time, we can save each
    food item once and then store favourites as a Many To Many Field from the User model.

    In order to extrapolate any arbitrary measurement, we store the value of each macro
    that is contained in a single unit (ie fat in 1g of X) and then extrapolate out for
    eg; a 300g Cheeseburger based on 300 * 1 unit for each field

    That's my current thinking anyway, we'll see how it performs in reality
    """
    name = models.CharField(max_length=200)
    is_alcohol = models.BooleanField(default=False)
    serving_unit = models.CharField(max_length=10, null=True)
    serving_size = models.FloatField(max_length=10, null=True)

    # Macros in one unit (ie 1g / 1mL)
    calcium = models.FloatField(null=True)
    calories = models.FloatField(null=True)
    carbohydrates = models.FloatField(null=True)
    cholesterol = models.FloatField(null=True)
    fat = models.FloatField(null=True)
    fat_monounsatured = models.FloatField(null=True)
    fat_polyunsaturated = models.FloatField(null=True)
    fat_saturated = models.FloatField(null=True)
    fat_trans = models.FloatField(null=True)
    fibre = models.FloatField(null=True)
    iron = models.FloatField(null=True)
    potassium = models.FloatField(null=True)
    protein = models.FloatField(null=True)
    sodium = models.FloatField(null=True)
    sugar = models.FloatField(null=True)
    vitamin_a = models.FloatField(null=True)
    vitamin_c = models.FloatField(null=True)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()


class Meal(models.Model):
    """
    While Food objects can be shared between users, the actual instances of a food item
    being tracked and consumed are specific to a user.

    In this sense, a Meal is an instance of food being eaten, but not the food itself

    We may want to look at which segment of a day was a meal specifically eaten (ie Morning Tea)
    or what foods are most reliably tracked for example.

    If a Food item were deleted for some reason, we don't want to delete the Meal itself
    given a User still actually ate the meal in question. I can't say I know why a Food item
    would ever be deleted, and for now, there is no functionality to actually perform such a deletion.

    The term Daypart is used to refer to the part of the day a meal was consumed eg; Morning Tea or Lunch

    I had never heard of the term before but it comes from broadcast television which uses the term
    to refer to timeslots such as "post late fringe" or "prime time"

    See: https://en.wikipedia.org/wiki/Dayparting
    """
    BREAKFAST = 'BR'
    MORNING_TEA = 'MT'
    LUNCH = 'LN'
    AFTERNOON_TEA = 'AT'
    DINNER = 'DN'
    SUPPER = 'SP'
    DAYPART_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (MORNING_TEA, 'Morning Tea'),
        (LUNCH, 'Lunch'),
        (AFTERNOON_TEA, 'Afternoon Tea'),
        (DINNER, 'Dinner'),
        (SUPPER, 'Supper'),
    ]
    id = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(to='lobby.User', on_delete=models.CASCADE)
    food = models.ForeignKey(to='Food', on_delete=models.SET_NULL, null=True)
    alcoholic = models.BooleanField(default=False)
    time_tracked = models.DateTimeField(null=True)
    day_associated = models.DateField(auto_now=True)
    daypart_associated = models.CharField(max_length=2, choices=DAYPART_CHOICES)

    def __str__(self):
        return f"{self.food.name} eaten at {self.daypart_associated}"

    def __repr__(self):
        return self.__str__()