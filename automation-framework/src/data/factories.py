"""Test data factories for generating realistic test data."""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from faker import Faker

from ..utils.helpers import generate_random_string, generate_random_email, generate_random_phone
from ..utils.logger import get_logger

logger = get_logger(__name__)

# Initialize Faker with different locales for variety
fake_en = Faker('en_US')
fake_es = Faker('es_ES')
fake_fr = Faker('fr_FR')

# Default fake instance for backward compatibility
fake = fake_en


@dataclass
class UserData:
    """User test data structure."""
    first_name: str
    last_name: str
    email: str
    phone: str
    username: str
    password: str
    date_of_birth: str
    address: Dict[str, str] = field(default_factory=dict)
    preferences: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'username': self.username,
            'password': self.password,
            'date_of_birth': self.date_of_birth,
            'address': self.address,
            'preferences': self.preferences,
            'metadata': self.metadata
        }


@dataclass
class ProductData:
    """Product test data structure."""
    name: str
    description: str
    price: float
    category: str
    sku: str
    in_stock: bool = True
    quantity: int = 0
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'sku': self.sku,
            'in_stock': self.in_stock,
            'quantity': self.quantity,
            'attributes': self.attributes
        }


@dataclass
class OrderData:
    """Order test data structure."""
    order_id: str
    user_id: str
    products: List[Dict[str, Any]]
    total_amount: float
    status: str
    shipping_address: Dict[str, str]
    billing_address: Dict[str, str]
    payment_method: str
    created_at: str
    updated_at: str
    user: Optional[Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'products': self.products,
            'total_amount': self.total_amount,
            'status': self.status,
            'shipping_address': self.shipping_address,
            'billing_address': self.billing_address,
            'payment_method': self.payment_method,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user': self.user
        }


