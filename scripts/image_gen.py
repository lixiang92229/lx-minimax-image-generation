#!/usr/bin/env python3
"""
MiniMax Image Generation Tool
Supports text-to-image (t2i) and image-to-image (i2i)
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error


API_BASE = "https://api.minimaxi.com/v1/image_generation"

# MiniMax API Key - can pass via --api-key argument or set MINIMAX_API_KEY env var
API_KEY = os.environ.get("MINIMAX_API_KEY", "")

# Default output directory
OUTPUT_DIR = "/home/ubuntu/.openclaw/workspace/images"


def generate_image(
    prompt: str,
    model: str = "image-01",
    style_type: str = None,
    style_weight: float = 0.8,
    aspect_ratio: str = "1:1",
    width: int = None,
    height: int = None,
    response_format: str = "url",
    seed: int = None,
    n: int = 1,
    prompt_optimizer: bool = False,
    aigc_watermark: bool = False,
    subject_reference: list = None,
    output_path: str = None,
) -> dict:
    """
    Generate image(s) using MiniMax API.
    
    Args:
        prompt: Text description of the image (max 1500 chars)
        model: "image-01" or "image-01-live"
        style_type: For image-01-live: "漫画", "元气", "中世纪", "水彩"
        style_weight: Style weight (0, 1], default 0.8
        aspect_ratio: "1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"
        width: Image width [512, 2048], must be multiple of 8
        height: Image height [512, 2048], must be multiple of 8
        response_format: "url" or "base64"
        seed: Random seed for reproducibility
        n: Number of images to generate [1, 9]
        prompt_optimizer: Enable auto prompt optimization
        aigc_watermark: Add AIGC watermark
        subject_reference: For i2i, list of {type: "character", image_file: "url or base64"}
        output_path: Where to save the downloaded image(s)
    
    Returns:
        dict with image_urls or image_base64 data
    """
    
    if not API_KEY:
        return {"error": "MINIMAX_API_KEY not set"}
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": response_format,
        "n": n,
        "prompt_optimizer": prompt_optimizer,
        "aigc_watermark": aigc_watermark,
    }
    
    # Add style for image-01-live
    if model == "image-01-live" and style_type:
        payload["style"] = {
            "style_type": style_type,
            "style_weight": style_weight,
        }
    
    # Add dimensions if specified
    if width and height:
        payload["width"] = width
        payload["height"] = height
    
    # Add seed if specified
    if seed is not None:
        payload["seed"] = seed
    
    # Add subject reference for i2i
    if subject_reference:
        payload["subject_reference"] = subject_reference
    
    req = urllib.request.Request(
        API_BASE,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            
            if result.get("base_resp", {}).get("status_code") != 0:
                return {
                    "error": result.get("base_resp", {}).get("status_msg", "Unknown error")
                }
            
            # If response_format is url, download images
            if response_format == "url" and result.get("data", {}).get("image_urls"):
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                image_urls = result["data"]["image_urls"]
                saved_paths = []
                
                for i, url in enumerate(image_urls):
                    # Generate filename
                    if output_path and len(image_urls) == 1:
                        filename = output_path
                    else:
                        timestamp = int(time.time())
                        ext = "png" if url.endswith(".png") else "jpg"
                        filename = f"{OUTPUT_DIR}/img_{timestamp}_{i+1}.{ext}"
                    
                    # Download image
                    try:
                        download_req = urllib.request.Request(url)
                        with urllib.request.urlopen(download_req, timeout=30) as img_resp:
                            with open(filename, "wb") as f:
                                f.write(img_resp.read())
                        saved_paths.append(filename)
                    except Exception as e:
                        saved_paths.append({"url": url, "download_error": str(e)})
                
                result["_local_paths"] = saved_paths
            
            return result
    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="MiniMax Image Generation")
    parser.add_argument("--prompt", "-p", required=True, help="Image description")
    parser.add_argument("--model", "-m", default="image-01", choices=["image-01", "image-01-live"])
    parser.add_argument("--style", "-s", help="Style type (for image-01-live): 漫画/元气/中世纪/水彩")
    parser.add_argument("--ratio", "-r", default="1:1", help="Aspect ratio: 1:1/16:9/4:3/3:2/2:3/3:4/9:16/21:9")
    parser.add_argument("--n", "-n", type=int, default=1, help="Number of images [1-9]")
    parser.add_argument("--output", "-o", help="Output path (single image)")
    parser.add_argument("--base64", action="store_true", help="Return base64 instead of downloading")
    parser.add_argument("--api-key", help="MiniMax API Key (or set MINIMAX_API_KEY env var)")
    
    # 图生图参数
    parser.add_argument("--reference", "-ref", help="Reference image URL or base64 (for i2i)")
    parser.add_argument("--ref-type", default="character", help="Reference type: character (default)")
    
    args = parser.parse_args()
    
    # Use --api-key argument if provided, otherwise fall back to environment variable
    if args.api_key:
        os.environ["MINIMAX_API_KEY"] = args.api_key
    
    # 构建subject_reference（用于图生图）
    subject_reference = None
    if args.reference:
        subject_reference = [
            {
                "type": args.ref_type,
                "image_file": args.reference
            }
        ]
    
    result = generate_image(
        prompt=args.prompt,
        model=args.model,
        style_type=args.style,
        aspect_ratio=args.ratio,
        n=args.n,
        response_format="base64" if args.base64 else "url",
        output_path=args.output,
        subject_reference=subject_reference,
    )
    
    if "error" in result:
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
