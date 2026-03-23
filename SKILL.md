---
name: minimax-image
description: MiniMax文生图(T2I)和图生图(I2I)工具 / MiniMax image generation tool supporting T2I and I2I. Generate 1-9 images per request with customizable aspect ratios.
homepage: https://github.com/lixiang92229/lx-minimax
---

# MiniMax Image Generation Skill

## 概述 | Overview

通过 MiniMax API 实现**文生图（T2I）**和**图生图（I2I）**功能。

Supports **Text-to-Image** and **Image-to-Image** generation via MiniMax API.

## 功能 | Features

### 1. 文生图 Text-to-Image

根据文字描述生成图片 / Generate images from text prompts:

```python
from scripts.image_gen import generate_image

result = generate_image(
    prompt="北京故宫角楼，晴空万里，摄影作品",
    model="image-01",
    aspect_ratio="16:9",
    n=2
)
```

### 2. 图生图 Image-to-Image

基于参考图片生成新图，保持人物主体特征 / Create variations using a reference image:

```python
result = generate_image(
    prompt="穿着中国传统服装，站在长城上",
    model="image-01",
    aspect_ratio="3:4",
    subject_reference=[
        {
            "type": "character",
            "image_file": "https://example.com/photo.jpg"  # 或 base64 Data URL
        }
    ],
    n=1
)
```

### 3. 画风生成 Style Models (需要订阅 / Requires subscription)

使用 `image-01-live` 模型指定画风 / Specify artistic styles:

| 风格 Style | 说明 |
|-----------|------|
| 漫画 | Comic/ Manga |
| 元气 | Energetic/ Youthful |
| 中世纪 | Medieval |
| 水彩 | Watercolor |

```python
result = generate_image(
    prompt="一位中国科学家在实验室",
    model="image-01-live",
    style_type="水彩",
    style_weight=0.8
)
```

## 命令行使用 | CLI Usage

```bash
# 1. 设置环境变量 / Set environment variable
export MINIMAX_API_KEY="your-api-key-here"

# 2. 文生图 / Text-to-Image
python3 scripts/image_gen.py -p "一只可爱的橘猫在阳光下打盹" -r "16:9" -n 2

# 3. 图生图 / Image-to-Image
python3 scripts/image_gen.py -p "穿着西装" -r "3:4" --reference "https://example.com/photo.jpg"

# 4. 指定画风 / With style
python3 scripts/image_gen.py -p "海边日落" -s "水彩" -r "16:9"
```

## 参数说明 | Parameters

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--prompt, -p` | 必填 | 图片描述，最长1500字符 / Image description, max 1500 chars |
| `--model, -m` | image-01 | 模型 / Model: `image-01` 或 `image-01-live` |
| `--ratio, -r` | 1:1 | 宽高比 / Aspect ratio: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9 |
| `--n` | 1 | 生成数量1-9 / Number of images [1-9] |
| `--style, -s` | - | 画风类型（仅image-01-live）/ Style type for image-01-live |
| `--reference, -ref` | - | 参考图URL或base64（用于图生图）/ Reference image URL or base64 |
| `--output, -o` | - | 输出路径 / Output file path |
| `--base64` | false | 返回base64格式 / Return base64 instead of downloading |

## 输出 | Output

脚本自动下载图片到 `/home/ubuntu/.openclaw/workspace/images/`

Script auto-downloads images to workspace images directory.

返回 / Returns:
- `image_urls`: 图片URL列表 / List of image URLs
- `_local_paths`: 本地保存路径 / Local saved file paths

## 环境要求 | Requirements

需要设置 `MINIMAX_API_KEY` 环境变量 / Requires `MINIMAX_API_KEY` environment variable:

```bash
export MINIMAX_API_KEY="your-api-key-here"
```

API Key 获取地址 / Get API Key: https://platform.minimaxi.com

## 注意事项 | Notes

- ⚠️ `image-01-live` 需要会员订阅 / Requires premium subscription
- ⚠️ 图片URL有效期24小时 / Image URLs expire in 24 hours
- 图片建议小于10MB / Image should be under 10MB
- 参考图建议单人正面照片 / Reference: single person, frontal photo works best

## 详细API文档 | Full API Reference

- [API文档（中文）](references/api.md)
- [API Reference（English）](references/api_en.md)
