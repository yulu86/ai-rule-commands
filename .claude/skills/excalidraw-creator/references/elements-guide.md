# Excalidraw 元素类型和属性指南

## 基础元素类型

### 1. 矩形 (rectangle)
**用途**: 容器、流程步骤、功能模块
```javascript
// 基本参数
{
  type: "rectangle",
  x: 100,        // X坐标
  y: 100,        // Y坐标  
  width: 200,    // 宽度
  height: 100,   // 高度
  backgroundColor: "#ffffff",
  strokeColor: "#000000",
  strokeWidth: 2,
  roughness: 1,
  opacity: 1
}
```

**常用变体**:
- 流程步骤：白色背景，黑色边框
- 数据存储：浅蓝色背景
- 重要模块：浅黄色背景

### 2. 椭圆 (ellipse)  
**用途**: 起止点、强调内容、圆形元素
```javascript
{
  type: "ellipse", 
  x: 150,
  y: 150,
  width: 120,
  height: 80,
  backgroundColor: "#a5d8ff",
  strokeColor: "#1971c2"
}
```

**常用场景**:
- 开始/结束：绿色/红色椭圆
- 关键决策：橙色椭圆
- 循环返回：蓝色椭圆

### 3. 菱形 (diamond)
**用途**: 决策点、判断条件、分支节点
```javascript
{
  type: "diamond",
  x: 200,
  y: 200, 
  width: 160,
  height: 120,
  backgroundColor: "#fff3bf",
  strokeColor: "#f08c00"
}
```

**标准配色**:
- 普通决策：黄色背景
- 重要决策：橙色背景
- 风险决策：红色背景

### 4. 箭头 (arrow)
**用途**: 连接元素、流程方向、数据流向
```javascript
{
  type: "arrow",
  x: 300, y: 150,    // 起点坐标
  width: 200,         // X方向偏移
  height: 0,          // Y方向偏移  
  points: [[0, 0], [100, 0]], // 箭头点数组
  strokeColor: "#000000",
  strokeWidth: 2
}
```

**箭头类型**:
- 实线箭头：正常流程
- 虚线箭头：可选流程
- 双向箭头：双向交互

### 5. 文本 (text)
**用途**: 标注、说明、标题
```javascript
{
  type: "text",
  x: 250,
  y: 180,
  text: "处理步骤",
  fontSize: 20,
  fontFamily: "Virgil, sans-serif",
  textAlign: "center",
  verticalAlign: "middle"
}
```

**字体规范**:
- 标题：24-32px，粗体
- 正文：16-20px，常规
- 注释：12-14px，斜体

### 6. 标签 (label)  
**用途**: 简短说明、连接线标注
```javascript
{
  type: "label",
  x: 400,
  y: 120,
  text: "确认",
  fontSize: 14
}
```

## 高级属性

### 颜色系统
**基础颜色**:
- 黑色: `#000000`
- 白色: `#ffffff` 
- 灰色: `#868e96`
- 红色: `#ff6b6b`
- 绿色: `#51cf66`
- 蓝色: `#339af0`
- 黄色: `#ffd43b`
- 橙色: `#ff922b`

**系统颜色**:
- 主色调: `#1971c2` (深蓝)
- 辅助色: `#40c057` (绿色)
- 警告色: `#f59f00` (橙色)
- 错误色: `#fa5252` (红色)

### 样式属性
**粗糙度 (roughness)**:
- 0: 完全平滑
- 1: 轻微手绘效果 (推荐)
- 2: 中等手绘效果
- 3: 明显手绘效果

**透明度 (opacity)**:
- 1.0: 完全不透明
- 0.8: 轻微透明
- 0.6: 半透明
- 0.4: 明显透明

**边框粗细 (strokeWidth)**:
- 1: 细线 (辅助线)
- 2: 标准 (推荐)
- 3: 粗线 (强调)
- 4: 特粗 (重要元素)

## 元素组织

### 分组 (Group)
相关元素应该分组，便于整体操作：
```javascript
// 使用相同的前缀或标识符
group_1_rect_1, group_1_text_1, group_1_arrow_1
```

### 层次结构
1. **背景层** - 容器、框架
2. **内容层** - 主要形状、流程步骤  
3. **连接层** - 箭头、连接线
4. **标注层** - 文本、标签、注释

## 常见组合模式

### 流程步骤组合
```
矩形(步骤名称) + 箭头 + 下一个矩形
```

### 决策分支组合  
```
菱形(决策条件) + 多个箭头 + 分支说明
```

### 容器内容组合
```
大矩形(容器) + 小矩形(内容) + 标签(容器名称)
```