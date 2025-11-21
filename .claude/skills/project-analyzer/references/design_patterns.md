# 设计模式参考指南

## 创建型模式 (Creational Patterns)

### Singleton (单例模式)
**特征**:
- 确保类只有一个实例
- 提供全局访问点
- 常用于配置管理器、连接池等

**代码特征**:
- 私有构造函数
- 静态实例变量
- getInstance()方法

**识别关键词**: `singleton`, `instance`, `getInstance`, `_instance`

### Factory Method (工厂方法模式)
**特征**:
- 定义创建对象的接口
- 让子类决定实例化哪个类
- 解耦对象的创建和使用

**代码特征**:
- create或build开头的方法
- 抽象创建方法
- 具体工厂类

**识别关键词**: `factory`, `create`, `build`, `make`

### Abstract Factory (抽象工厂模式)
**特征**:
- 提供创建一系列相关对象的接口
- 支持多个产品族
- 常用于UI组件库

**代码特征**:
- 多个创建方法
- 产品族概念
- 抽象工厂接口

**识别关键词**: `abstract factory`, `factory`, `family`

### Builder (建造者模式)
**特征**:
- 分步骤创建复杂对象
- 支持不同的表示
- 常用于配置对象构建

**代码特征**:
- 链式调用方法
- with、set、add前缀方法
- build()或create()终结方法

**识别关键词**: `builder`, `build`, `with`, `set`, `add`

### Prototype (原型模式)
**特征**:
- 通过克隆创建对象
- 避免构造函数的复杂性
- 常用于对象复制

**代码特征**:
- clone()方法
- copy()方法
- 原型接口

**识别关键词**: `prototype`, `clone`, `copy`

## 结构型模式 (Structural Patterns)

### Adapter (适配器模式)
**特征**:
- 转换接口以兼容不同系统
- 包装现有类
- 常用于第三方库集成

**代码特征**:
- 包装类
- 接口转换方法
- 适配器后缀

**识别关键词**: `adapter`, `wrapper`, `convert`, `adapter`

### Decorator (装饰器模式)
**特征**:
- 动态添加对象功能
- 不改变对象结构
- 常用于AOP、日志记录

**代码特征**:
- 装饰器类
- @符号 (Python/TypeScript)
- 包装原有方法

**识别关键词**: `decorator`, `wrapper`, `@`

### Facade (外观模式)
**特征**:
- 简化复杂子系统接口
- 提供高级接口
- 常用于API封装

**代码特征**:
- 管理器类
- 简化的接口方法
- 内部复杂性隐藏

**识别关键词**: `facade`, `manager`, `controller`

### Proxy (代理模式)
**特征**:
- 控制对对象的访问
- 延迟加载
- 常用于缓存、安全控制

**代码特征**:
- 代理类
- 与被代理对象相同接口
- 访问控制逻辑

**识别关键词**: `proxy`, `surrogate`, `handler`

### Composite (组合模式)
**特征**:
- 组合对象和叶子对象
- 树形结构
- 常用于UI组件、文件系统

**代码特征**:
- 组合节点类
- 叶子节点类
- 统一接口

**识别关键词**: `composite`, `component`, `leaf`, `node`, `tree`

### Bridge (桥接模式)
**特征**:
- 分离抽象和实现
- 独立变化
- 常用于平台无关的UI

**代码特征**:
- 抽象类
- 实现类
- 桥接引用

**识别关键词**: `bridge`, `abstraction`, `implementation`

### Flyweight (享元模式)
**特征**:
- 共享细粒度对象
- 减少内存使用
- 常用于文本编辑器、游戏

**代码特征**:
- 对象池
- 共享对象
- 内在状态/外在状态分离

**识别关键词**: `flyweight`, `pool`, `shared`, `cache`

## 行为型模式 (Behavioral Patterns)

### Observer (观察者模式)
**特征**:
- 一对多依赖关系
- 状态变化通知
- 常用于事件处理

**代码特征**:
- 观察者列表
- 通知方法
- 订阅/取消订阅

**识别关键词**: `observer`, `subject`, `notify`, `subscribe`, `listen`, `event`

### Strategy (策略模式)
**特征**:
- 封装算法族
- 运行时选择算法
- 常用于排序、支付方式

**代码特征**:
- 策略接口
- 具体策略类
- 上下文类

**识别关键词**: `strategy`, `algorithm`, `policy`

### Command (命令模式)
**特征**:
- 封装请求为对象
- 支持撤销/重做
- 常用于菜单操作、宏命令

**代码特征**:
- 命令接口
- 具体命令类
- 执行方法

**识别关键词**: `command`, `execute`, `invoke`, `action`

### State (状态模式)
**特征**:
- 对象状态改变行为
- 状态转换
- 常于工作流、游戏

**代码特征**:
- 状态接口
- 具体状态类
- 上下文类

**识别关键词**: `state`, `context`, `transition`

### Template Method (模板方法模式)
**特征**:
- 定义算法骨架
- 子类实现具体步骤
- 常于框架设计

**代码特征**:
- 抽象模板类
- 具体子类
- 钩子方法

**识别关键词**: `template`, `abstract`, `hook`, `base`

### Iterator (迭代器模式)
**特征**:
- 访问集合元素
- 不暴露内部结构
- 常于数据结构遍历

**代码特征**:
- 迭代器接口
- hasNext()、next()方法
- 集合类

**识别关键词**: `iterator`, `iterate`, `traverse`

### Mediator (中介者模式)
**特征**:
- 协调对象交互
- 减少耦合
- 常于GUI、聊天室

**代码特征**:
- 中介者类
- 同事类
- 通信方法

**识别关键词**: `mediator`, `colleague`, `coordinator`

### Memento (备忘录模式)
**特征**:
- 保存对象状态
- 支持撤销
- 常于编辑器、游戏存档

**代码特征**:
- 备忘录类
- 状态保存/恢复
- 原发器类

**识别关键词**: `memento`, `snapshot`, `undo`, `restore`

### Visitor (访问者模式)
**特征**:
- 分离操作和数据结构
- 添加新操作
- 常于编译器、文档处理

**代码特征**:
- 访问者接口
- 具体访问者类
- accept()方法

**识别关键词**: `visitor`, `accept`, `visit`

### Chain of Responsibility (责任链模式)
**特征**:
- 链式处理请求
- 动态处理链
- 常于日志记录、异常处理

**代码特征**:
- 处理者链
- successor引用
- 处理方法

**识别关键词**: `chain`, `handler`, `successor`, `pipeline`

## 架构模式识别

### 分层架构 (Layered Architecture)
**特征**:
- 表现层、业务层、数据层
- 单向依赖
- 清晰的职责分离

**识别特征**:
- presentation, business, data目录
- controller, service, repository模式
- 依赖注入

### MVC/MVVM模式
**特征**:
- Model-View-Controller/ViewModel
- 关注点分离
- 数据绑定

**识别特征**:
- models, views, controllers目录
- 数据绑定框架
- 视图模板

### 微服务架构 (Microservices)
**特征**:
- 独立部署的服务
- API通信
- 去中心化数据管理

**识别特征**:
- 多个service目录
- API网关配置
- Docker配置

### 事件驱动架构 (Event-Driven)
**特征**:
- 事件发布/订阅
- 松耦合
- 异步通信

**识别特征**:
- event, eventbus目录
- 消息队列配置
- 异步处理

### 插件架构 (Plugin Architecture)
**特征**:
- 核心系统+插件
- 动态加载
- 可扩展性

**识别特征**:
- plugins目录
- 插件接口定义
- 动态加载机制