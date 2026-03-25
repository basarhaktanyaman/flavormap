from django.core.management.base import BaseCommand
from myapp.models import Category, Location, Restaurant, Review


class Command(BaseCommand):
    help = "Populate the database with sample FinDish data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding FinDish database...")

        # --- Categories ---
        categories_data = [
            {"name": "Turkish", "description": "Traditional Turkish cuisine", "icon": "bi-cup-hot"},
            {"name": "Italian", "description": "Pizza, pasta, and Mediterranean flavors", "icon": "bi-globe-europe-africa"},
            {"name": "Fast Food", "description": "Quick bites and street food", "icon": "bi-lightning-fill"},
            {"name": "Seafood", "description": "Fresh fish and ocean delights", "icon": "bi-tsunami"},
            {"name": "Asian", "description": "Far East culinary traditions", "icon": "bi-globe-asia-australia"},
        ]
        categories = {}
        for data in categories_data:
            obj, created = Category.objects.get_or_create(name=data["name"], defaults=data)
            categories[data["name"]] = obj
            status = "Created" if created else "Exists"
            self.stdout.write(f"  Category: {obj.name} [{status}]")

        # --- Locations ---
        locations_data = [
            {"city": "Istanbul", "district": "Kadikoy"},
            {"city": "Istanbul", "district": "Besiktas"},
            {"city": "Istanbul", "district": "Beyoglu"},
            {"city": "Ankara", "district": "Cankaya"},
            {"city": "Izmir", "district": "Alsancak"},
        ]
        locations = {}
        for data in locations_data:
            obj, created = Location.objects.get_or_create(**data)
            locations[f"{data['district']}, {data['city']}"] = obj
            status = "Created" if created else "Exists"
            self.stdout.write(f"  Location: {obj} [{status}]")

        # --- Restaurants ---
        restaurants_data = [
            {
                "name": "Kebapci Mehmet Usta",
                "description": "Authentic Turkish kebabs grilled over charcoal. A local favorite since 1985 with a warm, family-friendly atmosphere and generous portions.",
                "address": "Caferaga Mah. Moda Cad. No:42, Kadikoy",
                "phone": "+90 216 555 1234",
                "price_range": "€€",
                "category": categories["Turkish"],
                "location": locations["Kadikoy, Istanbul"],
                "image_url": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=600",
            },
            {
                "name": "Napoli Pizza House",
                "description": "Wood-fired Neapolitan pizzas crafted with imported Italian flour and San Marzano tomatoes. Cozy candlelit ambiance perfect for date nights.",
                "address": "Siraselviler Cad. No:15, Beyoglu",
                "phone": "+90 212 555 5678",
                "price_range": "€€",
                "category": categories["Italian"],
                "location": locations["Beyoglu, Istanbul"],
                "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600",
            },
            {
                "name": "Burger Lab",
                "description": "Gourmet burgers with creative toppings and hand-cut fries. Try the signature Truffle Smash Burger — you won't regret it!",
                "address": "Barbaros Blv. No:8, Besiktas",
                "phone": "+90 212 555 9012",
                "price_range": "€",
                "category": categories["Fast Food"],
                "location": locations["Besiktas, Istanbul"],
                "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600",
            },
            {
                "name": "Balik Ekmek Iskele",
                "description": "Fresh-off-the-boat fish sandwiches and grilled sea bass right by the Bosphorus. Best enjoyed with a glass of cold salgam.",
                "address": "Iskele Meydani No:3, Kadikoy",
                "phone": "+90 216 555 3456",
                "price_range": "€",
                "category": categories["Seafood"],
                "location": locations["Kadikoy, Istanbul"],
                "image_url": "https://images.unsplash.com/photo-1534766555764-ce878a5e3a2b?w=600",
            },
            {
                "name": "Tokyo Ramen Bar",
                "description": "Rich tonkotsu and miso ramen bowls with handmade noodles. Minimalist decor, maximum umami.",
                "address": "Tunali Hilmi Cad. No:22, Cankaya",
                "phone": "+90 312 555 7890",
                "price_range": "€€",
                "category": categories["Asian"],
                "location": locations["Cankaya, Ankara"],
                "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600",
            },
            {
                "name": "Sultan Sofrasi",
                "description": "Ottoman-era recipes served in a beautifully restored mansion. An upscale Turkish dining experience with a curated wine list.",
                "address": "Kordon Boyu No:55, Alsancak",
                "phone": "+90 232 555 2345",
                "price_range": "€€€",
                "category": categories["Turkish"],
                "location": locations["Alsancak, Izmir"],
                "image_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600",
            },
        ]

        restaurants = []
        for data in restaurants_data:
            obj, created = Restaurant.objects.get_or_create(name=data["name"], defaults=data)
            restaurants.append(obj)
            status = "Created" if created else "Exists"
            self.stdout.write(f"  Restaurant: {obj.name} [{status}]")

        # --- Reviews ---
        reviews_data = [
            {"restaurant": restaurants[0], "author_name": "Ayse K.", "rating": 5, "comment": "Best kebabs in Kadikoy! The adana kebab is perfection."},
            {"restaurant": restaurants[0], "author_name": "Mehmet D.", "rating": 4, "comment": "Great food, slightly slow service during weekends."},
            {"restaurant": restaurants[1], "author_name": "Laura P.", "rating": 5, "comment": "Authentic Napoli taste! The Margherita is incredible."},
            {"restaurant": restaurants[1], "author_name": "Can B.", "rating": 4, "comment": "Best Italian in Beyoglu. Loved the tiramisu too."},
            {"restaurant": restaurants[2], "author_name": "Emre T.", "rating": 4, "comment": "Juicy burgers, great value for money. Will come back!"},
            {"restaurant": restaurants[2], "author_name": "Zeynep A.", "rating": 3, "comment": "Good burgers but the place was too noisy."},
            {"restaurant": restaurants[3], "author_name": "Ali V.", "rating": 5, "comment": "Nothing beats fresh fish by the sea. Amazing experience."},
            {"restaurant": restaurants[4], "author_name": "Deniz S.", "rating": 4, "comment": "Closest thing to real Tokyo ramen in Turkey!"},
            {"restaurant": restaurants[4], "author_name": "Yuki M.", "rating": 5, "comment": "As a Japanese person, I approve. Excellent tonkotsu."},
            {"restaurant": restaurants[5], "author_name": "Selin G.", "rating": 5, "comment": "The lamb shank was out of this world. A special occasion restaurant."},
            {"restaurant": restaurants[5], "author_name": "Baris O.", "rating": 4, "comment": "Beautiful setting and great food, but pricey."},
        ]

        review_count = 0
        for data in reviews_data:
            _, created = Review.objects.get_or_create(
                restaurant=data["restaurant"],
                author_name=data["author_name"],
                defaults=data,
            )
            if created:
                review_count += 1

        self.stdout.write(f"  Reviews: {review_count} new reviews created")
        self.stdout.write(self.style.SUCCESS("\nDatabase populated successfully!"))