class UserFactory:
    """Factory for generating user test data."""
    
    @staticmethod
    def create_user(
        locale: str = "en_US",
        include_address: bool = True,
        include_preferences: bool = True,
        custom_fields: Optional[Dict[str, Any]] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        date_of_birth: Optional[str] = None,
        **kwargs
    ) -> UserData:
        """
        Create a single user with realistic data.
        
        Args:
            locale: Faker locale
            include_address: Whether to include address data
            include_preferences: Whether to include preferences
            custom_fields: Custom field overrides
            
        Returns:
            UserData instance
        """
        # Use global fake instance if available (for testing), otherwise create new one
        fake = fake_en if locale == "en_US" else Faker(locale)
        
        # Generate basic user data (use provided values or generate new ones)
        first_name = first_name or fake.first_name()
        last_name = last_name or fake.last_name()
        email = email or fake.email()
        phone = phone or fake.phone_number()
        username = username or fake.user_name()
        password = password or fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        date_of_birth = date_of_birth or fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d")
        
        user_data = UserData(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            username=username,
            password=password,
            date_of_birth=date_of_birth
        )
        
        # Add address if requested
        if include_address:
            user_data.address = {
                "street": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "zip_code": fake.zipcode(),
                "country": fake.country()
            }
        
        # Add preferences if requested
        if include_preferences:
            user_data.preferences = {
                "language": random.choice(["en", "es", "fr"]),
                "timezone": fake.timezone(),
                "notifications": {
                    "email": random.choice([True, False]),
                    "sms": random.choice([True, False]),
                    "push": random.choice([True, False])
                },
                "theme": random.choice(["light", "dark", "auto"])
            }
        
        # Apply custom fields if provided
        if custom_fields:
            for key, value in custom_fields.items():
                if hasattr(user_data, key):
                    setattr(user_data, key, value)
                else:
                    user_data.metadata[key] = value
        
        logger.debug(f"Generated user: {user_data.email}")
        return user_data
    
    @staticmethod
    def create_users(
        count: int,
        locale: str = "en_US",
        include_address: bool = True,
        include_preferences: bool = True,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> List[UserData]:
        """
        Create multiple users.
        
        Args:
            count: Number of users to create
            locale: Faker locale
            include_address: Whether to include address data
            include_preferences: Whether to include preferences
            custom_fields: Custom field overrides
            
        Returns:
            List of UserData instances
        """
        users = []
        for i in range(count):
            user = UserFactory.create_user(
                locale=locale,
                include_address=include_address,
                include_preferences=include_preferences,
                custom_fields=custom_fields
            )
            users.append(user)
        
        logger.info(f"Generated {count} users")
        return users
    
    @staticmethod
    def create_admin_user() -> UserData:
        """Create an admin user with elevated privileges."""
        user = UserFactory.create_user()
        user.metadata["role"] = "admin"
        user.metadata["permissions"] = ["read", "write", "delete", "admin"]
        user.email = f"admin_{user.email}"
        return user
    
    @staticmethod
    def create_test_user() -> UserData:
        """Create a test user with predictable data."""
        return UserData(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone="(555) 123-4567",
            username="testuser",
            password="TestPassword123!",
            date_of_birth="1990-01-01",
            address={
                "street": "123 Test St",
                "city": "Test City",
                "state": "TS",
                "zip_code": "12345",
                "country": "United States"
            }
        )


class ProductFactory:
    """Factory for generating product test data."""
    
    PRODUCT_CATEGORIES = [
        "Electronics", "Clothing", "Books", "Home & Garden", "Sports",
        "Beauty", "Toys", "Automotive", "Health", "Food & Beverage"
    ]
    
    @staticmethod
    def create_product(
        category: Optional[str] = None,
        price_range: tuple = (10.0, 1000.0),
        in_stock: Optional[bool] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        sku: Optional[str] = None,
        quantity: Optional[int] = None,
        **kwargs
    ) -> ProductData:
        """
        Create a single product with realistic data.
        
        Args:
            category: Product category (random if None)
            price_range: Price range tuple (min, max)
            in_stock: Stock status (random if None)
            
        Returns:
            ProductData instance
        """
        fake = fake_en
        
        # Generate product data (use provided values or generate new ones)
        name = name or fake.catch_phrase()
        description = description or fake.text(max_nb_chars=200)
        price = price or round(random.uniform(*price_range), 2)
        category = category or random.choice(ProductFactory.PRODUCT_CATEGORIES)
        sku = sku or fake.bothify(text="???-####-???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        in_stock = in_stock if in_stock is not None else random.choice([True, False])
        quantity = quantity or (random.randint(0, 100) if in_stock else 0)
        
        # Generate attributes based on category
        attributes = ProductFactory._generate_attributes(category)
        
        product_data = ProductData(
            name=name,
            description=description,
            price=price,
            category=category,
            sku=sku,
            in_stock=in_stock,
            quantity=quantity,
            attributes=attributes
        )
        
        logger.debug(f"Generated product: {product_data.name}")
        return product_data
    
    @staticmethod
    def create_products(
        count: int,
        category: Optional[str] = None,
        price_range: tuple = (10.0, 1000.0),
        in_stock: Optional[bool] = None
    ) -> List[ProductData]:
        """
        Create multiple products.
        
        Args:
            count: Number of products to create
            category: Product category (random if None)
            price_range: Price range tuple (min, max)
            in_stock: Stock status (random if None)
            
        Returns:
            List of ProductData instances
        """
        products = []
        for i in range(count):
            product = ProductFactory.create_product(
                category=category,
                price_range=price_range,
                in_stock=in_stock
            )
            products.append(product)
        
        logger.info(f"Generated {count} products")
        return products
    
    @staticmethod
    def _generate_attributes(category: str) -> Dict[str, Any]:
        """Generate category-specific attributes."""
        attributes = {
            "brand": fake_en.company(),
            "model": fake_en.bothify(text="Model-###"),
            "color": random.choice(["Black", "White", "Red", "Blue", "Green", "Yellow"]),
            "size": random.choice(["XS", "S", "M", "L", "XL", "XXL"]),
            "weight": round(random.uniform(0.1, 50.0), 2),
            "dimensions": {
                "length": round(random.uniform(1, 100), 1),
                "width": round(random.uniform(1, 100), 1),
                "height": round(random.uniform(1, 100), 1)
            }
        }
        
        # Category-specific attributes
        if category == "Electronics":
            attributes.update({
                "warranty": f"{random.randint(1, 5)} years",
                "power_consumption": f"{random.randint(10, 500)}W",
                "connectivity": random.choice(["WiFi", "Bluetooth", "USB", "Ethernet"])
            })
        elif category == "Clothing":
            attributes.update({
                "material": random.choice(["Cotton", "Polyester", "Wool", "Silk", "Linen"]),
                "care_instructions": "Machine wash cold",
                "season": random.choice(["Spring", "Summer", "Fall", "Winter", "All Season"])
            })
        elif category == "Books":
            attributes.update({
                "author": fake_en.name(),
                "isbn": fake_en.isbn13(),
                "pages": random.randint(50, 1000),
                "language": random.choice(["English", "Spanish", "French", "German"])
            })
        
        return attributes


class OrderFactory:
    """Factory for generating order test data."""
    
    ORDER_STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled", "returned"]
    PAYMENT_METHODS = ["credit_card", "debit_card", "paypal", "apple_pay", "google_pay", "bank_transfer"]
    
    @staticmethod
    def create_order(
        user_id: Optional[str] = None,
        products: Optional[List[Dict[str, Any]]] = None,
        status: Optional[str] = None,
        payment_method: Optional[str] = None,
        **kwargs
    ) -> OrderData:
        """
        Create a single order with realistic data.
        
        Args:
            user_id: User ID for the order
            products: List of products in the order
            status: Order status (random if None)
            payment_method: Payment method (random if None)
            
        Returns:
            OrderData instance
        """
        fake = fake_en
        
        # Generate order data
        order_id = fake.bothify(text="ORD-########")
        user_id = user_id or fake.uuid4()
        products = products or [{"id": fake.uuid4(), "name": fake.word(), "price": round(random.uniform(10, 100), 2), "quantity": random.randint(1, 5)}]
        status = status or random.choice(OrderFactory.ORDER_STATUSES)
        payment_method = payment_method or random.choice(OrderFactory.PAYMENT_METHODS)
        
        # Calculate total amount
        total_amount = sum(product.get("price", 0) * product.get("quantity", 1) for product in products)
        
        # Generate addresses
        shipping_address = {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.zipcode(),
            "country": fake.country()
        }
        
        billing_address = shipping_address.copy()  # Often the same
        
        # Generate timestamps
        created_at = fake.date_time_between(start_date="-30d", end_date="now")
        updated_at = created_at + timedelta(days=random.randint(0, 7))
        
        order_data = OrderData(
            order_id=order_id,
            user_id=user_id,
            products=products,
            total_amount=round(total_amount, 2),
            status=status,
            shipping_address=shipping_address,
            billing_address=billing_address,
            payment_method=payment_method,
            created_at=created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=updated_at.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        logger.debug(f"Generated order: {order_data.order_id}")
        return order_data
    
    @staticmethod
    def create_orders(
        count: int,
        products_per_order: int = 3,
        status: Optional[str] = None,
        payment_method: Optional[str] = None
    ) -> List[OrderData]:
        """
        Create multiple orders.
        
        Args:
            count: Number of orders to create
            products_per_order: Number of products per order
            status: Order status (random if None)
            payment_method: Payment method (random if None)
            
        Returns:
            List of OrderData instances
        """
        fake = fake_en
        orders = []
        
        for i in range(count):
            user_id = fake.uuid4()
            # Generate products for this order
            products = []
            for _ in range(products_per_order):
                product = ProductFactory.create_product()
                products.append({
                    "id": product.sku,
                    "name": product.name,
                    "price": product.price,
                    "quantity": random.randint(1, 5)
                })
            
            order = OrderFactory.create_order(
                user_id=user_id,
                products=products,
                status=status,
                payment_method=payment_method
            )
            orders.append(order)
        
        logger.info(f"Generated {len(orders)} orders")
        return orders


class TestDataManager:
    """Manager for test data operations."""
    
    def __init__(self):
        """Initialize test data manager."""
        self.users: List[UserData] = []
        self.products: List[ProductData] = []
        self.orders: List[OrderData] = []
    
    def generate_test_dataset(
        self,
        user_count: int = 100,
        product_count: int = 50,
        order_count: int = 200
    ) -> Dict[str, Any]:
        """
        Generate a complete test dataset.
        
        Args:
            user_count: Number of users to generate
            product_count: Number of products to generate
            order_count: Number of orders to generate
            
        Returns:
            Dictionary containing all test data
        """
        logger.info(f"Generating test dataset: {user_count} users, {product_count} products, {order_count} orders")
        
        # Generate users
        self.users = UserFactory.create_users(user_count)
        user_ids = [user.email for user in self.users]  # Using email as ID
        
        # Generate products
        self.products = ProductFactory.create_products(product_count)
        
        # Generate orders
        self.orders = OrderFactory.create_orders(
            count=order_count,
            products_per_order=random.randint(1, 5)
        )
        
        dataset = {
            "users": [self._convert_to_dict(user) for user in self.users],
            "products": [self._convert_to_dict(product) for product in self.products],
            "orders": [self._convert_to_dict(order) for order in self.orders],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "user_count": len(self.users),
                "product_count": len(self.products),
                "order_count": len(self.orders)
            }
        }
        
        logger.info("Test dataset generation completed")
        return dataset
    
    def _convert_to_dict(self, obj) -> Dict[str, Any]:
        """Convert dataclass to dictionary."""
        if hasattr(obj, '__dict__'):
            result = {}
            for key, value in obj.__dict__.items():
                if hasattr(value, '__dict__'):
                    result[key] = self._convert_to_dict(value)
                elif isinstance(value, (list, tuple)):
                    result[key] = [self._convert_to_dict(item) if hasattr(item, '__dict__') else item for item in value]
                else:
                    result[key] = value
            return result
        return obj
    
    def get_user_by_email(self, email: str) -> Optional[UserData]:
        """Get user by email."""
        for user in self.users:
            if user.email == email:
                return user
        return None
    
    def get_products_by_category(self, category: str) -> List[ProductData]:
        """Get products by category."""
        return [product for product in self.products if product.category == category]
    
    def get_orders_by_user(self, user_id: str) -> List[OrderData]:
        """Get orders by user ID."""
        return [order for order in self.orders if order.user_id == user_id]
    
    def get_orders_by_status(self, status: str) -> List[OrderData]:
        """Get orders by status."""
        return [order for order in self.orders if order.status == status]
