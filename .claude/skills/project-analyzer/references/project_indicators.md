# 项目技术栈识别指标

## Web前端项目

### 框架识别指标

#### React
**配置文件**:
- `package.json` - 包含 "react", "react-dom"
- `webpack.config.js` - React相关配置
- `next.config.js` - Next.js框架
- `vite.config.js` - Vite构建工具

**目录结构**:
```
src/
├── components/     # 组件目录
├── pages/         # 页面目录 (Next.js)
├── hooks/         # 自定义Hook
├── utils/         # 工具函数
├── styles/        # 样式文件
└── App.js         # 根组件
```

**文件特征**:
- `.jsx`, `.tsx` 文件扩展名
- `import React from 'react'`
- `useState`, `useEffect` Hook
- JSX语法

#### Vue.js
**配置文件**:
- `package.json` - 包含 "vue"
- `vue.config.js` - Vue CLI配置
- `vite.config.js` - Vue 3 + Vite
- `nuxt.config.js` - Nuxt.js框架

**目录结构**:
```
src/
├── components/    # 组件目录
├── views/         # 页面目录
├── router/        # 路由配置
├── store/         # 状态管理
├── assets/        # 静态资源
└── App.vue        # 根组件
```

**文件特征**:
- `.vue` 文件扩展名
- `<template>`, `<script>`, `<style>` 块
- `export default`
- Vue指令语法

#### Angular
**配置文件**:
- `package.json` - 包含 "@angular/*"
- `angular.json` - Angular CLI配置
- `tsconfig.json` - TypeScript配置

**目录结构**:
```
src/
├── app/
│   ├── components/  # 组件目录
│   ├── services/    # 服务目录
│   ├── models/      # 模型目录
│   └── modules/     # 模块目录
├── assets/          # 静态资源
└── environments/    # 环境配置
```

**文件特征**:
- `.ts` 文件扩展名
- `@Component`, `@Injectable` 装饰器
- NgModule
- TypeScript语法

### 构建工具识别

#### Webpack
**配置文件**:
- `webpack.config.js`
- `webpack.config.ts`
- `webpack.*.config.js`

**特征**:
- module.rules 配置
- plugins 配置
- entry/output 配置

#### Vite
**配置文件**:
- `vite.config.js`
- `vite.config.ts`

**特征**:
- devServer 配置
- plugins 配置
- esbuild 构建

#### Parcel
**配置文件**:
- `.parcelrc`
- `package.json` 中的 parcel 脚本

**特征**:
- 零配置
- 自动依赖安装

## Web后端项目

### Node.js后端

#### Express.js
**配置文件**:
- `package.json` - 包含 "express"
- `app.js` 或 `index.js` - 入口文件

**目录结构**:
```
src/
├── routes/        # 路由定义
├── controllers/   # 控制器
├── models/        # 数据模型
├── middleware/    # 中间件
├── utils/         # 工具函数
├── config/        # 配置文件
└── app.js         # 应用入口
```

**代码特征**:
- `const express = require('express')`
- `app.get()`, `app.post()`
- 中间件使用
- 路由定义

#### Koa.js
**配置文件**:
- `package.json` - 包含 "koa"
- `app.js` 或 `index.js`

**特征**:
- `const Koa = require('koa')`
- async/await 中间件
- Context 对象
- 洋葱模型中间件

#### NestJS
**配置文件**:
- `package.json` - 包含 "@nestjs/*"
- `nest-cli.json` - CLI配置
- `tsconfig.json` - TypeScript配置

**目录结构**:
```
src/
├── modules/       # 模块目录
├── controllers/   # 控制器
├── services/      # 服务
├── entities/      # 实体
├── dto/          # 数据传输对象
└── main.ts       # 应用入口
```

**特征**:
- `@Controller`, `@Injectable` 装饰器
- 模块化架构
- TypeScript支持

### Python后端

#### Django
**配置文件**:
- `manage.py` - Django管理脚本
- `requirements.txt` - 依赖列表
- `settings.py` - 项目配置
- `urls.py` - URL配置

**目录结构**:
```
project/
├── app1/
│   ├── models.py     # 数据模型
│   ├── views.py      # 视图函数
│   ├── urls.py       # URL路由
│   └── tests.py      # 测试文件
├── project/
│   ├── settings.py   # 项目配置
│   └── urls.py       # 根URL配置
└── manage.py         # 管理脚本
```

**特征**:
- `from django.db import models`
- `from django.shortcuts import render`
- MTV架构模式
- ORM使用

#### Flask
**配置文件**:
- `app.py` 或 `application.py` - 应用入口
- `requirements.txt` - 依赖列表
- `config.py` - 配置文件

**目录结构**:
```
app/
├── routes/       # 路由定义
├── models/       # 数据模型
├── templates/    # 模板文件
├── static/       # 静态文件
└── app.py        # 应用入口
```

