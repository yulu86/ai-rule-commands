# 代码最佳实践指南

## 通用编程原则

### SOLID原则
- **S - 单一职责原则**: 每个类/函数只负责一个功能
- **O - 开闭原则**: 对扩展开放，对修改关闭
- **L - 里氏替换原则**: 子类可以替换父类
- **I - 接口隔离原则**: 接口应该小而专一
- **D - 依赖倒置原则**: 依赖抽象而非具体实现

### DRY原则 (Don't Repeat Yourself)
- 避免代码重复
- 提取公共逻辑到函数/类
- 使用模板和配置减少重复

### KISS原则 (Keep It Simple, Stupid)
- 保持代码简单易懂
- 避免过度设计
- 优先选择简单的解决方案

## 安全编程实践

### 输入验证
```python
# 好的做法 - 使用白名单验证
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# 避免 - 黑名单过滤容易被绕过
def sanitize_input(user_input):
    # 不要这样做：过滤特定字符
    return user_input.replace("<", "").replace(">", "")
```

### SQL注入防护
```java
// 好的做法 - 使用参数化查询
PreparedStatement stmt = connection.prepareStatement(
    "SELECT * FROM users WHERE username = ? AND password = ?");
stmt.setString(1, username);
stmt.setString(2, password);

// 避免 - 字符串拼接SQL
String query = "SELECT * FROM users WHERE username = '" + username + 
              "' AND password = '" + password + "'";
```

### 密码处理
```javascript
// 好的做法 - 使用强哈希算法
const bcrypt = require('bcrypt');
async function hashPassword(password) {
    const saltRounds = 10;
    return await bcrypt.hash(password, saltRounds);
}

// 避免 - 明文存储或弱哈希
function insecureHash(password) {
    return crypto.createHash('md5').update(password).digest('hex');
}
```

## 性能优化实践

### 算法选择
```python
# 好的做法 - 选择合适的算法
def find_duplicates_fast(arr):
    """O(n) 时间复杂度"""
    seen = set()
    duplicates = set()
    for item in arr:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return duplicates

# 避免 - 低效算法
def find_duplicates_slow(arr):
    """O(n^2) 时间复杂度"""
    duplicates = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in duplicates:
                duplicates.append(arr[i])
    return duplicates
```

### 缓存策略
```javascript
// 好的做法 - 实现缓存机制
class DataCache {
    constructor(ttl = 300000) { // 5分钟TTL
        this.cache = new Map();
        this.ttl = ttl;
    }
    
    get(key) {
        const item = this.cache.get(key);
        if (!item) return null;
        
        if (Date.now() > item.expiry) {
            this.cache.delete(key);
            return null;
        }
        
        return item.data;
    }
    
    set(key, data) {
        this.cache.set(key, {
            data: data,
            expiry: Date.now() + this.ttl
        });
    }
}
```

### 数据库优化
```sql
-- 好的做法 - 索引优化
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_order_user_date ON orders(user_id, created_date);

-- 避免 - 全表扫描
EXPLAIN SELECT * FROM orders WHERE user_id = 123;
```

## 错误处理实践

### 异常处理
```python
# 好的做法 - 具体的异常处理
try:
    result = divide_numbers(a, b)
except ZeroDivisionError:
    logger.error(f"Division by zero: {a} / {b}")
    raise ValueError("Cannot divide by zero")
except TypeError as e:
    logger.error(f"Invalid input types: {a}, {b}")
    raise TypeError("Both arguments must be numbers")
else:
    return result
finally:
    cleanup_resources()

# 避免 - 过于宽泛的异常处理
try:
    result = some_operation()
except:
    pass  # 静默忽略所有异常
```

### 日志记录
```java
// 好的做法 - 结构化日志
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class UserService {
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);
    
    public User createUser(String email, String password) {
        logger.info("Creating user with email: {}", email);
        
        try {
            User user = new User(email, password);
            userRepository.save(user);
            
            logger.info("User created successfully with ID: {}", user.getId());
            return user;
        } catch (Exception e) {
            logger.error("Failed to create user with email: {}", email, e);
            throw new UserCreationException("Unable to create user", e);
        }
    }
}
```

## 代码组织实践

### 函数设计
```javascript
// 好的做法 - 单一职责，清晰的参数
function calculateDiscount(price, customerType, quantity) {
    if (quantity > 10) {
        return price * 0.15; // 批量折扣
    }
    
    switch (customerType) {
        case 'VIP':
            return price * 0.20;
        case 'PREMIUM':
            return price * 0.10;
        default:
            return price * 0.05;
    }
}

// 避免 - 函数过长，职责不清
function processOrder(order) {
    // 验证订单 (20行)
    // 计算价格 (30行)  
    // 发送邮件 (15行)
    // 更新库存 (25行)
    // 记录日志 (10行)
    // 总共100多行...
}
```

