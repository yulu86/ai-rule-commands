# Python 代码审查指南

## 🔴 高优先级问题

### 安全问题

#### SQL注入防护
```python
# ❌ 问题：SQL字符串拼接
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)

# ✅ 改进：使用参数化查询
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))

# ✅ 更好：使用ORM
from sqlalchemy.orm import Session
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
```

#### 不安全的反序列化
```python
# ❌ 问题：使用pickle反序列化
import pickle
def load_data(data):
    return pickle.loads(data)  # 可能执行恶意代码

# ✅ 改进：使用JSON
import json
def load_data(data):
    return json.loads(data)

# ✅ 或使用msgpack等安全格式
import msgpack
def load_data(data):
    return msgpack.unpackb(data, raw=False)
```

#### 硬编码敏感信息
```python
# ❌ 问题：硬编码密码和密钥
class Config:
    DATABASE_PASSWORD = "admin123"
    API_KEY = "sk-1234567890abcdef"
    SECRET_KEY = "my-secret-key"

# ✅ 改进：使用环境变量
import os
from dataclasses import dataclass

@dataclass
class Config:
    DATABASE_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    API_KEY: str = os.getenv('API_KEY', '')
    SECRET_KEY: str = os.getenv('SECRET_KEY', '')
    
    def __post_init__(self):
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable is required")
```

### 性能问题

#### 低效的循环
```python
# ❌ 问题：O(n²) 复杂度
def find_duplicates(items):
    duplicates = []
    for i, item in enumerate(items):
        for j, other_item in enumerate(items[i+1:], i+1):
            if item == other_item and item not in duplicates:
                duplicates.append(item)
    return duplicates

# ✅ 改进：O(n) 复杂度
def find_duplicates(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)

# ✅ 更好：使用集合操作
def find_duplicates(items):
    return list(set(item for item in items if items.count(item) > 1))
```

#### 内存使用优化
```python
# ❌ 问题：一次性加载大文件到内存
def process_large_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()  # 大文件会消耗大量内存
    return process_lines(lines)

# ✅ 改进：逐行处理
def process_large_file(filename):
    results = []
    with open(filename, 'r') as f:
        for line in f:  # 逐行读取，内存友好
            result = process_line(line)
            results.append(result)
    return results

# ✅ 更好：使用生成器
def process_large_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield process_line(line)
```

#### 字符串操作优化
```python
# ❌ 问题：频繁的字符串拼接
def build_string(items):
    result = ""
    for item in items:
        result += str(item) + ","  # 每次都创建新字符串
    return result

# ✅ 改进：使用列表和join
def build_string(items):
    return ",".join(str(item) for item in items)

# ✅ 或者使用StringIO
from io import StringIO
def build_string(items):
    with StringIO() as buffer:
        for i, item in enumerate(items):
            if i > 0:
                buffer.write(",")
            buffer.write(str(item))
        return buffer.getvalue()
```

## 🟡 中优先级问题

### 异常处理

#### 过于宽泛的异常捕获
```python
# ❌ 问题：捕获所有异常
def divide_numbers(a, b):
    try:
        return a / b
    except:  # 捕获所有异常，包括KeyboardInterrupt
        return None

# ✅ 改进：捕获具体异常
def divide_numbers(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        logging.error(f"Division by zero: {a} / {b}")
        return None
    except TypeError as e:
        logging.error(f"Invalid types: {type(a)}, {type(b)} - {e}")
        raise ValueError("Both arguments must be numbers")

# ✅ 更好：使用装饰器
def handle_division_errors(func):
    def wrapper(a, b):
        try:
            return func(a, b)
        except ZeroDivisionError:
            logging.error(f"Division by zero in {func.__name__}")
            return float('inf')
    return wrapper

@handle_division_errors
def divide_numbers(a, b):
    return a / b
```

#### 异常信息泄露
```python
# ❌ 问题：暴露敏感信息
def login_user(username, password):
    try:
        user = authenticate(username, password)
        return user
    except Exception as e:
        # 直接暴露异常信息可能泄露系统结构
        return {"error": str(e)}

# ✅ 改进：安全的错误信息
def login_user(username, password):
    try:
        user = authenticate(username, password)
        return {"success": True, "user_id": user.id}
    except InvalidCredentialsError:
        logging.warning(f"Failed login attempt for user: {username}")
        return {"error": "Invalid username or password"}
    except Exception as e:
        logging.error(f"Unexpected error during login: {e}")
        return {"error": "Internal server error"}
```

