# JavaScript/TypeScript 代码审查指南

## 🔴 高优先级问题

### 异步处理问题

#### Promise错误处理不完整
```javascript
// ❌ 问题：缺少错误处理
fetch('/api/user')
  .then(response => response.json())
  .then(data => console.log(data));

// ✅ 改进：添加错误处理
fetch('/api/user')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.error('Fetch error:', error));

// ✅ 更好：使用async/await
async function fetchUser() {
  try {
    const response = await fetch('/api/user');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Fetch error:', error);
  }
}
```

#### 竞态条件
```javascript
// ❌ 问题：竞态条件
let userId = null;
async function loadUser() {
  const response = await fetch('/api/current-user');
  userId = (await response.json()).id;
}

async function updateProfile(data) {
  await loadUser();
  return fetch(`/api/users/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
}

// ✅ 改进：确保顺序执行
class UserService {
  constructor() {
    this.currentUser = null;
    this.loadingPromise = null;
  }
  
  async getCurrentUser() {
    if (this.currentUser) return this.currentUser;
    
    if (!this.loadingPromise) {
      this.loadingPromise = this.loadUser();
    }
    
    return this.loadingPromise;
  }
  
  async loadUser() {
    const response = await fetch('/api/current-user');
    this.currentUser = await response.json();
    return this.currentUser;
  }
  
