from pathlib import Path
from PIL import Image
import json
root = Path(__file__).parent
image = Image.open(root / "setup-Aggregate-on.png").convert("RGB")
results = []
for color, expected in [((80, 144, 220), [220, 140, 160]), ((255, 160, 58), [45, 30, 40])]:
    points = {(x, y) for y in range(105, 357) for x in range(323, 837) if image.getpixel((x, y)) == color}
    boxes = []
    while points:
        seed = points.pop()
        stack, component = [seed], [seed]
        while stack:
            x, y = stack.pop()
            for adjacent in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if adjacent in points:
                    points.remove(adjacent)
                    stack.append(adjacent)
                    component.append(adjacent)
        if len(component) > 100:
            xs, ys = zip(*component)
            boxes.append({"x":min(xs),"y":min(ys),"width":max(xs)-min(xs)+1,"height":max(ys)-min(ys)+1})
    boxes.sort(key=lambda b:b["x"])
    assert len(boxes) == 3, boxes
    for box, value in zip(boxes, expected):
        assert abs(box["height"] - value * 251 / 250) <= 2, (box, value)
        assert abs(box["y"] + box["height"] - 356) <= 2, box
    results.append({"rgb":color,"boxes":boxes,"expectedValues":expected,"passed":True})
(root / "pixel-verification.json").write_text(json.dumps({"plotCrop":[323,105,837,357],"axisRange":[0,250],"plotHeight":251,"heightTolerancePixels":2,"results":results},indent=2))
print("PASS: six rendered bars match settled sum values and common baseline within two pixels")