### 代码设计

#### 函数职责过多
```python
# ❌ 问题：函数过长，职责不清
def process_user_registration(data):
    # 验证数据 (15行)
    if not data.get('email'):
        raise ValueError("Email is required")
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', data['email']):
        raise ValueError("Invalid email format")
    # ... 更多验证逻辑
    
    # 创建用户 (10行)
    user = User(
        email=data['email'],
        password_hash=hash_password(data['password']),
        created_at=datetime.now()
    )
    db.session.add(user)
    db.session.commit()
    
    # 发送邮件 (8行)
    send_welcome_email(user.email, user.name)
    
    # 记录日志 (5行)
    logging.info(f"New user registered: {user.email}")
    
    return user

# ✅ 改进：拆分为多个小函数
class UserRegistrationService:
    def __init__(self, db, email_service, password_service):
        self.db = db
        self.email_service = email_service
        self.password_service = password_service
    
    def validate_registration_data(self, data: dict) -> None:
        """验证注册数据"""
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required")
        
        if not self._is_valid_email(data['email']):
            raise ValueError("Invalid email format")
        
        if len(data['password']) < 8:
            raise ValueError("Password must be at least 8 characters")
    
    def create_user(self, data: dict) -> User:
        """创建用户"""
        return User(
            email=data['email'],
            password_hash=self.password_service.hash(data['password']),
            name=data['name'],
            created_at=datetime.utcnow()
        )
    
    def send_welcome_email(self, user: User) -> None:
        """发送欢迎邮件"""
        self.email_service.send_welcome(user.email, user.name)
    
    def register_user(self, data: dict) -> User:
        """注册用户的主流程"""
        self.validate_registration_data(data)
        
        user = self.create_user(data)
        self.db.session.add(user)
        self.db.session.commit()
        
        self.send_welcome_email(user)
        logging.info(f"New user registered: {user.email}")
        
        return user
```

#### 魔法数字和重复代码
```python
# ❌ 问题：魔法数字和重复代码
def calculate_discount(price, quantity, customer_type):
    if quantity > 100:
        if customer_type == "VIP":
            return price * 0.8  # 20% discount
        else:
            return price * 0.9  # 10% discount
    elif quantity > 50:
        return price * 0.95  # 5% discount
    return price

def calculate_shipping(weight, distance):
    if weight > 10:
        if distance > 100:
            return weight * distance * 0.15
        else:
            return weight * distance * 0.12
    else:
        return weight * distance * 0.1

# ✅ 改进：使用常量和配置
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class CustomerType(Enum):
    VIP = "VIP"
    PREMIUM = "PREMIUM"
    REGULAR = "REGULAR"

@dataclass
class DiscountConfig:
    BULK_QUANTITY_THRESHOLD: int = 100
    MEDIUM_QUANTITY_THRESHOLD: int = 50
    VIP_DISCOUNT_RATE: float = 0.2
    BULK_DISCOUNT_RATE: float = 0.1
    MEDIUM_DISCOUNT_RATE: float = 0.05

@dataclass
class ShippingConfig:
    HEAVY_WEIGHT_THRESHOLD: float = 10.0
    LONG_DISTANCE_THRESHOLD: float = 100.0
    HEAVY_LONG_DISTANCE_RATE: float = 0.15
    HEAVY_SHORT_DISTANCE_RATE: float = 0.12
    STANDARD_RATE: float = 0.10

class PriceCalculator:
    def __init__(self):
        self.discount_config = DiscountConfig()
        self.shipping_config = ShippingConfig()
    
    def calculate_discount(self, price: float, quantity: int, 
                          customer_type: CustomerType) -> float:
        """计算折扣价格"""
        if quantity >= self.discount_config.BULK_QUANTITY_THRESHOLD:
            if customer_type == CustomerType.VIP:
                discount_rate = self.discount_config.VIP_DISCOUNT_RATE
            else:
                discount_rate = self.discount_config.BULK_DISCOUNT_RATE
        elif quantity >= self.discount_config.MEDIUM_QUANTITY_THRESHOLD:
            discount_rate = self.discount_config.MEDIUM_DISCOUNT_RATE
        else:
            discount_rate = 0.0
        
        return price * (1 - discount_rate)
    
    def calculate_shipping(self, weight: float, distance: float) -> float:
        """计算运费"""
        if weight >= self.shipping_config.HEAVY_WEIGHT_THRESHOLD:
            if distance >= self.shipping_config.LONG_DISTANCE_THRESHOLD:
                rate = self.shipping_config.HEAVY_LONG_DISTANCE_RATE
            else:
                rate = self.shipping_config.HEAVY_SHORT_DISTANCE_RATE
        else:
            rate = self.shipping_config.STANDARD_RATE
        
        return weight * distance * rate
```