**特征**:
- `from flask import Flask, render_template`
- 蓝图 (Blueprint) 使用
- 装饰器路由
- Jinja2模板

#### FastAPI
**配置文件**:
- `requirements.txt` - 包含 "fastapi"
- `main.py` - 应用入口

**特征**:
- `from fastapi import FastAPI`
- 类型注解
- 自动API文档
- Pydantic模型验证

### Java后端

#### Spring Boot
**配置文件**:
- `pom.xml` 或 `build.gradle` - 构建配置
- `application.properties` 或 `application.yml` - 应用配置

**目录结构**:
```
src/main/java/
├── controller/    # 控制器
├── service/       # 服务层
├── repository/    # 数据访问层
├── entity/        # 实体类
├── config/        # 配置类
└── Application.java # 应用入口
```

**特征**:
- `@RestController`, `@Service`, `@Repository` 注解
- `@SpringBootApplication` 主类
- 自动配置
- 依赖注入

## 移动应用项目

### React Native
**配置文件**:
- `package.json` - 包含 "react-native"
- `metro.config.js` - Metro打包配置
- `babel.config.js` - Babel配置

**目录结构**:
```
android/           # Android原生代码
ios/              # iOS原生代码
src/
├── components/    # 组件目录
├── screens/       # 页面目录
├── navigation/    # 导航配置
├── utils/         # 工具函数
└── App.js         # 应用入口
```

**特征**:
- React组件
- 原生模块桥接
- 平台特定代码

### Flutter
**配置文件**:
- `pubspec.yaml` - 项目配置
- `analysis_options.yaml` - 分析选项

**目录结构**:
```
lib/
├── main.dart          # 应用入口
├── screens/           # 页面目录
├── widgets/           # 组件目录
├── services/          # 服务目录
├── models/            # 模型目录
└── utils/             # 工具目录
android/               # Android原生代码
ios/                  # iOS原生代码
```

**特征**:
- Dart语言
- Widget树结构
- 热重载支持

## 桌面应用项目

### Electron
**配置文件**:
- `package.json` - 包含 "electron"
- `electron-builder.json` - 打包配置

**目录结构**:
```
src/
├── main/          # 主进程代码
├── renderer/      # 渲染进程代码
├── preload/       # 预加载脚本
└── build/         # 构建输出
```

**特征**:
- 主进程/渲染进程分离
- Web技术栈
- 跨平台支持

### Qt项目
**配置文件**:
- `CMakeLists.txt` - CMake构建配置
- `.pro` 文件 - qmake项目文件

**目录结构**:
```
src/
├── main.cpp       # 程序入口
├── mainwindow.cpp # 主窗口
├── widgets/       # 自定义控件
├── resources/     # 资源文件
└── ui/           # UI表单文件
```

**特征**:
- C++代码
- Qt框架
- 信号槽机制

## 数据科学项目

### 机器学习项目
**配置文件**:
- `requirements.txt` - Python依赖
- `environment.yml` - Conda环境
- `Dockerfile` - 容器配置

**目录结构**:
```
data/
├── raw/           # 原始数据
├── processed/     # 处理后数据
└── models/        # 训练模型
notebooks/         # Jupyter笔记本
src/
├── data/          # 数据处理
├── features/      # 特征工程
├── models/        # 模型定义
├── training/      # 训练脚本
└── evaluation/    # 评估脚本
```

**特征**:
- Jupyter笔记本
- 数据可视化
- 模型训练脚本
- 实验跟踪

### 数据分析项目
**文件类型**:
- `.ipynb` - Jupyter笔记本
- `.py` - Python脚本
- `.R` - R语言脚本
- `.sql` - SQL查询

**依赖识别**:
- `pandas`, `numpy`, `matplotlib`, `seaborn`
- `scikit-learn`, `tensorflow`, `pytorch`
- `jupyter`, `ipykernel`

## 数据库相关项目

### 识别指标

#### SQL数据库
- `.sql` 文件
- `schema.sql` 或 `database.sql`
- `migrations/` 目录
- ORM配置文件

#### NoSQL数据库
- MongoDB配置
- Redis配置
- Elasticsearch配置
- 数据模型定义

#### 数据库工具
- `alembic/` - SQLAlchemy迁移
- `flyway/` - Java数据库迁移
- `liquibase/` - 数据库版本控制

## 项目质量指标

### 代码质量
- 测试覆盖率
- 代码复杂度
- 文档完整性
- 代码风格一致性

### 架构质量
- 模块化程度
- 依赖关系清晰度
- 设计模式使用
- 错误处理机制

### 安全性
- 敏感信息处理
- 输入验证
- 认证授权机制
- 依赖安全性

### 性能
- 响应时间
- 资源使用效率
- 扩展性
- 缓存策略

### 可维护性
- 代码可读性
- 模块化设计
- 配置管理
- 日志记录