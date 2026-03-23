# Minimax Image Generation Skills for OpenClaw

[English](#english) | [中文](#中文)

---

## English

### Overview

This is an **OpenClaw Skill** for generating images via the MiniMax API. It supports **Text-to-Image (T2I)** and **Image-to-Image (I2I)** generation.

### Features

- **Text-to-Image**: Generate images from text prompts
- **Image-to-Image**: Create variations based on a reference image (maintains character features)
- **Multiple Aspect Ratios**: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9
- **Multiple Output**: Generate 1-9 images in one request
- **Style Models** (requires premium subscription): Comic, Energetic, Medieval, Watercolor

### Requirements

- **MiniMax API Key** — Get it from [MiniMax Platform](https://platform.minimaxi.com)
- OpenClaw environment

### Installation

1. Install via ClawHub:
```bash
npx clawhub install lx-minimax
```

2. Set environment variable:
```bash
export MINIMAX_API_KEY="your-api-key-here"
```

### Quick Start

```bash
# Text-to-Image
python3 scripts/image_gen.py -p "A cute orange cat sleeping in sunlight" -r "16:9" -n 2

# Image-to-Image
python3 scripts/image_gen.py -p "Wearing a suit" -r "3:4" --reference "https://example.com/photo.jpg"

# With style (premium)
python3 scripts/image_gen.py -p "Sunset at the beach" -s "watercolor" -r "16:9"
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `-p, --prompt` | Required | Image description (max 1500 chars) |
| `-m, --model` | image-01 | Model: `image-01` or `image-01-live` |
| `-r, --ratio` | 1:1 | Aspect ratio |
| `-n` | 1 | Number of images [1-9] |
| `-s, --style` | - | Style type (image-01-live only) |
| `--reference` | - | Reference image URL or base64 (for I2I) |

### Security Notes

- 🔐 Never commit your API key to version control
- 🔗 Reference image URLs are sent to the MiniMax API
- ⚠️ Do not use sensitive/private image URLs unless you trust the service

### License

MIT License

---

## 中文

### 概述

这是面向 **OpenClaw** 的 **MiniMax 图片生成 Skill**。支持**文生图（T2I）**和**图生图（I2I）**两种模式。

### 功能特点

- **文生图**：根据文字描述生成图片
- **图生图**：基于参考图生成新图，保持人物主体特征
- **多种比例**：1:1、16:9、4:3、3:2、2:3、3:4、9:16、21:9
- **批量生成**：单次请求可生成1-9张图片
- **画风模式**（需会员订阅）：漫画、元气、中世纪、水彩

### 环境要求

- **MiniMax API Key** — 从 [MiniMax 开放平台](https://platform.minimaxi.com) 获取
- OpenClaw 环境

### 安装方式

1. 通过 ClawHub 安装：
```bash
npx clawhub install lx-minimax
```

2. 设置环境变量：
```bash
export MINIMAX_API_KEY="your-api-key-here"
```

### 快速开始

```bash
# 文生图
python3 scripts/image_gen.py -p "一只可爱的橘猫在阳光下打盹" -r "16:9" -n 2

# 图生图
python3 scripts/image_gen.py -p "穿着西装" -r "3:4" --reference "https://example.com/photo.jpg"

# 画风模式（会员）
python3 scripts/image_gen.py -p "海边日落" -s "水彩" -r "16:9"
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-p, --prompt` | 必填 | 图片描述（最长1500字符） |
| `-m, --model` | image-01 | 模型：`image-01` 或 `image-01-live` |
| `-r, --ratio` | 1:1 | 宽高比 |
| `-n` | 1 | 生成数量 [1-9] |
| `-s, --style` | - | 画风类型（仅 image-01-live） |
| `--reference` | - | 参考图URL或base64（图生图用） |

### 安全须知

- 🔐 切勿将 API Key 提交到版本控制
- 🔗 参考图URL会发送到 MiniMax API
- ⚠️ 请勿使用敏感/私有图片URL，除非你信任该服务商

### 开源协议

MIT License