  async updateProfile(data) {
    const user = await this.getCurrentUser();
    const response = await fetch(`/api/users/${user.id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
    return response.json();
  }
}
```

### 内存泄漏问题

#### 事件监听器未清理
```javascript
// ❌ 问题：事件监听器未清理
class Component {
  constructor(element) {
    this.element = element;
    this.element.addEventListener('click', this.handleClick.bind(this));
  }
  
  handleClick() {
    console.log('clicked');
  }
}

// ✅ 改进：添加清理方法
class Component {
  constructor(element) {
    this.element = element;
    this.handleClick = this.handleClick.bind(this);
    this.element.addEventListener('click', this.handleClick);
  }
  
  handleClick() {
    console.log('clicked');
  }
  
  destroy() {
    this.element.removeEventListener('click', this.handleClick);
    this.element = null;
  }
}
```

#### 定时器未清理
```javascript
// ❌ 问题：定时器可能造成内存泄漏
function startPolling() {
  setInterval(() => {
    fetch('/api/status').then(/* ... */);
  }, 5000);
}

// ✅ 改进：提供清理机制
class PollingService {
  constructor() {
    this.intervals = [];
  }
  
  startPolling(callback, interval = 5000) {
    const intervalId = setInterval(callback, interval);
    this.intervals.push(intervalId);
    return intervalId;
  }
  
  stopPolling(intervalId) {
    clearInterval(intervalId);
    this.intervals = this.intervals.filter(id => id !== intervalId);
  }
  
  stopAll() {
    this.intervals.forEach(id => clearInterval(id));
    this.intervals = [];
  }
}
```

### 安全问题

#### XSS防护
```javascript
// ❌ 问题：XSS漏洞
function renderUserContent(content) {
  document.getElementById('output').innerHTML = content;
}

// ✅ 改进：HTML转义
function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function renderUserContent(content) {
  const safeContent = escapeHtml(content);
  document.getElementById('output').textContent = safeContent;
}

// ✅ 更好：使用DOMPurify库
import DOMPurify from 'dompurify';
function renderUserContent(content) {
  const cleanContent = DOMPurify.sanitize(content);
  document.getElementById('output').innerHTML = cleanContent;
}
```

#### 敏感数据处理
```javascript
// ❌ 问题：敏感信息暴露在客户端
const API_KEY = 'sk-1234567890abcdef';
const config = {
  database: {
    password: 'admin123',
    host: 'production-db.example.com'
  }
};

// ✅ 改进：敏感信息放在环境变量中
const config = {
  apiKey: process.env.REACT_APP_API_KEY,
  apiUrl: process.env.REACT_APP_API_URL
};
```

## 🟡 中优先级问题

### 性能优化

#### 不必要的重新渲染
```javascript
// ❌ 问题：不必要的重新计算
function ExpensiveComponent({ items }) {
  const expensiveValue = items.reduce((sum, item) => {
    // 复杂计算
    return sum + calculateComplexValue(item);
  }, 0);
  
  return <div>{expensiveValue}</div>;
}

// ✅ 改进：使用useMemo
import React, { useMemo } from 'react';

function ExpensiveComponent({ items }) {
  const expensiveValue = useMemo(() => {
    return items.reduce((sum, item) => {
      return sum + calculateComplexValue(item);
    }, 0);
  }, [items]);
  
  return <div>{expensiveValue}</div>;
}
```

#### 数组操作优化
```javascript
// ❌ 问题：低效的数组操作
function processLargeArray(items) {
  const result = [];
  for (let i = 0; i < items.length; i++) {
    if (items[i].active) {
      result.push(items[i].value * 2);
    }
  }
  return result;
}

// ✅ 改进：使用函数式方法
function processLargeArray(items) {
  return items
    .filter(item => item.active)
    .map(item => item.value * 2);
}

// ✅ 更好：对于大数据集使用流式处理
function* processItems(items) {
  for (const item of items) {
    if (item.active) {
      yield item.value * 2;
    }
  }
}
```

### 代码质量

#### 过度使用全局变量
```javascript
// ❌ 问题：全局状态污染
let currentUser = null;
let isLoading = false;

function loadUser() {
  isLoading = true;
  // ...
}

// ✅ 改进：使用模块化的状态管理
class UserStore {
  constructor() {
    this.currentUser = null;
    this.isLoading = false;
    this.listeners = [];
  }
  
  setLoading(loading) {
    this.isLoading = loading;
    this.notifyListeners();
  }
  
  setCurrentUser(user) {
    this.currentUser = user;
    this.notifyListeners();
  }
  
  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }
  
  notifyListeners() {
    this.listeners.forEach(listener => listener(this));
  }
}

const userStore = new UserStore();
export default userStore;
```

#### 魔法数字和字符串
```javascript
// ❌ 问题：魔法数字
function calculatePrice(basePrice, quantity) {
  if (quantity > 100) {
    return basePrice * 0.8; // 20% discount
  } else if (quantity > 50) {
    return basePrice * 0.9; // 10% discount
  }
  return basePrice;
}

// ✅ 改进：使用常量
const DISCOUNT_THRESHOLDS = {
  BULK_QUANTITY: 100,
  MEDIUM_QUANTITY: 50
};

const DISCOUNT_RATES = {
  BULK: 0.2,
  MEDIUM: 0.1
};

function calculatePrice(basePrice, quantity) {
  if (quantity > DISCOUNT_THRESHOLDS.BULK_QUANTITY) {
    return basePrice * (1 - DISCOUNT_RATES.BULK);
  } else if (quantity > DISCOUNT_THRESHOLDS.MEDIUM_QUANTITY) {
    return basePrice * (1 - DISCOUNT_RATES.MEDIUM);
  }
  return basePrice;
}
```

## 🟢 低优先级问题

### 代码风格

#### 一致性命名
```javascript
// ❌ 问题：命名不一致
const getUserInfo = () => { /* ... */ };
const get_user_data = () => { /* ... */ };
const FetchUserDetails = () => { /* ... */ };

// ✅ 改进：统一的命名规范
const getUserInfo = () => { /* ... */ };
const getUserData = () => { /* ... */ };
const fetchUserDetails = () => { /* ... */ };
```

#### 函数长度控制
```javascript
// ❌ 问题：函数过长
function processOrder(order) {
  // 验证订单 (15行)
  if (!order.items || order.items.length === 0) {
    throw new Error('Order must have items');
  }
  // ... 更多验证逻辑
  
  // 计算价格 (20行)
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }
  // ... 更多计算逻辑
  
  // 发送确认邮件 (10行)
  // ... 邮件发送逻辑
}

// ✅ 改进：拆分为小函数
class OrderProcessor {
  validateOrder(order) {
    if (!order.items || order.items.length === 0) {
      throw new Error('Order must have items');
    }
    // 更多验证逻辑
  }
  
  calculateTotal(order) {
    return order.items.reduce((total, item) => {
      return total + (item.price * item.quantity);
    }, 0);
  }
  
  sendConfirmationEmail(order) {
    // 邮件发送逻辑
  }
  
  processOrder(order) {
    this.validateOrder(order);
    const total = this.calculateTotal(order);
    this.sendConfirmationEmail(order);
    return { order, total };
  }
}
```

## TypeScript 特定问题

### 类型定义不完整
```typescript
// ❌ 问题：类型定义不完整
interface User {
  name: string;
}

// 可能为null的属性没有类型说明
function getUserAge(user: User): number {
  return user.age; // 编译错误，但类型定义不完整
}

// ✅ 改进：完整的类型定义
interface User {
  id: string;
  name: string;
  email: string;
  age?: number; // 可选属性
  createdAt: Date;
  updatedAt: Date;
}

function getUserAge(user: User): number | undefined {
  return user.age; // 正确处理可选属性
}
```

### 过度使用any类型
```typescript
// ❌ 问题：过度使用any
function processData(data: any): any {
  return data.map((item: any) => item.value * 2);
}

// ✅ 改进：具体类型定义
interface DataItem {
  id: string;
  value: number;
  category: string;
}

function processData(items: DataItem[]): number[] {
  return items.map(item => item.value * 2);
}

// ✅ 更好：泛型函数
function extractValues<T extends { value: number }>(items: T[]): number[] {
  return items.map(item => item.value * 2);
}
```

## 框架特定检查

### React Hooks
```javascript
// ❌ 问题：在条件中使用hooks
function MyComponent({ shouldFetch }) {
  const [data, setData] = useState(null);
  
  if (shouldFetch) {
    useEffect(() => {
      fetch('/api/data').then(setData);
    }, []);
  }
  
  return <div>{data}</div>;
}

// ✅ 改进：正确的hooks使用
function MyComponent({ shouldFetch }) {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    if (shouldFetch) {
      fetch('/api/data').then(setData);
    }
  }, [shouldFetch]);
  
  return <div>{data}</div>;
}

// ❌ 问题：依赖数组不正确
useEffect(() => {
  setCount(count + 1);
}, []); // 缺少count依赖

// ✅ 改进：正确的依赖
useEffect(() => {
  setCount(prevCount => prevCount + 1);
}, []); // 使用函数式更新
```

### Node.js 最佳实践
```javascript
// ❌ 问题：同步I/O操作
function readConfig() {
  const data = fs.readFileSync('/config.json');
  return JSON.parse(data);
}

// ✅ 改进：异步I/O操作
async function readConfig() {
  try {
    const data = await fs.promises.readFile('/config.json');
    return JSON.parse(data);
  } catch (error) {
    console.error('Failed to read config:', error);
    return {};
  }
}

// ❌ 问题：错误处理不完整
function createUser(userData) {
  db.query('INSERT INTO users SET ?', userData, (err, result) => {
    if (err) {
      console.log('Error creating user');
    }
    return result;
  });
}

// ✅ 改进：完善的错误处理
async function createUser(userData) {
  try {
    const result = await db.query('INSERT INTO users SET ?', userData);
    return result;
  } catch (error) {
    console.error('Error creating user:', error);
    throw new Error('Failed to create user');
  }
}
```

这些检查点可以帮助识别JavaScript/TypeScript代码中的常见问题，并提供具体的改进建议。