### 类设计
```python
# 好的做法 - 清晰的职责分离
class UserRepository:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def find_by_id(self, user_id):
        return self.db.query("SELECT * FROM users WHERE id = ?", (user_id,))
    
    def save(self, user):
        # 保存用户逻辑
        pass

class EmailService:
    def __init__(self, smtp_client):
        self.smtp = smtp_client
    
    def send_welcome_email(self, user_email):
        # 发送邮件逻辑
        pass

class UserService:
    def __init__(self, user_repo, email_service):
        self.user_repo = user_repo
        self.email_service = email_service
    
    def register_user(self, email, password):
        # 协调各个服务完成用户注册
        pass
```

## 测试实践

### 单元测试
```python
# 好的做法 - 清晰的测试结构
import unittest
from unittest.mock import Mock

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.mock_email = Mock()
        self.service = UserService(self.mock_repo, self.mock_email)
    
    def test_register_user_success(self):
        # Arrange
        email = "test@example.com"
        password = "password123"
        self.mock_repo.save.return_value = User(id=1, email=email)
        
        # Act
        user = self.service.register_user(email, password)
        
        # Assert
        self.assertEqual(user.email, email)
        self.mock_repo.save.assert_called_once()
        self.mock_email.send_welcome_email.assert_called_once_with(email)
    
    def test_register_user_duplicate_email(self):
        # 测试边界情况
        pass
```

### 测试驱动开发 (TDD)
```python
# 1. 先写测试
def test_calculate_tax():
    assert calculate_tax(100, 0.1) == 10
    assert calculate_tax(0, 0.1) == 0
    with pytest.raises(ValueError):
        calculate_tax(-100, 0.1)

# 2. 实现功能
def calculate_tax(amount, rate):
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return amount * rate
```

## 文档实践

### 代码注释
```javascript
/**
 * 计算商品折扣价格
 * 
 * @param {number} originalPrice - 商品原价
 * @param {string} customerType - 客户类型 ('VIP', 'PREMIUM', 'REGULAR')
 * @param {number} quantity - 购买数量
 * @returns {number} 折扣后的价格
 * @throws {Error} 当参数无效时抛出错误
 * 
 * @example
 * const price = calculateDiscount(100, 'VIP', 5);
 * console.log(price); // 80
 */
function calculateDiscount(originalPrice, customerType, quantity) {
    // 实现逻辑...
}
```

### README文档
```markdown
# 项目名称

## 简介
简要描述项目功能和用途

## 快速开始
```bash
npm install
npm start
```

## API文档
详细的API接口说明

## 部署指南
部署步骤和环境要求

## 贡献指南
如何参与项目开发
```

## 版本控制实践

### Git提交信息
```bash
# 好的做法 - 清晰的提交信息
git commit -m "feat: 添加用户认证功能"
git commit -m "fix: 修复登录页面样式问题"
git commit -m "docs: 更新API文档"
git commit -m "refactor: 重构订单处理逻辑"

# 避免 - 不清晰的提交信息
git commit -m "修复bug"
git commit -m "更新代码"
git commit -m "临时提交"
```

### 分支策略
```
main (生产环境)
├── develop (开发环境)
├── feature/user-auth (功能分支)
├── bugfix/login-issue (修复分支)
└── hotfix/security-patch (热修复分支)
```

## 性能监控实践

### 关键指标监控
```python
# 好的做法 - 添加性能监控
import time
import logging

def monitor_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            if execution_time > 1.0:  # 超过1秒记录警告
                logging.warning(f"Slow query: {func.__name__} took {execution_time:.2f}s")
            
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

@monitor_performance
def process_large_dataset(data):
    # 处理大数据集的逻辑
    pass
```

## 配置管理实践

### 环境配置
```python
# 好的做法 - 环境变量配置
import os
from dataclasses import dataclass

@dataclass
class Config:
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    API_KEY: str = os.getenv('API_KEY')
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    MAX_CONNECTIONS: int = int(os.getenv('MAX_CONNECTIONS', '10'))

config = Config()

# 避免 - 硬编码配置
class BadConfig:
    DATABASE_URL = "mysql://user:pass@localhost:3306/db"
    API_KEY = "sk-1234567890abcdef"
```

## 可维护性实践

### 配置外部化
```yaml
# config.yml
database:
  host: localhost
  port: 5432
  name: myapp
  pool_size: 10

cache:
  provider: redis
  ttl: 3600
  
logging:
  level: INFO
  file: app.log
```

### 依赖注入
```python
# 好的做法 - 依赖注入
class PaymentService:
    def __init__(self, payment_gateway, email_service):
        self.gateway = payment_gateway
        self.email_service = email_service
    
    def process_payment(self, amount, customer_email):
        result = self.gateway.charge(amount)
        if result.success:
            self.email_service.send_receipt(customer_email, amount)
        return result

# 便于测试和替换实现
```

这些最佳实践可以作为代码审查的参考标准，帮助识别代码中的改进机会并提供具体的修改建议。