## 🟢 低优先级问题

### Pythonic 代码

#### 列表推导式和生成器
```python
# ❌ 问题：不必要的循环
def get_even_numbers(numbers):
    result = []
    for num in numbers:
        if num % 2 == 0:
            result.append(num)
    return result

def get_squares(numbers):
    result = []
    for num in numbers:
        result.append(num ** 2)
    return result

# ✅ 改进：使用列表推导式
def get_even_numbers(numbers):
    return [num for num in numbers if num % 2 == 0]

def get_squares(numbers):
    return [num ** 2 for num in numbers]

# ✅ 更好：使用生成器表达式（大数据集）
def process_large_dataset(data):
    return (x * 2 for x in data if x > 0)  # 返回生成器，节省内存
```

#### 上下文管理器
```python
# ❌ 问题：手动资源管理
def process_file(filename):
    f = open(filename, 'r')
    try:
        content = f.read()
        # 处理内容
        return processed_content
    finally:
        f.close()

# ✅ 改进：使用with语句
def process_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
        return process_content(content)

# ✅ 自定义上下文管理器
from contextlib import contextmanager

@contextmanager
def database_transaction():
    session = create_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def update_user_data(user_id, new_data):
    with database_transaction() as session:
        user = session.query(User).get(user_id)
        user.update(new_data)
```

#### 装饰器使用
```python
# ❌ 问题：重复的横切关注点代码
def fetch_user_data(user_id):
    start_time = time.time()
    try:
        # 数据库查询逻辑
        result = db.query(User).get(user_id)
        return result
    except Exception as e:
        logging.error(f"Error fetching user {user_id}: {e}")
        raise
    finally:
        end_time = time.time()
        logging.info(f"Query took {end_time - start_time:.2f}s")

# ✅ 改进：使用装饰器
import time
import logging
from functools import wraps

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            logging.info(f"{func.__name__} took {end_time - start_time:.2f}s")
    return wrapper

def handle_database_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Database error in {func.__name__}: {e}")
            raise
    return wrapper

@log_execution_time
@handle_database_errors
def fetch_user_data(user_id):
    return db.query(User).get(user_id)
```

### 类型注解

#### 缺少类型提示
```python
# ❌ 问题：缺少类型注解
def process_data(data, processor):
    results = []
    for item in data:
        result = processor(item)
        results.append(result)
    return results

def create_user(name, email, age):
    return User(name=name, email=email, age=age)

# ✅ 改进：添加类型注解
from typing import List, Callable, Any, Optional

def process_data(
    data: List[Any], 
    processor: Callable[[Any], Any]
) -> List[Any]:
    """处理数据集合"""
    return [processor(item) for item in data]

def create_user(
    name: str, 
    email: str, 
    age: int
) -> User:
    """创建用户实例"""
    return User(name=name, email=email, age=age)

# ✅ 更好：使用泛型和协议
from typing import TypeVar, Protocol, Iterable

T = TypeVar('T')
R = TypeVar('R')

class Processor(Protocol[T, R]):
    def __call__(self, item: T) -> R: ...

def transform_data(
    data: Iterable[T], 
    processor: Processor[T, R]
) -> List[R]:
    """转换数据集合"""
    return [processor(item) for item in data]
```

### 测试和文档

#### 文档字符串
```python
# ❌ 问题：缺少文档
def calculate_tax(amount, rate):
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return amount * rate

# ✅ 改进：完整的文档字符串
def calculate_tax(amount: float, rate: float) -> float:
    """
    计算税额
    
    Args:
        amount (float): 应税金额，必须为非负数
        rate (float): 税率，例如0.1表示10%的税率
        
    Returns:
        float: 计算出的税额
        
    Raises:
        ValueError: 当金额为负数时抛出
        
    Examples:
        >>> calculate_tax(100, 0.1)
        10.0
        >>> calculate_tax(0, 0.05)
        0.0
        
    Note:
        此函数不对结果进行四舍五入，调用者负责格式化输出
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return amount * rate
```

这些检查点可以帮助识别Python代码中的常见问题，提供具体的改进建议，并促进更好的Python编码实践。